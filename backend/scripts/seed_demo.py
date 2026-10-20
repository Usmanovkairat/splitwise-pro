"""Explicitly populate an EMPTY migrated workspace: python -m backend.scripts.seed_demo."""

from backend.app.database import make_engine
from backend.app.sql_repository import SQLAlchemyRepository
from backend.app.service import Service
from backend.app.schemas import ExpenseInput


def seed_demo(repository):
    if repository.list("groups"):
        raise ValueError(
            "Demo seed requires an empty workspace; existing groups were not changed"
        )
    service = Service(repository)
    group = service.create_group(
        dict(
            name="Almaty weekend",
            currency="KZT",
            description="A long weekend with friends: mountains, good food, and shared memories.",
        )
    )
    group_id = group["id"]
    members = [
        service.add_member(group_id, dict(name=name))
        for name in ("Kairat Usmanov", "Aigerim Sadyk", "Timur Ali", "Dana Omar")
    ]
    ids = [member["id"] for member in members]
    records = [
        (
            "Mountain-view apartment",
            9600000,
            0,
            "Accommodation",
            "2026-10-16",
            "equal",
            {key: 1 for key in ids},
        ),
        (
            "Dinner at Navat",
            2840000,
            1,
            "Food & drinks",
            "2026-10-16",
            "equal",
            {key: 1 for key in ids},
        ),
        (
            "Cable car to Shymbulak",
            1280000,
            2,
            "Entertainment",
            "2026-10-17",
            "exact",
            {ids[0]: 320000, ids[1]: 320000, ids[2]: 320000, ids[3]: 320000},
        ),
        (
            "Coffee before the trail",
            138000,
            3,
            "Food & drinks",
            "2026-10-17",
            "percentage",
            {ids[0]: 3000, ids[1]: 2000, ids[2]: 3000, ids[3]: 2000},
        ),
        (
            "Airport transfers",
            420000,
            0,
            "Travel",
            "2026-10-18",
            "equal",
            {key: 1 for key in ids},
        ),
        (
            "Green Bazaar picnic",
            725000,
            1,
            "Shopping",
            "2026-10-18",
            "equal",
            {key: 1 for key in ids},
        ),
        (
            "Last brunch together",
            396001,
            3,
            "Food & drinks",
            "2026-10-19",
            "equal",
            {key: 1 for key in ids},
        ),
    ]
    for description, amount, payer, category, date, split_type, values in records:
        data = ExpenseInput(
            description=description,
            amount_minor=amount,
            payer_id=ids[payer],
            category=category,
            date=date,
            split_type=split_type,
            split_values=values,
        )
        service.expense(group_id, data.model_dump(mode="json"))
    suggestion = service.balances(group_id)["suggestions"][0]
    service.settlement(
        group_id,
        {
            **suggestion,
            "amount_minor": suggestion["amount_minor"] // 3,
            "date": "2026-10-19",
            "note": "First repayment after the trip",
        },
    )
    return group


def main():
    engine = make_engine()
    try:
        group = seed_demo(SQLAlchemyRepository(engine))
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    finally:
        engine.dispose()
    print(f"Created demo group: {group['name']} ({group['id']})")


if __name__ == "__main__":
    main()
