# noinspection PyUnresolvedReferences
import unittest
# noinspection PyUnresolvedReferences
import sys
sys.path.insert(1, '../src')
# noinspection PyUnresolvedReferences
from GsmHttpConnection import GsmHttpConnection


class GPSTest(unittest.TestCase):

    def test_build_without_slash(self):
        http = GsmHttpConnection("test.com", "path", "resource.html")
        self.assertEqual(http.build(), "GET /path/resource.html HTTP/1.1\r\nHost: test.com\r\n\r\n")

    def test_build_with_slash(self):
        http = GsmHttpConnection("test.com", "/path", "/resource.html")
        self.assertEqual(http.build(), "GET /path/resource.html HTTP/1.1\r\nHost: test.com\r\n\r\n")

    def test_build_with_one_slash(self):
        http = GsmHttpConnection("test.com", "/path", "resource.html")
        self.assertEqual(http.build(), "GET /path/resource.html HTTP/1.1\r\nHost: test.com\r\n\r\n")

unittest.main()
