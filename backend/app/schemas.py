from datetime import date as Date
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

MAX_MONEY = 1_000_000_000_000
Minor = Annotated[int, Field(strict=True, ge=0, le=MAX_MONEY)]
Positive = Annotated[int, Field(strict=True, gt=0, le=MAX_MONEY)]
Name = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)
]
Text = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
]
Identifier = Annotated[str, StringConstraints(min_length=1, max_length=100)]


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid")

    @field_validator("date", mode="before", check_fields=False)
    @classmethod
    def iso_date(cls, value):
        if (
            not isinstance(value, str)
            or len(value) != 10
            or value[4] != "-"
            or value[7] != "-"
        ):
            raise ValueError("Use an ISO date YYYY-MM-DD")
        try:
            return Date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError("Use a valid ISO calendar date") from exc


class GroupInput(Input):
    name: Name
    currency: Literal["KZT", "USD", "EUR", "GBP"]
    description: Annotated[
        str, StringConstraints(strip_whitespace=True, max_length=500)
    ]


class GroupUpdate(Input):
    name: Name
    description: Annotated[
        str, StringConstraints(strip_whitespace=True, max_length=500)
    ]


class MemberInput(Input):
    name: Name


class ExpenseInput(Input):
    description: Text
    amount_minor: Positive
    payer_id: Identifier
    category: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)
    ]
    date: Date
    split_type: Literal["equal", "exact", "percentage"]
    split_values: Annotated[
        dict[Identifier, Minor], Field(min_length=1, max_length=100)
    ]


class SettlementInput(Input):
    from_member_id: Identifier
    to_member_id: Identifier
    amount_minor: Positive
    date: Date
    note: Annotated[str, StringConstraints(strip_whitespace=True, max_length=500)]
