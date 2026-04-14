"""add categorias table

Revision ID: 003
Revises: e2313c722c5e
Create Date: 2026-04-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '003'
down_revision: Union[str, None] = 'e2313c722c5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'categorias',
        sa.Column('nome_categoria', sa.String(100), nullable=False),
        sa.Column('link_imagem', sa.String(500), nullable=False),
        sa.PrimaryKeyConstraint('nome_categoria')
    )


def downgrade() -> None:
    op.drop_table('categorias')
