"""Alterado coluna 'capacity' (string) para 'capacity_per_kilo' (integer) da tabela 'Vehicle'.

Revision ID: e0f5c48669e7
Revises: dbfc51cb11f4
Create Date: 2025-06-26 22:54:28.296210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0f5c48669e7'
down_revision = 'dbfc51cb11f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.add_column(sa.Column('capacity_per_kilo', sa.Integer(), nullable=False))
        batch_op.drop_column('capacity')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.add_column(sa.Column('capacity', sa.VARCHAR(), nullable=False))
        batch_op.drop_column('capacity_per_kilo')

    # ### end Alembic commands ###
