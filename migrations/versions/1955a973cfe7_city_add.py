"""city add

Revision ID: 1955a973cfe7
Revises: 5e02cb10127f
Create Date: 2024-04-20 04:02:40.876587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1955a973cfe7'
down_revision: Union[str, None] = '5e02cb10127f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
