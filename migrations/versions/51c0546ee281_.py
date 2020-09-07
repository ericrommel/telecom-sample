"""empty message

Revision ID: 51c0546ee281
Revises:
Create Date: 2020-09-02 10:58:23.156018

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "51c0546ee281"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "didnumbers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("value", sa.String(length=17), nullable=True),
        sa.Column("monthly_price", sa.Float(), nullable=True),
        sa.Column("setup_price", sa.Float(), nullable=True),
        sa.Column("currency", sa.String(length=3), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("value"),
    )
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=60), nullable=True),
        sa.Column("last_name", sa.String(length=60), nullable=True),
        sa.Column("email", sa.String(length=60), nullable=True),
        sa.Column("username", sa.String(length=60), nullable=True),
        sa.Column("password_hash", sa.String(length=100), nullable=True),
        sa.Column("is_admin", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_employees_email"), "employees", ["email"], unique=True)
    op.create_index(op.f("ix_employees_first_name"), "employees", ["first_name"], unique=False)
    op.create_index(op.f("ix_employees_last_name"), "employees", ["last_name"], unique=False)
    op.create_index(op.f("ix_employees_username"), "employees", ["username"], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_employees_username"), table_name="employees")
    op.drop_index(op.f("ix_employees_last_name"), table_name="employees")
    op.drop_index(op.f("ix_employees_first_name"), table_name="employees")
    op.drop_index(op.f("ix_employees_email"), table_name="employees")
    op.drop_table("employees")
    op.drop_table("didnumbers")
    # ### end Alembic commands ###
