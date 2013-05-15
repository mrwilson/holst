class Host():
  
  def __init__(self, hostname, props):
    self.hostname = hostname
    if "services" in props.keys():
      self.services = props["services"]
    else:
      self.services = []
