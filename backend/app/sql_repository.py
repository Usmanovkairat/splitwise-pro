from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .models import Group, Member, Expense, ExpenseShare, Settlement
from .domain import DomainError

MODELS = {
    "groups": Group,
    "members": Member,
    "expenses": Expense,
    "settlements": Settlement,
}


class SQLAlchemyRepository:
    def __init__(self, engine):
        self.engine = engine

    def _serialize(self, session, collection, row):
        value = {
            c.name: getattr(row, c.name)
            for c in row.__table__.columns
            if c.name != "normalized_name"
        }
        if collection == "expenses":
            shares = session.scalars(
                select(ExpenseShare)
                .where(ExpenseShare.expense_id == row.id)
                .order_by(ExpenseShare.member_id)
            ).all()
            value["split_values"] = {s.member_id: s.split_value for s in shares}
            value["shares"] = [
                dict(member_id=s.member_id, amount_minor=s.amount_minor) for s in shares
            ]
        return value

    def list(self, collection, group_id=None):
        model = MODELS[collection]
        statement = select(model)
        if group_id is not None:
            statement = statement.where(model.group_id == group_id)
        statement = statement.order_by(model.id)
        with Session(self.engine) as session:
            return [
                self._serialize(session, collection, row)
                for row in session.scalars(statement)
            ]

    def get(self, collection, resource_id):
        with Session(self.engine) as session:
            row = session.get(MODELS[collection], resource_id)
            return self._serialize(session, collection, row) if row else None

    def save(self, collection, value):
        fields = {k: v for k, v in value.items() if k not in ("shares", "split_values")}
        if collection == "members":
            fields["normalized_name"] = fields["name"].casefold()
        try:
            with Session(self.engine) as session, session.begin():
                session.merge(MODELS[collection](**fields))
                session.flush()
                if collection == "expenses":
                    session.execute(
                        delete(ExpenseShare).where(
                            ExpenseShare.expense_id == value["id"]
                        )
                    )
                    for share in value["shares"]:
                        session.add(
                            ExpenseShare(
                                expense_id=value["id"],
                                member_id=share["member_id"],
                                amount_minor=share["amount_minor"],
                                split_value=value["split_values"][share["member_id"]],
                            )
                        )
        except IntegrityError as exc:
            raise DomainError(
                "Write conflicts with an existing member or ledger reference", 409
            ) from exc
        return self.get(collection, value["id"])

    def delete(self, collection, resource_id):
        try:
            with Session(self.engine) as session, session.begin():
                session.execute(
                    delete(MODELS[collection]).where(
                        MODELS[collection].id == resource_id
                    )
                )
        except IntegrityError as exc:
            raise DomainError("Resource is referenced by the ledger", 409) from exc

    def delete_group(self, group_id):
        with Session(self.engine) as session, session.begin():
            expense_ids = select(Expense.id).where(Expense.group_id == group_id)
            session.execute(
                delete(ExpenseShare).where(ExpenseShare.expense_id.in_(expense_ids))
            )
            for model in (Expense, Settlement, Member):
                session.execute(delete(model).where(model.group_id == group_id))
            session.execute(delete(Group).where(Group.id == group_id))
