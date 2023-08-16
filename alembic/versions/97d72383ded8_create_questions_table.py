"""create questions table

Revision ID: 97d72383ded8
Revises: 
Create Date: 2023-08-14 19:10:42.886950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97d72383ded8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'questions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('unique_id', sa.String(), nullable=False),
        sa.Column('internal_id', sa.String(), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('repository', sa.String(), nullable=False),
        sa.Column('language', sa.String(), nullable=False),
        sa.Column('src_filename', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'print_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            "question_id",
            sa.Integer,
            sa.ForeignKey("questions.id"),
            nullable=False,
        ),
        sa.Column('log_number', sa.Integer(), nullable=False),
    )

    op.create_table(
        'metrics',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            "question_id",
            sa.Integer,
            sa.ForeignKey("questions.id"),
            nullable=False,
        ),
    )

    op.create_table(
        'choices',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            "question_id",
            sa.Integer,
            sa.ForeignKey("questions.id"),
            nullable=False,
        ),
    )

    op.create_table(
        'tags',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            "question_id",
            sa.Integer,
            sa.ForeignKey("questions.id"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table('print_logs')
    op.drop_table('tags')
    op.drop_table('choices')
    op.drop_table('metrics')
    op.drop_table('questions')
