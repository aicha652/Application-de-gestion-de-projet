from app.base.tools import (verify_pass, fail_response)
from flask import render_template, redirect, request, url_for, session
from app import login_manager
from app.base import blueprint
from pprint import pprint


@login_manager.unauthorized_handler
def unauthorized_handler():
    session['next_url'] = request.path
    if request.is_xhr:
        msg = 'Unautorized. Please login to access this route'
        return fail_response(403, msg)
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


@blueprint.app_errorhandler(413)
def access_forbidden(error):
    if request.is_xhr:
        return fail_response(413, error)
    else:
        pprint(request)
        return render_template('errors/page_403.html'), 403


@blueprint.app_errorhandler(400)
def access_forbidden(error):
    if request.is_xhr:
        return fail_response(400, error)


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
        return fail_response(500, msg)
    else:
        return render_template('errors/page_500.html'), 500