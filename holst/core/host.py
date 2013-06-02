class MissingDataException(Exception):
  pass

class Host():

  services = []
  
  def __init__(self, hostname, props):
    self.hostname = hostname

    if "ip" not in props.keys():
      raise MissingDataException("No ip defined for host")

    self.ip = props["ip"]

    if "services" in props.keys():
      self.services = props["services"]

  def get_services(self):
    if type(self.services) is dict:
      return self.services.keys()
    else:
      return [service.keys()[0] for service in self.services]
