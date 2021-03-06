"""empty message

Revision ID: 5f33cf0ee223
Revises: 
Create Date: 2021-10-20 22:52:31.738216

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5f33cf0ee223'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar')
    op.drop_column('users', 'verification_sent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('verification_sent', mysql.TINYINT(display_width=1), server_default=sa.text("'0'"), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('avatar', mysql.VARCHAR(length=100), nullable=True))
    # ### end Alembic commands ###
