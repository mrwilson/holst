import unittest
from nose.tools import istest as test
from nose.tools import raises
from holst.parser import Parser
from holst.core import Service

class ServiceTest(unittest.TestCase):

  @test
  def parse_service(self):
    parser = Parser()

    out = parser.parse("""
      example:
        type: service
    """)
    assert len(out["services"]) == 1
    assert isinstance(out["services"]["example"], Service)

  @raises(Exception)
  @test
  def parse_host_without_service(self):
    parser = Parser()

    out = parser.parse("""
      example:
        type: host
        services:
          - notcreated
    """)

  @test
  def parse_rule(self):
    parser = Parser()

    out = parser.parse("""
      example:
        type: service
        rule:
          accept: ["tcp", 80]
    """)

    example_service = out["services"]["example"]
    assert len(example_service.rules) == 1
    assert example_service.rules[0].to_rule() == "-A INPUT -p tcp -m tcp --dport 80 -j ACCEPT"
    
