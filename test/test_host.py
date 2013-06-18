import unittest
from holst.core import Host, MissingDataException
from holst.parser import Parser
from nose.tools import istest as test
from nose.tools import raises

class HostTest(unittest.TestCase):
 
  @test
  def get_host(self):
    parser = Parser()
    parser.parse("""
      example:
        type: host
        ip: 1.2.3.4
    """)
    assert len(parser.hosts) == 1
    assert "example" in parser.hosts.keys()
  
  @test
  def no_host(self):
    parser = Parser()
    parser.parse("""
      example:
        type: service      
    """) 
    assert len(parser.hosts) == 0

  @test
  def host_no_services(self):
    parser = Parser()
    parser.parse("""
      example:
        type: host
        ip: 1.2.3.4
    """)
    example = parser.hosts["example"]
    assert len(example.services) == 0

  @raises(MissingDataException)
  @test
  def error_if_no_ip(self):
    parser = Parser()
    out = parser.parse("""
      example:
        type: host
    """)

  @test
  def define_services_from_host(self):
    parser = Parser()
    parser.parse("""
      example:
        type: host
        ip: [1.2.3.4]
        services:
          example_service: [all]

      example_service:
        type: service
    """)

    assert "example_service" in parser.hosts.get("example").get_service_names()
