class Rule(object):

  def __init__(self, obj, hosts=None):
    self.operation, rule = obj.popitem()
    self.protocol = rule[0]
    self.dport = rule[1:]
    self.hosts = hosts

  def get_rules(self):
    rules = []

    if len(self.dport) > 1:
      matcher = "-m multiport --dports %s" % ",".join(map(str, self.dport))
    else:
      matcher = "-m %s --dport %d" % (self.protocol, self.dport[0])

    if self.hosts:
      for host in self.hosts:
        if type(host.ip) is list:
          for ip in host.ip:
            rules.append("-A INPUT -s %s -p %s %s -j %s" % (ip, self.protocol, matcher, self.operation.upper()))
        else:
            rules.append("-A INPUT -s %s -p %s %s -j %s" % (host.ip, self.protocol, matcher, self.operation.upper()))
    else:
      rules.append("-A INPUT -p %s %s -j %s" % (self.protocol, matcher, self.operation.upper()))

    return rules
