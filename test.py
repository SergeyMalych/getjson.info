#!/usr/bin/env python

"""Tests for the Flask Heroku template."""

import unittest
from app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home_page_works(self):
        rv = self.app.get('/')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)

    def test_ip(self):
        rv = self.app.get('/ip/')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)

    def test_specific_ip(self):
        rv = self.app.get('/ip/64.233.161.99')
        self.assertEqual(rv.status_code, 200)

    def test_specific_address(self):
        rv = self.app.get('/ip/google.com')
        self.assertEqual(rv.status_code, 200)

    def test_static_text_file_request(self):
        rv = self.app.get('/countries/')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)
        rv.close()


if __name__ == '__main__':
    unittest.main()