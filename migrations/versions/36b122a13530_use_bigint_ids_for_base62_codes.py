"""use bigint ids for base62 codes

Revision ID: 36b122a13530
Revises: 3263b9d34bf4
Create Date: 2026-09-30 10:11:04.188991

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '36b122a13530'
down_revision: Union[str, Sequence[str], None] = '3263b9d34bf4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'short_urls',
        'id',
        existing_type=sa.Integer(),
        type_=sa.BigInteger(),
        existing_nullable=False
    )

    op.execute('ALTER SEQUENCE short_urls_id_seq AS BIGINT NO MAXVALUE')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'short_urls',
        'id',
        existing_type=sa.BigInteger(),
        type_=sa.Integer(),
        existing_nullable=False
    )

    op.execute('ALTER SEQUENCE short_urls_id_seq AS INTEGER NO MAXVALUE')
