import click

from service.db.factories import create_db_tables, create_db_engine


@click.group()
def db():
    pass


@db.command()
def create_tables():
    create_db_tables(engine=create_db_engine())


if __name__ == '__main__':
    db()
