"""empty message

Revision ID: 6b8149be3a14
Revises: 200180470f72
Create Date: 2025-04-08 19:22:36.179542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b8149be3a14'
down_revision = '200180470f72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auth_token', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('token',
               existing_type=sa.TEXT(),
               type_=sa.String(length=255),
               nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               nullable=False)
        batch_op.drop_index('idx_16385_sqlite_autoindex_auth_token_1')
        batch_op.create_unique_constraint(None, ['token'])

    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('uuid',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               nullable=False)
        batch_op.alter_column('img',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
        batch_op.alter_column('category',
               existing_type=sa.TEXT(),
               type_=sa.String(length=20),
               existing_nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.TEXT(),
               type_=sa.String(length=20),
               existing_nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               type_=sa.String(length=1000),
               existing_nullable=True)
        batch_op.alter_column('season_id',
               existing_type=sa.TEXT(),
               type_=sa.Integer(),
               nullable=False)
        batch_op.drop_index('idx_16390_sqlite_autoindex_card_1')
        batch_op.create_unique_constraint(None, ['uuid'])
        batch_op.create_foreign_key(None, 'season', ['season_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('uuid',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               nullable=False)
        batch_op.alter_column('card_id',
               existing_type=sa.TEXT(),
               type_=sa.Integer(),
               nullable=False)
        batch_op.drop_index('idx_16400_sqlite_autoindex_comment_1')
        batch_op.create_unique_constraint(None, ['uuid'])
        batch_op.create_foreign_key(None, 'card', ['card_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('season', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('uuid',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.TEXT(),
               type_=sa.String(length=20),
               existing_nullable=True)
        batch_op.drop_index('idx_16395_sqlite_autoindex_season_1')
        batch_op.create_unique_constraint(None, ['uuid'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('season', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('idx_16395_sqlite_autoindex_season_1', ['uuid'], unique=True)
        batch_op.alter_column('name',
               existing_type=sa.String(length=20),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('uuid',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('idx_16400_sqlite_autoindex_comment_1', ['uuid'], unique=True)
        batch_op.alter_column('card_id',
               existing_type=sa.Integer(),
               type_=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               nullable=True)
        batch_op.alter_column('uuid',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('idx_16390_sqlite_autoindex_card_1', ['uuid'], unique=True)
        batch_op.alter_column('season_id',
               existing_type=sa.Integer(),
               type_=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.String(length=1000),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.String(length=20),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('category',
               existing_type=sa.String(length=20),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('img',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('uuid',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('auth_token', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('idx_16385_sqlite_autoindex_auth_token_1', ['token'], unique=True)
        batch_op.alter_column('user_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               nullable=True)
        batch_op.alter_column('token',
               existing_type=sa.String(length=255),
               type_=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###
