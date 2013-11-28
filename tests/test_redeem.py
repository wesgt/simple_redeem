import unittest
from flask import json
import webapp
from webapp.redeem import ResultType, redeem


class IAPTestCase(unittest.TestCase):

    def setUp(self):
        app = webapp.create_app('config_testing.cfg')
        app.config['TESTING'] = True
        app.register_blueprint(redeem, url_prefix='/gogolook')
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
            '/gogolook/redeem_code',
            data=dict(email=email),
            follow_redirects=False)

        receive_result = json.loads(str(receive_rv.data, 'utf-8'))
        self.assertEqual(ResultType.RECEIVE_SUCCESS, receive_result['result'])

    def test_receive_redeem_code_return_email_error(self):
        email = 'wes'
        receive_rv = self.client.post(
            '/gogolook/redeem_code',
            data=dict(email=email),
            follow_redirects=False)

        receive_result = json.loads(str(receive_rv.data, 'utf-8'))
        self.assertEqual(ResultType.EMAIL_FAIL, receive_result['result'])

    def test_redeem_gift_return_correct(self):
        redeem_code = self._get_redeem_code('takachi@softstar.com.tw')
        self.assertEqual(ResultType.REDEEM_GIFT_SUCCESS,
                         self._redeem_gift('wes@softstar.com.tw', redeem_code))

    def test_redeem_gift_return_redeem_gift_count_fail(self):
        redeem_code_a = self._get_redeem_code('takachi_a@softstar.com.tw')
        redeem_code_b = self._get_redeem_code('takachi_b@softstar.com.tw')
        redeem_code_c = self._get_redeem_code('takachi_c@softstar.com.tw')
        redeem_code_d = self._get_redeem_code('takachi_d@softstar.com.tw')

        self.assertEqual(ResultType.REDEEM_GIFT_SUCCESS,
                         self._redeem_gift('wes@softstar.com.tw', redeem_code_a))
        self.assertEqual(ResultType.REDEEM_GIFT_SUCCESS,
                         self._redeem_gift('wes@softstar.com.tw', redeem_code_b))
        self.assertEqual(ResultType.REDEEM_GIFT_CONT_GREATER_THAN_THREE_FAIL,
                         self._redeem_gift('wes@softstar.com.tw', redeem_code_c))
        self.assertEqual(ResultType.REDEEM_GIFT_CONT_GREATER_THAN_THREE_FAIL,
                         self._redeem_gift('wes@softstar.com.tw', redeem_code_d))

    def test_redeem_gift_return_redeem_code_is_me_fail(self):
        redeem_code = self._get_redeem_code('wes@softstar.com.tw')
        self.assertEqual(ResultType.REDEEM_CODE_IS_ME_FAIL,
                         self._redeem_gift('wes@softstar.com.tw', redeem_code))

    def test_redeem_gift_return_redeem_code_duplicate_fail(self):
        self._get_redeem_code('wes2@softstar.com.tw')
        redeem_code_e = self._get_redeem_code('takachi_e@softstar.com.tw')

        self.assertEqual(ResultType.REDEEM_GIFT_SUCCESS,
                         self._redeem_gift('wes2@softstar.com.tw', redeem_code_e))
        self.assertEqual(ResultType.REDEEM_CODE_DUPLICATE_FAIL,
                         self._redeem_gift('wes2@softstar.com.tw', redeem_code_e))

    def _get_redeem_code(self, email):
        receive_a_rv = self.client.post(
            '/gogolook/redeem_code',
            data=dict(email=email),
            follow_redirects=False)

        receive_result = json.loads(str(receive_a_rv.data, 'utf-8'))
        return receive_result['redeem_code']

    def _redeem_gift(self, email, redeem_code):
        redeem_gift_rv = self.client.post(
            '/gogolook/redeem_gift',
            data=dict(email=email, redeem_code=redeem_code),
            follow_redirects=False)

        redeem_gift_result = json.loads(str(redeem_gift_rv.data, 'utf-8'))
        return redeem_gift_result['result']