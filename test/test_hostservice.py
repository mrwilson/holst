import unittest
from nose.tools import raises
from nose.tools import istest as test
from holst.parser import Parser

class HostServiceTest(unittest.TestCase):

  @raises(Exception)
  @test
  def error_if_host_does_not_exist(self):
    parser = Parser()

    parser.parse("""
      example:
        type: host
    """)

    parser.get_rules_for("notexample")

  @test
  def list_of_rules_for_host_and_service(self):
    parser = Parser()

    parser.parse("""
      example:
        type: host
        services:
          - http
          - ssh

      http:
        type: service
        rules:
          - accept: ["tcp", 80]

      ssh:
        type: service
        rules:
          - accept: ["tcp", 22]
    """)

    rules = parser.get_rules_for("example")

    assert len(rules) == 2
