"""Pure integer accounting. Positive net means the member is owed money."""

from collections import defaultdict


class DomainError(Exception):
    def __init__(self, detail: str, status: int = 422):
        self.detail, self.status = detail, status
        super().__init__(detail)


def allocate(amount: int, method: str, values: dict[str, int]) -> list[dict]:
    if not values:
        raise DomainError("Select at least one participant")
    ids = sorted(values)
    if method == "exact":
        if sum(values.values()) != amount:
            raise DomainError("Exact shares must sum to the expense amount")
        shares = values.copy()
    else:
        weights = {key: 1 for key in ids} if method == "equal" else values
        total = len(ids) if method == "equal" else 10000
        if method == "percentage" and sum(values.values()) != 10000:
            raise DomainError("Percentage basis points must sum to 10000")
        shares = {key: amount * weights[key] // total for key in ids}
        order = sorted(ids, key=lambda key: (-(amount * weights[key] % total), key))
        for key in order[: amount - sum(shares.values())]:
            shares[key] += 1
    return [{"member_id": key, "amount_minor": shares[key]} for key in ids]


def balances(members, expenses, settlements):
    ledger = {
        m["id"]: dict(
            member_id=m["id"], name=m["name"], paid_minor=0, owed_minor=0, net_minor=0
        )
        for m in members
    }
    for expense in expenses:
        ledger[expense["payer_id"]]["paid_minor"] += expense["amount_minor"]
        for share in expense["shares"]:
            ledger[share["member_id"]]["owed_minor"] += share["amount_minor"]
    for row in ledger.values():
        row["net_minor"] = row["paid_minor"] - row["owed_minor"]
    for settlement in settlements:
        ledger[settlement["from_member_id"]]["net_minor"] += settlement["amount_minor"]
        ledger[settlement["to_member_id"]]["net_minor"] -= settlement["amount_minor"]
    debtors = [
        [r["member_id"], -r["net_minor"]] for r in ledger.values() if r["net_minor"] < 0
    ]
    creditors = [
        [r["member_id"], r["net_minor"]] for r in ledger.values() if r["net_minor"] > 0
    ]
    suggestions = []
    while debtors and creditors:
        debtors.sort(key=lambda x: (-x[1], x[0]))
        creditors.sort(key=lambda x: (-x[1], x[0]))
        debtor, creditor = debtors[0], creditors[0]
        amount = min(debtor[1], creditor[1])
        suggestions.append(
            dict(
                from_member_id=debtor[0], to_member_id=creditor[0], amount_minor=amount
            )
        )
        debtor[1] -= amount
        creditor[1] -= amount
        if not debtor[1]:
            debtors.pop(0)
        if not creditor[1]:
            creditors.pop(0)
    return dict(
        members=sorted(ledger.values(), key=lambda r: r["member_id"]),
        suggestions=suggestions,
        total_minor=sum(e["amount_minor"] for e in expenses),
    )


def analytics(members, expenses, settlements):
    categories, dates, contributions = (
        defaultdict(int),
        defaultdict(int),
        defaultdict(int),
    )
    for e in expenses:
        categories[e["category"]] += e["amount_minor"]
        dates[e["date"]] += e["amount_minor"]
        contributions[e["payer_id"]] += e["amount_minor"]
    balance = balances(members, expenses, settlements)
    return dict(
        total_minor=balance["total_minor"],
        by_category=[
            dict(category=k, amount_minor=v) for k, v in sorted(categories.items())
        ],
        over_time=[dict(date=k, amount_minor=v) for k, v in sorted(dates.items())],
        contributions=[
            dict(member_id=m["id"], name=m["name"], amount_minor=contributions[m["id"]])
            for m in sorted(members, key=lambda x: x["id"])
        ],
        outstanding_minor=sum(max(0, m["net_minor"]) for m in balance["members"]),
    )
