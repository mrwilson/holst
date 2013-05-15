class Rule(object):

  def __init__(self, obj):
    self.operation, rule = obj.popitem()
    self.protocol = rule[0]
    self.dport = rule[1]

  def to_rule(self):
    return "-A INPUT -p %s -m %s --dport %d -j %s" % (self.protocol, self.protocol, self.dport, self.operation.upper())

  def __hash__(self):
    return hash(self.dport)

  def __eq__(self,other):
    return self.dport == other.dport
