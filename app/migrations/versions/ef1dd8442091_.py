"""empty message

Revision ID: ef1dd8442091
Revises: 
Create Date: 2020-11-11 10:22:57.933853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef1dd8442091'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rolename', sa.String(length=60), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('usuario', sa.Column('menor_tiempo', sa.Integer(), nullable=True))
    op.drop_column('usuario', 'admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuario', sa.Column('admin', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('usuario', 'menor_tiempo')
    op.drop_table('role')
    # ### end Alembic commands ###
