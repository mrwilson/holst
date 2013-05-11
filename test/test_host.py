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

  def test_host_services(self):
    parser = Parser()
    out = parser.parse("""
      foo:
        type: host
        services:
          - service1
          - service2
    """)
    foo = out["hosts"]["foo"]
    assert len(foo.services) == 2
    assert "service1" in foo.services
    assert "service2" in foo.services

  def test_host_no_services(self):
    parser = Parser()
    out = parser.parse("""
      foo:
        type: host
    """)
    foo = out["hosts"]["foo"]
    assert len(foo.services) == 0
