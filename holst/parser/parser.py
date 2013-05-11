import yaml
from holst.core import Host, Service

class Parser():
  
  def __init__(self):
    pass

  def parse(self, parse):
    obj = yaml.load(parse)
    ret = { "hosts" : {}, "services" : {} }
    services = []
    for k,v in obj.iteritems():
      if v["type"] == "host":
        ret["hosts"][k] = Host(k, v)
      else:
        ret["services"][k] = Service(k,v)
        services.append(k)

    for hostname, obj in ret["hosts"].iteritems():
      if len([x for x in obj.services if x not in services]) > 0:
        raise Exception("Undefined services")

    return ret
