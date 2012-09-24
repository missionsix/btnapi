#!/usr/bin/python
import btnapi
import unittest
import sys

from pprint import pprint

API_KEY = '71fa9e15febd904c64d1a6ba770a345a'

class TestAPIRequest(unittest.TestCase):

    def setUp(self):
        self.api = btnapi.BtnApi(API_KEY)

    def testBaseRequest(self):
        userinfo = self.api._BtnApi__request('userInfo')
        self.assertIsNotNone(userinfo)

    def testParamsRequest(self):
        torrents = self.api._BtnApi__request('getTorrentsSearch', 
                                     [{'series':'House', 'name': "S08E01"}, 2])
        self.assertIsNotNone(torrents)

    def testApiCallSimple(self):
        userinfo = self.api.userInfo()
        self.assertIsNotNone(userinfo)

    def testApiCallGet(self):
        tvnews = self.api.getTVNews([2])
        self.assertIsNotNone(tvnews)

    def testApiCallQuery(self):
        torrents = self.api.getTorrentSearch([{'series':'House', 'name': "S08E01"}, 2])
        self.assertIsNotNone(torrents)


if __name__ == '__main__':
    unittest.main()
