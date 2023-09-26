"""empty message

Revision ID: 8446322410d3
Revises: 8ac97084e8eb
Create Date: 2023-09-24 19:54:23.547901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8446322410d3'
down_revision = '8ac97084e8eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fs_uniquifier', sa.String(length=64), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('fs_uniquifier')

    # ### end Alembic commands ###
