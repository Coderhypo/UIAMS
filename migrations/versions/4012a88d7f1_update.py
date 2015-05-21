"""update

Revision ID: 4012a88d7f1
Revises: 1f42b7429378
Create Date: 2015-05-21 16:11:42.802754

"""

# revision identifiers, used by Alembic.
revision = '4012a88d7f1'
down_revision = '1f42b7429378'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('major', sa.Column('major_id', sa.Integer(), nullable=True))
    op.alter_column('major', 'major_name',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
    op.drop_index('major_name', table_name='major')
    op.add_column('unit', sa.Column('unit_id', sa.Integer(), nullable=True))
    op.alter_column('unit', 'unit_name',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
    op.drop_index('unit_name', table_name='unit')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('unit_name', 'unit', ['unit_name'], unique=True)
    op.alter_column('unit', 'unit_name',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)
    op.drop_column('unit', 'unit_id')
    op.create_index('major_name', 'major', ['major_name'], unique=True)
    op.alter_column('major', 'major_name',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)
    op.drop_column('major', 'major_id')
    ### end Alembic commands ###
