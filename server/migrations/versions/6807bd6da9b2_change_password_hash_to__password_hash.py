"""change password_hash to _password_hash

Revision ID: 6807bd6da9b2
Revises: abe05c39b249
Create Date: 2024-08-12 11:37:15.122164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6807bd6da9b2'
down_revision = 'abe05c39b249'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_password_hash', sa.String(), nullable=True))
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('_password_hash')

    # ### end Alembic commands ###
