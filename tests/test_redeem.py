import unittest
from flask import json
import webapp
from webapp.redeem import ResultType, redeem
from webapp.database import db_session, drop_all_table


class IAPTestCase(unittest.TestCase):

    def setUp(self):
        app = webapp.create_app('config_testing.cfg')
        app.config['TESTING'] = True
        app.register_blueprint(redeem, url_prefix='/redeem')
        self.client = app.test_client()

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_receive_redeem_code_return_correct(self):
        email = 'wes@softstar.com.tw'
        receive_rv = self.client.post(
            '/redeem/redeem_code',
            data=dict(email=email),
            follow_redirects=False)

        receive_result = json.loads(str(receive_rv.data, 'utf-8'))
        self.assertEqual(ResultType.RECEIVE_SUCCESS, receive_result['result'])

    def test_receive_redeem_code_return_email_error(self):
        email = 'wes'
        receive_rv = self.client.post(
            '/redeem/redeem_code',
            data=dict(email=email),
            follow_redirects=False)

        receive_result = json.loads(str(receive_rv.data, 'utf-8'))
        self.assertEqual(ResultType.EMAIL_FAIL, receive_result['result'])
