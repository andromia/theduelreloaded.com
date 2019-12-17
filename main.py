from app import create_app, db
from app.models import User, Post
import click

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post)