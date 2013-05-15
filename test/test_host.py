import unittest
from holst.core import Host
from holst.parser import Parser
from nose.tools import istest as test

class HostTest(unittest.TestCase):
 
  @test
  def get_host(self):
    parser = Parser()
    out = parser.parse("""
      foo:
        type: host
        ip: 1.2.3.4
    """)
    assert len(out["hosts"]) == 1
    assert "foo" in out["hosts"].keys()
  
  @test
  def no_host(self):
    parser = Parser()
    out = parser.parse("""
      foo:
        type: service      
    """) 
    assert len(out["hosts"]) == 0

  @test
  def host_no_services(self):
    parser = Parser()
    out = parser.parse("""
      foo:
        type: host
        ip: 1.2.3.4
    """)
    foo = out["hosts"]["foo"]
    assert len(foo.services) == 0
