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

    def test_build_with_empty_path(self):
        http = GsmHttpConnection("test.com", "", "resource.html")
        self.assertEqual(http.build(), "GET /resource.html HTTP/1.1\r\nHost: test.com\r\n\r\n")

    def test_build_with_body_inserts_content_length(self):
        http = GsmHttpConnection("test.com", "", "resource.html")
        http.set_body('TEST')
        self.assertEqual(http.build(), "GET /resource.html HTTP/1.1\r\nHost: test.com\r\nContent-Length: 4\r\n\r\nTEST")

unittest.main()
