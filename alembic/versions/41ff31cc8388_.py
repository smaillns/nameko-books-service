"""empty message

Revision ID: 41ff31cc8388
Revises:
Create Date: 2021-12-31 12:06:47.917788

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "41ff31cc8388"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'authors',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column(
            'gender',
            sa.Enum(
                'Male',
                'Female',
                name='authorGender'
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'books',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(('author_id',), ['authors.id'], ),
    )


def downgrade():
    op.drop_table("authors")
    op.drop_table("books")
