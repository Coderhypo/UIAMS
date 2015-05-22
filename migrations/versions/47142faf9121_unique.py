"""unique

Revision ID: 47142faf9121
Revises: 2f8630a6f269
Create Date: 2015-05-22 11:40:36.423778

"""

# revision identifiers, used by Alembic.
revision = '47142faf9121'
down_revision = '2f8630a6f269'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'major', ['major_name'])
    op.create_unique_constraint(None, 'major', ['major_id'])
    op.create_unique_constraint(None, 'unit', ['unit_id'])
    op.create_unique_constraint(None, 'unit', ['unit_name'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'unit', type_='unique')
    op.drop_constraint(None, 'unit', type_='unique')
    op.drop_constraint(None, 'major', type_='unique')
    op.drop_constraint(None, 'major', type_='unique')
    ### end Alembic commands ###
