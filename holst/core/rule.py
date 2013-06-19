class Rule(object):

  def __init__(self, obj, service_name, hosts=None):
    operation, rule = obj.popitem()
    
    if len(rule) <= 1:
      raise Exception("No ports specified rule in %s" % service_name)

    self.operation = operation.upper()
    self.protocol = rule[0]
    self.ports = ",".join([str(x) for x in rule[1:]])
    self.hosts = hosts
    self.name = service_name

    if self.hosts == ["all"]:
      self.source = []
    else:
      self.source = [ip for host in hosts for ip in host.ip]
