"""add foreign-key to posts table

Revision ID: dd7bbfa973b2
Revises: bad00d724046
Create Date: 2025-05-06 10:54:47.019613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd7bbfa973b2'
down_revision: Union[str, None] = 'bad00d724046'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint(
        'post_users_fk',
        table_name='posts'
    )
    op.drop_column(
        'posts',
        'owner_id'
    )
    pass
