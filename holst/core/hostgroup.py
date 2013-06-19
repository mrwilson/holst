class HostGroup():

  def __init__(self, name, obj):
    self.name = name

    if "hosts" in obj.keys():
      self.hosts = obj["hosts"]
    else:
      self.hosts = []
