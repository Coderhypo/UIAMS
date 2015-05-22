"""update

Revision ID: 4ff862cb66a8
Revises: 3744d69dc02f
Create Date: 2015-05-22 12:37:43.321338

"""

# revision identifiers, used by Alembic.
revision = '4ff862cb66a8'
down_revision = '3744d69dc02f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('unit_id', table_name='unit')
    op.drop_index('unit_id_2', table_name='unit')
    op.drop_column('unit', 'is_acachemy')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('unit', sa.Column('is_acachemy', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.create_index('unit_id_2', 'unit', ['unit_id'], unique=True)
    op.create_index('unit_id', 'unit', ['unit_id'], unique=True)
    ### end Alembic commands ###
