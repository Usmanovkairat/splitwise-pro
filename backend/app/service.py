from datetime import datetime, timezone
from uuid import uuid4
from .domain import DomainError, allocate, balances, analytics


class Service:
    def __init__(self, repository):
        self.repo = repository

    def require(self, collection, resource_id, group_id=None):
        value = self.repo.get(collection, resource_id)
        if value is None or (
            group_id is not None and value.get("group_id") != group_id
        ):
            raise DomainError("Resource not found", 404)
        return value

    def group(self, group_id):
        return self.require("groups", group_id)

    def list(self, collection, group_id):
        self.group(group_id)
        return self.repo.list(collection, group_id)

    def create_group(self, data):
        return self.repo.save(
            "groups",
            dict(
                id=str(uuid4()),
                **data,
                created_at=datetime.now(timezone.utc).isoformat()
            ),
        )

    def update_group(self, group_id, data):
        return self.repo.save("groups", {**self.group(group_id), **data})

    def delete_group(self, group_id):
        self.group(group_id)
        self.repo.delete_group(group_id)

    def add_member(self, group_id, data):
        self.group(group_id)
        if any(
            m["name"].casefold() == data["name"].casefold()
            for m in self.repo.list("members", group_id)
        ):
            raise DomainError("A member with this name already exists")
        return self.repo.save(
            "members", dict(id=str(uuid4()), group_id=group_id, **data)
        )

    def remove_member(self, group_id, member_id):
        self.group(group_id)
        self.require("members", member_id, group_id)
        used = any(
            e["payer_id"] == member_id or member_id in e["split_values"]
            for e in self.repo.list("expenses", group_id)
        )
        used |= any(
            member_id in (s["from_member_id"], s["to_member_id"])
            for s in self.repo.list("settlements", group_id)
        )
        if used:
            raise DomainError("Member is referenced by the ledger", 409)
        self.repo.delete("members", member_id)

    def expense(self, group_id, data, expense_id=None):
        self.group(group_id)
        if expense_id:
            self.require("expenses", expense_id, group_id)
        member_ids = {m["id"] for m in self.repo.list("members", group_id)}
        if (
            data["payer_id"] not in member_ids
            or not set(data["split_values"]) <= member_ids
        ):
            raise DomainError("Payer and participants must belong to this group")
        shares = allocate(
            data["amount_minor"], data["split_type"], data["split_values"]
        )
        return self.repo.save(
            "expenses",
            dict(
                id=expense_id or str(uuid4()), group_id=group_id, **data, shares=shares
            ),
        )

    def delete_expense(self, group_id, expense_id):
        self.group(group_id)
        self.require("expenses", expense_id, group_id)
        self.repo.delete("expenses", expense_id)

    def balances(self, group_id):
        self.group(group_id)
        return balances(
            *(
                self.repo.list(c, group_id)
                for c in ("members", "expenses", "settlements")
            )
        )

    def settlement(self, group_id, data):
        balance = self.balances(group_id)
        a, b = data["from_member_id"], data["to_member_id"]
        rows = {m["member_id"]: m for m in balance["members"]}
        if a == b or a not in rows or b not in rows:
            raise DomainError("Settlement requires two different group members")
        if rows[a]["net_minor"] >= 0 or rows[b]["net_minor"] <= 0:
            raise DomainError("Settlement must go from debtor to creditor")
        if data["amount_minor"] > min(-rows[a]["net_minor"], rows[b]["net_minor"]):
            raise DomainError("Settlement exceeds an outstanding balance")
        return self.repo.save(
            "settlements", dict(id=str(uuid4()), group_id=group_id, **data)
        )

    def analytics(self, group_id):
        self.group(group_id)
        return analytics(
            *(
                self.repo.list(c, group_id)
                for c in ("members", "expenses", "settlements")
            )
        )
