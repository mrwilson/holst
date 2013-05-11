import unittest
from holst.core import Host
from holst.parser import Parser

class HostTest(unittest.TestCase):
 
  def test_get_host(self):
    parser = Parser()
    out = parser.parse("""
      foo:
        type: host
    """)
    assert len(out["hosts"]) == 1
    assert "foo" in out["hosts"].keys()
  
  def test_no_host(self):
    parser = Parser()
    out = parser.parse("""
      foo:
        type: service      
    """) 
    assert len(out["hosts"]) == 0
