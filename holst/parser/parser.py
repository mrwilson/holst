import yaml
from holst.core import Host, Service, HostGroup

class UndefinedHostException(Exception):
  pass

class Parser():
  
  def __init__(self):
    self.hosts = dict()
    self.services = dict()
    self.hostgroups = dict()
    pass

  def parse(self, parse):
    obj = yaml.load(parse)
    for k,v in obj.iteritems():
      if v["type"] == "host":
        self.hosts[k] = Host(k, v)
      if v["type"] == "hostgroup":
        self.hostgroups[k] = HostGroup(k, v)
      else:
        self.services[k] = Service(k,v)

    for host in self.hosts.values():
      for service in host.get_services():
        self.validate_service(service)

    for hostgroup in self.hostgroups.values():
      self.validate_hostgroup(hostgroup)

  def validate_hostgroup(self, hostgroup):
    if hostgroup.name in hostgroup.hosts:
      raise UndefinedHostException("Hostgroup cannot contain itself")

    for host in hostgroup.hosts:
      if not host in self.hosts.keys():
        raise UndefinedHostException("Undefined host in hostgroup: %s" % host)

  def validate_service(self, service):
    service_name = service.keys()[0]
    hosts = service[service_name]

    if len(hosts) == 1 and hosts[0] == "all":
      return

    if not hosts <= self.hosts.keys():
      raise UndefinedHostException("Undefined host")

    if not service_name in self.services.keys():
      raise Exception("Undefined service - %s" % service_name)

  def get_chains(self, hostname):
    chains = []

    host = self.hosts.get(hostname)

    if len(host.services) == 1:
      service = host.services[0].keys()[0]
      return [self.services[service].get_chain()]

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
        groups = [item for name, item in self.hostgroups.iteritems() if name in hosts]

        for group in groups:
          service_hosts.extend([item for name, item in self.hosts.iteritems() if name in group.hosts])

      service_rules = self.services[service_name].create_rules(service_hosts)

      rules.append(service_rules)

    return rules
