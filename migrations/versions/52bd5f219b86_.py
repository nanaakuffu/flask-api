"""empty message

Revision ID: 52bd5f219b86
Revises: 5f33cf0ee223
Create Date: 2021-10-20 23:02:50.450633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52bd5f219b86'
down_revision = '5f33cf0ee223'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar')
    # ### end Alembic commands ###
