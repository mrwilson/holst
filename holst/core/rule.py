class Rule(object):

  def __init__(self, obj, service_name, hosts=None):
    self.operation, rule = obj.popitem()
    self.dport = rule[1:]
    self.hosts = hosts
    self.name = service_name

  def get_rules(self):

    print self.hosts

    if self.hosts == ["all"]:
      return ["-A %s -j %s" % (self.name, self.operation.upper())]

    rules = []

    for host in self.hosts:
      for ip in host.ip:
        rules.append("-A %s -s %s -j %s" % (self.name, ip, self.operation.upper()))

    return rules
