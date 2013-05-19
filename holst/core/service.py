from rule import Rule

class Service():
  def __init__(self, name, service):
    self.rules = set()
    self.name = name

    if "rules" in service:
      self.rule_template = service["rules"]

  def create_rules(self, hosts=None):

    print self.rule_template  

    for rule in self.rule_template:
      self.rules |= set(Rule(rule, self.name, hosts).get_rules())

    return self.rules
