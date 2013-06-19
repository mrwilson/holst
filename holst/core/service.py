from rule import Rule

class Service():
  def __init__(self, name, service):
    self.rules = []
    self.name = name

    if "rules" in service:
      if type(service["rules"]) is dict:
        self.rule_template = [service["rules"]]
      else:
        self.rule_template = service["rules"]

  def create_rules(self, chain_name, hosts=None):

    for rule in self.rule_template:
      self.rules.append(Rule(rule, chain_name, hosts))

    return self.rules
