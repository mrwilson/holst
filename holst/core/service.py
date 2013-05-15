from rule import Rule

class Service():

  def __init__(self, name, service):
    self.rules = set()

    if "rules" in service:
      self.setup_rules(service["rules"])

  def setup_rules(self, rules):
      for rule in rules:
        self.rules.add(Rule(rule))
