"""empty message

Revision ID: f94123368be6
Revises: 8aea3cd9ee1a
Create Date: 2023-03-19 14:42:11.813211

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f94123368be6"
down_revision = "8aea3cd9ee1a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "questions",
        sa.Column("publish_id", sa.String(length=64), nullable=True),
    )
    op.create_unique_constraint(None, "questions", ["publish_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "questions", type_="unique")
    op.drop_column("questions", "publish_id")
    # ### end Alembic commands ###
