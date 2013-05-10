import unittest
from holst.core import Host
from holst.parser import Parser

class HostTest(unittest.TestCase):
  
  def test_get_host(self):
    parser = Parser()
    host = parser.parse("""
      foo:
        type: host
    """)
    assert host.hostname == "foo"

