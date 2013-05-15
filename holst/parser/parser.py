import yaml
from holst.core import Host, Service

class Parser():
  
  def __init__(self):
    self.hosts = dict()
    self.services = dict()
    pass

  def parse(self, parse):
    obj = yaml.load(parse)
    for k,v in obj.iteritems():
      if v["type"] == "host":
        self.hosts[k] = Host(k, v)
      else:
        self.services[k] = Service(k,v)

    for hostname, host in self.hosts.iteritems():
      if len([x for x in host.services if x not in self.services.keys()]) > 0:
        raise Exception("Undefined services")

    return { "hosts" : self.hosts, "services": self.services }

  def get_rules_for(self,hostname):

    if (hostname not in self.hosts):
      raise Exception("Host not found")

    rules = []
    host = self.hosts[hostname]

    for service in host.services:
      for rule in self.services[service].rules:
        rules.append(rule.to_rule())

    return rules
