import yaml
from holst.core import Host, Service, HostGroup

class UndefinedHostException(Exception):
  pass

class YAMLParser():
  
  def __init__(self):
    self.hosts = dict()
    self.services = dict()
    self.hostgroups = dict()
    pass

  def load(self, yamlfile):
    with open(yamlfile) as template_file:
      self.obj = yaml.load(template_file.read()) 

  def parse(self):
    for k,v in self.obj.iteritems():
      if v["type"] == "host":
        self.hosts[k] = Host(k, v)
      elif v["type"] == "hostgroup":
        self.hostgroups[k] = HostGroup(k, v)
      else:
        self.services[k] = Service(k,v)

    self.validate()

  def validate(self):
    for host in self.hosts.values():
      for service in host.get_services():
        self._validate_service(service)

    for hostgroup in self.hostgroups.values():
      self._validate_hostgroup(hostgroup)

  def _validate_hostgroup(self, hostgroup):
    if hostgroup.name in hostgroup.hosts:
      raise UndefinedHostException("Hostgroup cannot contain itself")

    for host in hostgroup.hosts:
      if not host in self.hosts.keys():
        raise UndefinedHostException("Undefined host in hostgroup: %s" % host)

  def _validate_service(self, service):
    service_name = service.keys()[0]
    hosts = service[service_name]

    if len(hosts) == 1 and hosts[0] == "all":
      return

    if not hosts <= self.hosts.keys():
      raise UndefinedHostException("Undefined host")

    if not service_name in self.services.keys():
      raise Exception("Undefined service - %s" % service_name)

  def chains(self, hostname):
    return self.hosts.get(hostname).get_service_names()

  def incoming_rules(self, hostname):
    if (hostname not in self.hosts):
      raise Exception("Host not found")
                                    
    return self._rules(self.hosts.get(hostname).services_incoming, "in")

  def outgoing_rules(self, hostname):
    if (hostname not in self.hosts):
      raise Exception("Host not found")
                                    
    return self._rules(self.hosts.get(hostname).services_outgoing, "out")

  def _rules(self,services, origin):
    
    rules = []

    for service in services:
      service_name, hosts = service.popitem()

      chain_name = "%s_%s" % (service_name, origin)

      if hosts == ["all"]:
        service_hosts = ["all"]
      else:
        service_hosts = [item for name,item in self.hosts.iteritems() if name in hosts]
        groups = [item for name, item in self.hostgroups.iteritems() if name in hosts]

        for group in groups:
          service_hosts.extend([item for name, item in self.hosts.iteritems() if name in group.hosts])

      service_rules = self.services[service_name].create_rules(chain_name, service_hosts)

      rules.extend(service_rules)

    return rules
