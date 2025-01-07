"""add 2 fileds to cheque

Revision ID: 75533741767d
Revises: 03bd0001c647
Create Date: 2025-01-07 23:51:40.373283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75533741767d'
down_revision: Union[str, None] = '03bd0001c647'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cheques', sa.Column('total', sa.Double(), nullable=False))
    op.add_column('cheques', sa.Column('notes', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cheques', 'notes')
    op.drop_column('cheques', 'total')
    # ### end Alembic commands ###
