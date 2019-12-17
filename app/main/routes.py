import os

from flask import render_template, redirect, send_from_directory
from flask_login import current_user, login_required
from app import db
from app.models import Post
from app.main.forms import PostForm
from app.main import bp

from app.utils import url_for


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(url_for('static', filename='favicon.ico'),
        mimetype='image/vnd.microsoft.icon')

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    posts = Post.query.filter_by(project='TDR').order_by(Post.timestamp.desc())
    return render_template('index.html', title='The Duel Reloaded', posts=posts)
@bp.route('/staff_post', methods=['GET', 'POST'])

def staff_post():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    form = PostForm()
    if form.validate_on_submit():
        user = current_user
        is_dev = form.is_dev.data
        text = form.text.data
        project = form.project.data
        post = Post(is_dev=is_dev, text=text, project=project, user_id=user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('staff/post.html', title="Staff Post", form=form)