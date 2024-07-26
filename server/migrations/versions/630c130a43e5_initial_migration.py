"""Initial migration

Revision ID: 630c130a43e5
Revises: 
Create Date: 2024-07-26 01:34:58.753401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '630c130a43e5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reddit_id', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('img_url', sa.String(), nullable=True),
    sa.Column('body', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('reddit_id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('authenticated', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('searches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('search_terms', sa.String(), nullable=False),
    sa.Column('origin_user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['origin_user_id'], ['users.id'], name=op.f('fk_searches_origin_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('search_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['search_id'], ['searches.id'], name=op.f('fk_comments_search_id_searches')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_comments_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('search_posts',
    sa.Column('search_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('fk_search_posts_post_id_posts')),
    sa.ForeignKeyConstraint(['search_id'], ['searches.id'], name=op.f('fk_search_posts_search_id_searches'))
    )
    op.create_table('user_searches',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('search_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['search_id'], ['searches.id'], name=op.f('fk_user_searches_search_id_searches')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_searches_user_id_users'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_searches')
    op.drop_table('search_posts')
    op.drop_table('comments')
    op.drop_table('searches')
    op.drop_table('users')
    op.drop_table('posts')
    # ### end Alembic commands ###
