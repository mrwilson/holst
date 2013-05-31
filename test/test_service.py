import unittest
from nose.tools import istest as test
from nose.tools import raises
from holst.parser import Parser
from holst.core import Service

class ServiceTest(unittest.TestCase):

  @test
  def parse_service(self):
    parser = Parser()
    parser.parse("""
      example:
        type: service
    """)
    assert len(parser.services) == 1

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
