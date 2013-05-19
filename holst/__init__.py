import sys
from holst.parser import Parser

def main():
  if len(sys.argv) != 3:
    print "Usage: holst <template-file> <host-name>"
    sys.exit(0)

  filename = sys.argv[1]
  hostname = sys.argv[2]

  out = []

  try:
    with open(filename) as template_file:
      parser = Parser()

      parser.parse(template_file.read())

      out.extend(parser.get_header(hostname))
      out.extend(parser.get_chains(hostname))
      out.extend(parser.get_rules_for(hostname))
  except IOError:
    print 'Cannot access file: %s' % filename
    sys.exit(1)

  for line in out:
    print line
