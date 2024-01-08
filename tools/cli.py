import sys, os

sys.path.append(os.getcwd())  # Чтобы запускать скрипт локально, находясь в корневой директории проекта
import click
import contextlib
from contextlib import contextmanager
from sqlalchemy import text
from sqlalchemy.sql import text as sa_text
from shared.database.models import *
from shared.database import session, engine


@click.group()
def cli():
    pass


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    db_session = session()
    try:
        yield db_session
        db_session.commit()
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()


@cli.command()
def clear_db():
    """
    Clear all Tables
    """
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(Base.metadata.sorted_tables):
            con.execute(sa_text(f'TRUNCATE TABLE {table} CASCADE;'))
        trans.commit()


@cli.command()
def drop_db():
    """
    Delete all tables and drop alembic_version
    """
    Base.metadata.drop_all(engine)
    with session_scope() as session:
        query = text("DELETE FROM alembic_version;")
        session.execute(query)
        session.commit()


if __name__ == '__main__':
    cli()
