class MissingDataException(Exception):
  pass

class Host():

  services_outgoing = []
  services_incoming = []
  
  def __init__(self, hostname, props):
    self.hostname = hostname

    if "ip" not in props.keys():
      raise MissingDataException("No ip defined for host")

    self.ip = props["ip"]

    if "output" in props.keys():
      if type(props["output"]) is dict:
        self.services_outgoing = [props["output"]]
      else:
        self.services_outgoing = props["output"]

    if "input" in props.keys():
      if type(props["input"]) is dict:
        self.services_incoming = [props["input"]]
      else:
        self.services_incoming = props["input"]

  def get_services(self):
    return self.services_outgoing + self.services_incoming

  def incoming_service_names(self):
    return ["%s_in" % service.keys()[0] for service in self.services_incoming]

  def get_service_names(self):
    return self.outgoing_service_names() + self.incoming_service_names()

  def outgoing_service_names(self):
    return ["%s_out" % service.keys()[0] for service in self.services_outgoing]
