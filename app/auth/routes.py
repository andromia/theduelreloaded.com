from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, ResetPasswordForm, CreateUserForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

def handle_reset_password(user, form):
    if user.check_password(form.password.data):
        user.set_password(form.new_password.data)
        db.session.add(user)
        db.session.commit()
        flash('Password has been updated!')
        return True
    flash('Current password is incorrect.')
    return False

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = current_user
        if handle_reset_password(user, form): return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', title='Reset Password', form=form)

@bp.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if not current_user.is_owner:
        flash('This feature is only available to owners!')
        return redirect(url_for('auth.login'))
    form = CreateUserForm()
    if form.validate_on_submit():
        exists = db.session.query(User.id)\
            .filter_by(username=form.username.data).scalar() is not None
        if not exists:
            user = User(username=form.username.data, is_admin=form.is_admin.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        flash('Username %s already exists.' % form.username.data)
    return render_template('auth/create_user.html', title='Create User', form=form)