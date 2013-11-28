__author__ = 'wes'

from flask import request, Blueprint, current_app, json, jsonify


redeem = Blueprint('redeem', __name__, template_folder='templates')


class ResultType:
    RECEIVE_SUCCESS = 'receive_success'
    EMAIL_FAIL = 'email_fail'
    REDEEM_GIFT_SUCCESS = 'redeem_gift_success'
    EMAIL_NOT_RECEIVE_REDEEM_CODE_FAIL = 'email_not_receive_redeem_code_fail'
    REDEEM_GIFT_CONT_GREATER_THAN_THREE_FAIL = 'redeem_gift_count_greater_than_three_fail'
    REDEEM_CODE_FAIL = 'redeem_code_fail'
    REDEEM_CODE_DUPLICATE_FAIL = 'redeem_code_duplicate_fail'
    REDEEM_CODE_IS_ME_FAIL = 'redeem_code_is_me_fail'

@redeem.route('/redeem_code_test', methods=['GET'])
def receive_redeem_code_test():

    from webapp.models import User

    email = 'test@test.com.tw'

    user = User.query.filter(User.email == email).first()

    if user is None:
        user = User(email, _create_redeem_code(), 0)
        user.save()

    return jsonify(result=ResultType.RECEIVE_SUCCESS, redeem_code=user.redeem_code)

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

@redeem.route('/redeem_gift', methods=['POST'])
def redeem_gift():
    """redeem gift

    everyone can redeem gift count <= 3

    """

    from webapp.models import User, RedeemGift

    email = request.form['email']
    redeem_code = request.form['redeem_code']

    if not _validate_email(email):
        return jsonify(result=ResultType.EMAIL_FAIL)

    # check email receive redeem code
    user = User.query.filter(User.email == email).first()

    if user is None:
        return jsonify(result=ResultType.EMAIL_NOT_RECEIVE_REDEEM_CODE_FAIL)

    # check redeem code is me
    if user.redeem_code == redeem_code:
        return jsonify(result=ResultType.REDEEM_CODE_IS_ME_FAIL)

    # check redeem code exit
    user = User.query.filter(User.redeem_code == redeem_code).first()

    if user is None:
        return jsonify(result=ResultType.REDEEM_CODE_FAIL)

    # check redeem count <= 3
    redeem_gifts = RedeemGift.query.filter(RedeemGift.email == email).all()
    if redeem_gifts and len(redeem_gifts) >= 3:
        return jsonify(result=ResultType.REDEEM_GIFT_CONT_GREATER_THAN_THREE_FAIL)

    # check redeem code duplicate
    for redeem_gift_data in redeem_gifts:
        if redeem_gift_data.redeem_code == redeem_code:
            return jsonify(result=ResultType.REDEEM_CODE_DUPLICATE_FAIL)

    redeem_gifts = RedeemGift(email, redeem_code)
    redeem_gifts.save()

    return jsonify(result=ResultType.REDEEM_GIFT_SUCCESS)