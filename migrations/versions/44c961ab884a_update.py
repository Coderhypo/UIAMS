"""update

Revision ID: 44c961ab884a
Revises: 58f1ecb4c6a9
Create Date: 2015-05-04 21:01:56.751650

"""

# revision identifiers, used by Alembic.
revision = '44c961ab884a'
down_revision = '58f1ecb4c6a9'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('competition', sa.Column('id_competitionproject', sa.Integer(), nullable=True))
    op.drop_constraint(u'competition_ibfk_1', 'competition', type_='foreignkey')
    op.create_foreign_key(None, 'competition', 'competitionproject', ['id_competitionproject'], ['id'])
    op.drop_column('competition', 'id_project')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('competition', sa.Column('id_project', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'competition', type_='foreignkey')
    op.create_foreign_key(u'competition_ibfk_1', 'competition', 'competitionproject', ['id_project'], ['id'])
    op.drop_column('competition', 'id_competitionproject')
    ### end Alembic commands ###
