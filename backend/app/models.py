"""Portable SQLAlchemy relational ledger; no JSON blobs or SQLite-specific SQL."""

from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    currency: Mapped[str] = mapped_column(String(3))
    description: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[str] = mapped_column(String(40))
    __table_args__ = (
        CheckConstraint(
            "currency IN ('KZT','USD','EUR','GBP')", name="ck_group_currency"
        ),
    )


class Member(Base):
    __tablename__ = "members"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    group_id: Mapped[str] = mapped_column(ForeignKey("groups.id"), index=True)
    name: Mapped[str] = mapped_column(String(80))
    normalized_name: Mapped[str] = mapped_column(String(240))
    __table_args__ = (
        UniqueConstraint("group_id", "normalized_name", name="uq_member_group_name"),
    )


class Expense(Base):
    __tablename__ = "expenses"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    group_id: Mapped[str] = mapped_column(ForeignKey("groups.id"), index=True)
    description: Mapped[str] = mapped_column(String(200))
    amount_minor: Mapped[int] = mapped_column(BigInteger)
    payer_id: Mapped[str] = mapped_column(ForeignKey("members.id"))
    category: Mapped[str] = mapped_column(String(50))
    date: Mapped[str] = mapped_column(String(10), index=True)
    split_type: Mapped[str] = mapped_column(String(10))
    __table_args__ = (
        CheckConstraint("amount_minor > 0", name="ck_expense_positive"),
        CheckConstraint(
            "split_type IN ('equal','exact','percentage')", name="ck_expense_split_type"
        ),
    )


class ExpenseShare(Base):
    __tablename__ = "expense_shares"
    expense_id: Mapped[str] = mapped_column(
        ForeignKey("expenses.id", ondelete="CASCADE"), primary_key=True
    )
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id"), primary_key=True)
    split_value: Mapped[int] = mapped_column(BigInteger)
    amount_minor: Mapped[int] = mapped_column(BigInteger)
    __table_args__ = (
        CheckConstraint("split_value >= 0", name="ck_share_value"),
        CheckConstraint("amount_minor >= 0", name="ck_share_amount"),
    )


class Settlement(Base):
    __tablename__ = "settlements"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    group_id: Mapped[str] = mapped_column(ForeignKey("groups.id"), index=True)
    from_member_id: Mapped[str] = mapped_column(ForeignKey("members.id"))
    to_member_id: Mapped[str] = mapped_column(ForeignKey("members.id"))
    amount_minor: Mapped[int] = mapped_column(BigInteger)
    date: Mapped[str] = mapped_column(String(10), index=True)
    note: Mapped[str] = mapped_column(String(500))
    __table_args__ = (
        CheckConstraint("amount_minor > 0", name="ck_settlement_positive"),
        CheckConstraint(
            "from_member_id != to_member_id", name="ck_settlement_distinct"
        ),
    )
