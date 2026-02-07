import logging
import sys
from pathlib import Path

# Add parent dir (app root) to path so config/models are importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine

from config import Config
from models import Base

# Import all models so Base.metadata has all tables
from models import AllowedUser, AuthToken, Card, Season, Comment, Order  # noqa: F401

config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

# Sync URL for migrations (psycopg2)
url = Config.SQLALCHEMY_DATABASE_URI
config.set_main_option("sqlalchemy.url", url)
target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(url)

    def process_revision_directives(context, revision, directives):
        if getattr(getattr(config, "cmd_opts", None), "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
