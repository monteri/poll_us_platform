"""empty message

Revision ID: b09e6f48ca43
Revises: 0406fe2d9a02
Create Date: 2023-04-02 13:55:51.825779

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b09e6f48ca43"
down_revision = "0406fe2d9a02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_answers", sa.Column("publish_id", sa.String(length=64), nullable=False)
    )
    op.drop_constraint(
        "user_answers_question_id_fkey", "user_answers", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "user_answers", "questions", ["publish_id"], ["publish_id"]
    )
    op.drop_column("user_answers", "question_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_answers",
        sa.Column("question_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "user_answers", type_="foreignkey")
    op.create_foreign_key(
        "user_answers_question_id_fkey",
        "user_answers",
        "questions",
        ["question_id"],
        ["id"],
    )
    op.drop_column("user_answers", "publish_id")
    # ### end Alembic commands ###
