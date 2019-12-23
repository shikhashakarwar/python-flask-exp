import mysql.connector
import click

from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(user="root",host="127.0.0.1", database="quiz_db")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db(): 
    db = get_db()
    
@click.command("init-db")
@with_appcontext
def init_db_command(): 
    init_db()
    click.echo("Initialize the database")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)