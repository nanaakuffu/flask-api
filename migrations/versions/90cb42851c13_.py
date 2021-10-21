"""empty message

Revision ID: 90cb42851c13
Revises: 52bd5f219b86
Create Date: 2021-10-21 14:05:06.314836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90cb42851c13'
down_revision = '52bd5f219b86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('verification_sent', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'verification_sent')
    # ### end Alembic commands ###
