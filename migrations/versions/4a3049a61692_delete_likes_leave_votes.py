"""delete likes leave votes

Revision ID: 4a3049a61692
Revises: b868d7a499a6
Create Date: 2023-01-15 05:23:30.693350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a3049a61692'
down_revision = 'b868d7a499a6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id', 'user_id')
    )
    op.drop_table('dislike')
    op.drop_table('like')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('like',
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='like_post_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='like_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id', 'user_id', name='like_pkey')
    )
    op.create_table('dislike',
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='dislike_post_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='dislike_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id', 'user_id', name='dislike_pkey')
    )
    op.drop_table('votes')
    # ### end Alembic commands ###
