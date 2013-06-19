import unittest
from nose.tools import istest as test
from nose.tools import raises
from holst.parser import YAMLParser, UnknownTypeException

class YAMLParserTest(unittest.TestCase):

  @raises(IOError)
  @test
  def parserShouldExceptionOnFileNotExisting(self):
    parser = YAMLParser()
    parser.load("/")

  @test
  def loadOpensAndReadsFileCorrectly(self):
    parser = YAMLParser()
    parser.load("./resources/host.yaml")

  @raises(UnknownTypeException)
  @test
  def parseThrowsExceptionIfTypeIsUndefined(self):
    parser = YAMLParser()
    parser.obj = { "example_typeless": { "key" : "value" } }
    parser.parse()

  @test
  def parseCorrectlyIdentifiesHost(self):
    parser = YAMLParser()
    parser.obj = { "example_host": { "type": "host", "ip" : ["1.2.3.4"] } }
    parser.parse()

    assert "example_host" in parser.hosts.keys()

  @test
  def parseCorrectlyIdentifiesService(self):
    parser = YAMLParser()
    parser.obj = { "example_service": { "type": "service" } }
    parser.parse()

    assert "example_service" in parser.services.keys()

  @test
  def parseCorrectlyIdentifiesHostgroup(self):
    parser = YAMLParser()
    parser.obj = { "example_hostgroup": { "type": "hostgroup" } }
    parser.parse()

    assert "example_hostgroup" in parser.hostgroups.keys()

  @raises(UnknownTypeException)
  @test
  def parseThrowsExceptionOnUnexpectedType(self):
    parser = YAMLParser()
    parser.obj = { "example_unknown": { "type" : "unknown" } }
    parser.parse()
