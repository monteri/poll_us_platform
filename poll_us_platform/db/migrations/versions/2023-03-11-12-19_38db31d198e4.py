"""empty message

Revision ID: 38db31d198e4
Revises: 7373003f04ba
Create Date: 2023-03-11 12:19:52.661001

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "38db31d198e4"
down_revision = "7373003f04ba"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "answers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(length=500), nullable=False),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["questions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("answers")
    # ### end Alembic commands ###
