class Rule():

  def __init__(self, obj):
    self.rule = "-A INPUT -p tcp -m tcp --dport 80 -j ACCEPT"

  def to_rule(self):
    return self.rule

class Service():

  def __init__(self, name, obj):
    r = Rule(obj)
    self.rules = [r]
