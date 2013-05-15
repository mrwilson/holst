class Host():

  services = []
  
  def __init__(self, hostname, props):
    self.hostname = hostname

    if "ip" not in props.keys():
      raise Exception("No ip defined for host")

    self.ip = props["ip"]

    if "services" in props.keys():
      self.services = props["services"]
