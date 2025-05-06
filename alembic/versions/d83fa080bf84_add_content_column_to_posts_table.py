"""add content column to posts table

Revision ID: d83fa080bf84
Revises: 1c554ec0e8dd
Create Date: 2025-05-06 10:27:11.644747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd83fa080bf84'
down_revision: Union[str, None] = '1c554ec0e8dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column(
        'posts',
        'content'
    )
    pass
