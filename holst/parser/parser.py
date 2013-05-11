import yaml
from holst.core import Host

class Parser():
  
  def __init__(self):
    pass

  def parse(self, parse):
    obj = yaml.load(parse)
    ret = { "hosts" : {} }

    for k,v in obj.iteritems():
      if v["type"] == "host":
        ret["hosts"][k] = Host(k)

    return ret
