"""Create File

Revision ID: 4725d1ecc8da
Revises: cc105ee77163
Create Date: 2023-02-23 17:15:54.472462

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '4725d1ecc8da'
down_revision = 'cc105ee77163'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('is_downloadable', sa.Boolean(), nullable=True),
    sa.Column('owner', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_created_at'), 'file', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_file_created_at'), table_name='file')
    op.drop_table('file')
    # ### end Alembic commands ###