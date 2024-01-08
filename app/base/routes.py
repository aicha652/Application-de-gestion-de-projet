# -*- encoding: utf-8 -*-

from flask import current_app, jsonify, render_template, redirect, request, url_for, abort
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from flask_restful import Resource
import datetime
from app import db, login_manager,api
from flask import current_app,session
from app.base import blueprint
from app.base.models import User

from app.base.tools import (verify_pass,
                            success_response,fail_response,
                            send_email)
import secrets


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.signin_view'))


@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))


@blueprint.before_app_request
def last_seen_updater():
    if current_user.is_authenticated:
        current_user.last_seen = db.func.now()
        db.session.commit()

############ Auth Views ################################


@blueprint.route('/signin', methods=['GET', 'POST'])
def signin_view():

    if not current_user.is_authenticated:
        return render_template('login/login-vs.html')
    elif current_user.is_admin:
        return redirect(url_for('home_blueprint.admin_dashboard'))
    elif not current_user.is_admin:
        return redirect(url_for('home_blueprint.index'))
    else:
        abort(500)


@blueprint.route('/auth/activateAccount/<token>')
def activate_account_view(token):
    user = User.query.filter_by(activation_token=token).first()

    if user is None or user.is_active:
        abort(404)
    else:
        user.is_active = True
        user.activation_token = None
        db.session.commit()
        login_user(user)

    return redirect(url_for('base_blueprint.signin_view'))


@blueprint.route('/auth/resetPassword/<token>')
def reset_password_view(token):
    user = User.query.filter_by(password_reset_token=token).first()
    if user is None:
        abort(404)
    elif user.password_reset_expires <= datetime.datetime.now():
        return render_template('token_expired.html')
    session['password_reset_token'] = token
    return render_template('login/reset_password.html')


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.signin_view'))

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    if request.is_xhr:
        msg = 'Unautorized. Please login to access this route'
        return fail_response(403,msg)
    else:
        return redirect(url_for('base_blueprint.signin_view'))
        ##### This throws a bug when logging out , must be checked later
        # return render_template('errors/page_403.html'), 403


@blueprint.app_errorhandler(403)
def access_forbidden(error):
    if request.is_xhr:
        return fail_response(403, error)
    else:
        return render_template('errors/page_403.html'), 403


@blueprint.app_errorhandler(404)
def not_found_error(error):
    if request.is_xhr:
        msg = 'This route doesnt exist or underconstruction'
        return fail_response(404, msg)
    else:
        return render_template('errors/page_404.html'), 404


@blueprint.app_errorhandler(500)
def internal_error(error):
    if request.is_xhr:
        msg = 'Internal Error. Please try again !'
        return fail_response(500,msg)
    else :
        return render_template('errors/page_500.html'), 500

