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

  @test
  def error_if_hostgroup_shares_name_with_host(self):
    pass

  @test
  def error_if_hostgroup_contains_itself(self):
    pass
