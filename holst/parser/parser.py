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
      for service in host.services:
        self.validate_service(service)

    return { "hosts" : self.hosts, "services": self.services }


  def validate_service(self, service):
    if type(service) is dict:
      service_name = service.keys()[0];
      hosts = service[service_name]

      if len(hosts) == 1 and hosts[0] == "all":
        return

      if not hosts <= self.hosts.keys():
        raise Exception("Undefined host")

      if not service_name in self.services.keys():
        raise Exception("Undefined service")
      return

    if not service in self.services.keys():
      raise Exception("Undefined service")

  def get_header(self, hostname):
    header = ["*nat", ":PREROUTING ACCEPT", ":POSTROUTING ACCEPT", ":OUTPUT ACCEPT"]
    header.extend(["*filter", ":INPUT DROP", ":OUTPUT ACCEPT", ":FORWARD DROP"])

    host = self.hosts.get(hostname)

    if type(host.services) is dict:
      header.append(":%s -" % host.services.keys()[0])
      return header

    for service in host.services:
      header.append(":%s -" % service.keys()[0])

    return header

  def get_chains(self, hostname):
    chains = []

    host = self.hosts.get(hostname)

    if len(host.services) == 1:
      return self.services[host.services.keys()[0]].get_chain()

    for service_obj in host.services:
      service = service_obj.keys()[0]
      chains.extend(self.services[service].get_chain())

    return chains

  def get_rules_for(self,hostname):

    if (hostname not in self.hosts):
      raise Exception("Host not found")

    rules = []
    host = self.hosts.get(hostname)

    for service in host.services:
      service_name, hosts = service.popitem()

      if hosts == ["all"]:
        service_hosts = ["all"]
      else:
        service_hosts = [item for name,item in self.hosts.iteritems() if name in hosts]

      service_rules = self.services[service_name].create_rules(service_hosts)

      for rule in service_rules:
        rules.append(rule)

    return rules
