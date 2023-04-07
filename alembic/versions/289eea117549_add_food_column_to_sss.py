"""add food column to sss

Revision ID: 289eea117549
Revises: 35885c2a84ba
Create Date: 2023-04-07 13:30:42.673578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '289eea117549'
down_revision = '35885c2a84ba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('self_sufficiency_standard', sa.Column('food', sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column('self_sufficiency_standard', 'food')
