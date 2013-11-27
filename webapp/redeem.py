__author__ = 'wes'

from flask import request, Blueprint, current_app, json, jsonify


redeem = Blueprint('redeem', __name__, template_folder='templates')


class ResultType:
    RECEIVE_SUCCESS = 'receive_success'
    EMAIL_FAIL = 'email_fail'


@redeem.route('/redeem_code', methods=['POST'])
def receive_redeem_code():
    """receive redeem_code

    same email have same redeem_code

    """

    from webapp.models import User

    email = request.form['email']

    if not _validate_email(email):
        return jsonify(result=ResultType.EMAIL_FAIL)

    user = User.query.filter(User.email == email).first()

    if user is None:
        user = User(email, _create_redeem_code(), 0)
        user.save()

    return jsonify(result=ResultType.RECEIVE_SUCCESS, redeem_code=user.redeem_code)


def _create_redeem_code():
    import uuid
    from webapp.models import User

    redeem_code = str(uuid.uuid4())[0:8]
    user = User.query.filter(User.redeem_code == redeem_code).first()

    if user is None:
        return redeem_code
    else:
        _create_redeem_code()


def _validate_email(email):
    import re

    mail_pattern = '^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$'
    if len(email) > 7:
        if re.match(mail_pattern, email) is not None:
            return True
    return False