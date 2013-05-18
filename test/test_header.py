from nose.tools import istest as test
from holst.parser import Parser

import unittest

class HeaderTest(unittest.TestCase):

  def test_header_contains_service_chains(self):
    parser = Parser()
    parser.parse("""
      example_service:
        type: service

      example_host:
        type: host
        ip: 1.2.3.4
        services:
          example_service: [all]
    """)

    header = parser.get_header("example_host")
  
    assert ":example_service -" in header
