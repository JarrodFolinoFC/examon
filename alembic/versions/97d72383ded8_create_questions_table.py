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
        sa.Column('unique_id', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('internal_id', sa.String(), nullable=True, index=True),
        sa.Column('repository', sa.String(), nullable=False, index=True),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('answer', sa.String(), nullable=False),
        sa.Column('language', sa.String(), nullable=False),
        sa.Column('src_filename', sa.String(), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            server_onupdate=sa.func.now(),
            nullable=False,
        )
    )

    op.create_table(
        'print_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('value', sa.String),
        sa.Column(
            "question_id",
            sa.Integer,
            sa.ForeignKey("questions.id"),
            nullable=False,
        ),
        sa.Column('log_number', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            server_onupdate=sa.func.now(),
            nullable=False,
        )
    )

    op.create_table(
        'metrics',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('no_of_functions', sa.Integer(), nullable=False),
        sa.Column('loc', sa.Integer(), nullable=False),
        sa.Column('lloc', sa.Integer(), nullable=False),
        sa.Column('sloc', sa.Integer(), nullable=False),
        sa.Column('difficulty', sa.Float(), nullable=False),
        sa.Column('categorised_difficulty', sa.String(), nullable=False),
        sa.Column(
            "question_id",
            sa.Integer,
            sa.ForeignKey("questions.id"),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            server_onupdate=sa.func.now(),
            nullable=False,
        )
    )

    op.create_table(
        'choices',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('value', sa.String),
        sa.Column(
            "question_id",
            sa.Integer,
            sa.ForeignKey("questions.id"),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            server_onupdate=sa.func.now(),
            nullable=False,
        )
    )

    op.create_table(
        'tags',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('value', sa.String, nullable=False),
        sa.Column(
            "question_id",
            sa.Integer,
            sa.ForeignKey("questions.id"),
            nullable=False,
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            server_onupdate=sa.func.now(),
            nullable=False,
        )
    )

    # op.create_unique_constraint('tags_value_question_id', 'user', ['tags', 'question_id'])


def downgrade() -> None:
    op.drop_table('print_logs')
    op.drop_table('tags')
    op.drop_table('choices')
    op.drop_table('metrics')
    op.drop_table('questions')
