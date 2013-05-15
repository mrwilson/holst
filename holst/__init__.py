import sys
from holst.parser import Parser

def main():
  if len(sys.argv) != 3:
    print "Usage: holst <template-file> <host-name>"
    sys.exit(0)

  filename = sys.argv[1]
  hostname = sys.argv[2]

  rules = []

  try:
    with open(filename) as template_file:
      parser = Parser()
      parser.parse(template_file.read())
      rules = parser.get_rules_for(hostname)
  except IOError:
    print 'Cannot access file: %s' % filename
    sys.exit(1)

  for rule in rules:
    print rule
