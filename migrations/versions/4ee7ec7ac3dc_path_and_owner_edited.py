"""path_and_owner_edited

Revision ID: 4ee7ec7ac3dc
Revises: 4725d1ecc8da
Create Date: 2023-02-28 14:41:44.239840

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '4ee7ec7ac3dc'
down_revision = '4725d1ecc8da'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('file_owner_fkey', 'file', type_='foreignkey')
    op.create_foreign_key(None, 'file', 'user', ['owner'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'file', type_='foreignkey')
    op.create_foreign_key('file_owner_fkey', 'file', 'user', ['owner'], ['id'])
    # ### end Alembic commands ###
