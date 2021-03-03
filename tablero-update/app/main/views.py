from flask import render_template, flash, url_for, redirect, abort, jsonify, request, make_response
from flask_login import login_required, current_user, login_user

from . import main

@main.route('/home',methods = ['GET','POST'])
def home():
    if current_user.is_anonymous:
        abort(404)

    id_user = request.cookies.get('userID')

    print(id_user)

    return render_template('base.html', user = current_user)

@main.route('/another', methods = ['GET', 'POST'])
@login_required
def another():
    return jsonify({'mensaje':'esta es otra direccion'})