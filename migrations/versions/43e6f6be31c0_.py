"""empty message

Revision ID: 43e6f6be31c0
Revises: 4610e29eb91
Create Date: 2015-06-14 19:06:49.890199

"""

# revision identifiers, used by Alembic.
revision = '43e6f6be31c0'
down_revision = '4610e29eb91'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('adviser',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_competition', sa.Integer(), nullable=True),
    sa.Column('id_teacher', sa.Integer(), nullable=True),
    sa.Column('locant', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_competition'], ['competition.id'], ),
    sa.ForeignKeyConstraint(['id_teacher'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_competition', sa.Integer(), nullable=True),
    sa.Column('id_student', sa.Integer(), nullable=True),
    sa.Column('locant', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_competition'], ['competition.id'], ),
    sa.ForeignKeyConstraint(['id_student'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('participants')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('participants',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.drop_table('participant')
    op.drop_table('adviser')
    ### end Alembic commands ###
