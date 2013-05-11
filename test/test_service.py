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
      foo:
        type: service
    """)
    assert len(out["services"]) == 1
    assert isinstance(out["services"]["foo"], Service)

  @raises(Exception)
  @test
  def parse_host_without_service(self):
    parser = Parser()

    out = parser.parse("""
      foo:
        type: host
        services:
          - notcreated
    """)
