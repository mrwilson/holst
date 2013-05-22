import unittest
from nose.tools import istest as test
from nose.tools import raises
from holst.parser import Parser

class HostGroupTest(unittest.TestCase):

  @test
  def parse_hostgroup(self):
    parser = Parser()

    parser.parse("""
      host1:
        type: host
        ip: [1.2.3.4]

      host2:
        type: host
        ip: [5.6.7.8]

      group:
        type: hostgroup
        hosts: [host1, host2]
    """)

    assert len(parser.hostgroups) == 1

  @raises(Exception)
  @test
  def error_if_host_in_hostgroup_does_not_exist(self):
    parser = Parser()
    parser.parse("""
      group:
        type: hostgroup
        hosts: [notexist]
    """)

  @raises(Exception)
  @test
  def error_if_hostgroup_contains_itself(self):
    parser = Parser()
    parser.parse("""
      example:
        type: hostgroup
        hosts: [example]
    """)

  @test
  def error_if_hostgroup_contains_itself(self):
    parser = Parser()
    parser.parse("""
      example1:
        type: host
        ip: [1.2.3.4]

      example2:
        type: host
        ip: [5.6.7.8]

      example:
        type: hostgroup
        hosts: [example1, example2]

      service:
        type: service
        rules:
          - accept: ["tcp", 80]

      output:
        type: host
        ip: [9.10.11.12]
        services:
          - service: [example]
    """)

    rules = parser.get_rules_for("output")[0]
    assert len(rules) == 2
