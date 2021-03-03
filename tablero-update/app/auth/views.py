from flask import render_template, url_for, redirect, request, flash, jsonify, abort, make_response
from flask_login import login_required, login_user, current_user, logout_user

from . import auth
from .forms import LoginForm
from ..models import User

from flask import session


@auth.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        remember = True if form.remember_me.data else False

        user =  User(email = form.email.data, password= form.password.data)

        if not user.check_password():
            flash('Please check your login-password details and try again.')
            return jsonify({'Error':'Usuario Incorrecto'})

        login_user(user, remember=remember)

        session['username'] = current_user._id

        return  redirect(url_for('main.home'))

    return render_template('login.html', form = form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))


@auth.before_app_request
def before_request():
    if not current_user.is_authenticated and request.endpoint[:5] != 'auth.':
        return jsonify({'mensaje':'Logeate'})
