"""Initial relational shared-expense ledger."""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial_ledger"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "groups",
        sa.Column("id", sa.String(100), primary_key=True),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("description", sa.String(500), nullable=False),
        sa.Column("created_at", sa.String(40), nullable=False),
        sa.CheckConstraint(
            "currency IN ('KZT','USD','EUR','GBP')", name="ck_group_currency"
        ),
    )
    op.create_table(
        "members",
        sa.Column("id", sa.String(100), primary_key=True),
        sa.Column(
            "group_id", sa.String(100), sa.ForeignKey("groups.id"), nullable=False
        ),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("normalized_name", sa.String(240), nullable=False),
        sa.UniqueConstraint("group_id", "normalized_name", name="uq_member_group_name"),
    )
    op.create_index("ix_members_group_id", "members", ["group_id"])
    op.create_table(
        "expenses",
        sa.Column("id", sa.String(100), primary_key=True),
        sa.Column(
            "group_id", sa.String(100), sa.ForeignKey("groups.id"), nullable=False
        ),
        sa.Column("description", sa.String(200), nullable=False),
        sa.Column("amount_minor", sa.BigInteger(), nullable=False),
        sa.Column(
            "payer_id", sa.String(100), sa.ForeignKey("members.id"), nullable=False
        ),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("date", sa.String(10), nullable=False),
        sa.Column("split_type", sa.String(10), nullable=False),
        sa.CheckConstraint("amount_minor > 0", name="ck_expense_positive"),
        sa.CheckConstraint(
            "split_type IN ('equal','exact','percentage')", name="ck_expense_split_type"
        ),
    )
    op.create_index("ix_expenses_group_id", "expenses", ["group_id"])
    op.create_index("ix_expenses_date", "expenses", ["date"])
    op.create_table(
        "expense_shares",
        sa.Column(
            "expense_id",
            sa.String(100),
            sa.ForeignKey("expenses.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "member_id", sa.String(100), sa.ForeignKey("members.id"), primary_key=True
        ),
        sa.Column("split_value", sa.BigInteger(), nullable=False),
        sa.Column("amount_minor", sa.BigInteger(), nullable=False),
        sa.CheckConstraint("split_value >= 0", name="ck_share_value"),
        sa.CheckConstraint("amount_minor >= 0", name="ck_share_amount"),
    )
    op.create_table(
        "settlements",
        sa.Column("id", sa.String(100), primary_key=True),
        sa.Column(
            "group_id", sa.String(100), sa.ForeignKey("groups.id"), nullable=False
        ),
        sa.Column(
            "from_member_id",
            sa.String(100),
            sa.ForeignKey("members.id"),
            nullable=False,
        ),
        sa.Column(
            "to_member_id", sa.String(100), sa.ForeignKey("members.id"), nullable=False
        ),
        sa.Column("amount_minor", sa.BigInteger(), nullable=False),
        sa.Column("date", sa.String(10), nullable=False),
        sa.Column("note", sa.String(500), nullable=False),
        sa.CheckConstraint("amount_minor > 0", name="ck_settlement_positive"),
        sa.CheckConstraint(
            "from_member_id != to_member_id", name="ck_settlement_distinct"
        ),
    )
    op.create_index("ix_settlements_group_id", "settlements", ["group_id"])
    op.create_index("ix_settlements_date", "settlements", ["date"])


def downgrade():
    for table in ("settlements", "expense_shares", "expenses", "members", "groups"):
        op.drop_table(table)
