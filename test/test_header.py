from nose.tools import istest as test
from holst.parser import Parser

import unittest

class HeaderTest(unittest.TestCase):

  @test
  def test_header_contains_service_chains(self):
    parser = Parser()
    parser.parse("""
      example_service:
        type: service
        rules:
          accept: ["tcp", 80]

      example_host:
        type: host
        ip: [1.2.3.4]
        services:
          example_service: [all]
    """)

    header = parser.filter_header("example_host")
  
    assert ":example_service -" in header

  @test
  def render_ports_into_chains(self):
    parser = Parser()
    parser.parse("""
      example_service:
        type: service
        rules:
          - accept: ["tcp", 80]

      example_host:
        type: host
        ip: [1.2.3.4]
        services:
          example_service: [all]
    """)

    chains = parser.get_chains("example_host")

    assert len(chains) == 1
    assert "-A INPUT -p tcp -m tcp --dport 80 -m state --state NEW -j example_service" in chains
