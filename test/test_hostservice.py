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
        ip: [1.2.3.4]
        type: host
        services:
          - http: [all]
          - ssh: [all]

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

  @test
  def define_service_only_from_certain_hosts_multiple_ips(self):
    parser = Parser()

    parser.parse("""
      source:
        type: host
        ip: [1.2.3.4, 5.6.7.8]

      example:
        type: host
        ip: [9.10.11.12]
        services:
          - ssh: [source]

      ssh:
        type: service
        rules:
          - accept: ["tcp", 22]
    """)

    rules = parser.get_rules_for("example")[0]
    assert len(rules) == 2

  @test
  def define_service_multiple_ports(self):
    parser = Parser()
                                                               
    parser.parse("""
      source:
        type: host
        ip: [1.2.3.4]
                                                               
      example:
        type: host
        ip: [9.10.11.12]
        services:
          - ssh: [source]
                                                               
      ssh:
        type: service
        rules:
          - accept: ["tcp", 22, 23, 24]
    """)
                                                               
    rules = parser.get_rules_for("example")
    assert len(rules) == 1
    assert "-A ssh -s 1.2.3.4 -j ACCEPT" in rules[0]
