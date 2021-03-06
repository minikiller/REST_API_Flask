import requests
import unittest
import json
import os
from database import create_database


class UserEndpointsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists('../../db/datashop.db'):
            os.system('rm ../../db/datashop.db')
        create_database('../../db/datashop.db')
        cls.uri = 'http://127.0.0.1:5000'

    def test_user_authorization(cls):
        cls.uri += '/auth'
        post_request = requests.post(cls.uri, data=json.dumps({'username': 'test_1', 'password': 'test_1@test.pl'}),
        headers={'Content-Type': 'application/json'})
        cls.assertIn('access_token', json.loads(post_request.content).keys())

    def test_users_status_code(cls):
        cls.uri += '/users'
        uri_request = requests.get(cls.uri)
        cls.assertEqual(200, uri_request.status_code)

    def test_register_new_user(cls):
        payload = {	'username': 'test_6',
	                'password': 'test_6@test.pl'}

        cls.uri += '/register'
        post = requests.post(cls.uri, json=payload)
        content_decode = json.loads(post.content.decode('utf-8'))
        cls.assertEqual('User successfully added to the database!',
                          content_decode.get('message'))

    def test_could_not_register_existing_user(cls):
        payload = {	'username': 'test_1',
	                'password': 'test_1@test.pl'}

        cls.uri += '/register'
        post = requests.post(cls.uri, json=payload)
        cls.assertEqual(400, post.status_code)


    def test_users_response_check(cls):
        cls.uri += '/users'
        uri_request = requests.get(cls.uri).content
        content_decode = json.loads(uri_request.decode('utf-8'))
        test_user = 1
        list_of_users = 0
        for user in content_decode.get('users'):
            cls.assertEqual('test_{}'.format(test_user),
            content_decode.get('users')[list_of_users].get('username'))
            test_user += 1
            list_of_users += 1

    @classmethod
    def tearDownClass(cls):
        os.system('rm ../../db/datashop.db')


if __name__ == '__main__':
    unittest.main(verbosity=2)
