"""rename description to category and new description field added

Revision ID: d7174ad3e95c
Revises: 5d4963cad7d4
Create Date: 2024-11-25 08:44:32.528304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7174ad3e95c'
down_revision = '5d4963cad7d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('spending', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('spending', schema=None) as batch_op:
        batch_op.drop_column('category')

    # ### end Alembic commands ###