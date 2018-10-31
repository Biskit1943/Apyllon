"""Add Filepath table to Song, remove filename and directory from Song

Revision ID: 23386b2b8429
Revises: 3d7db9e741ca
Create Date: 2018-10-17 14:56:13.506268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23386b2b8429'
down_revision = '3d7db9e741ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('filepath',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=64), nullable=False),
    sa.Column('directory', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('song', sa.Column('filepath_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'song', 'filepath', ['filepath_id'], ['id'])
    op.drop_column('song', 'filename')
    op.drop_column('song', 'directory')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('song', sa.Column('directory', sa.TEXT(), nullable=False))
    op.add_column('song', sa.Column('filename', sa.VARCHAR(length=64), nullable=False))
    op.drop_constraint(None, 'song', type_='foreignkey')
    op.drop_column('song', 'filepath_id')
    op.drop_table('filepath')
    # ### end Alembic commands ###