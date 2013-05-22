import sys
import argparse
from holst.parser import Parser

def main():
  argparser = argparse.ArgumentParser(prog='holst', description='Transform DSL into iptables rule files.')
  argparser.add_argument('templatefile', help='template file to read data from')
  argparser.add_argument('hostname', help='name of host to generate files for')
  argparser.add_argument('--allow-established', help='accept established connections by default', action="store_true")

  args = argparser.parse_args()
  process(args)

def process(args):
  templatefile = args.templatefile
  hostname = args.hostname

  parser = Parser()

  try:
    with open(templatefile) as template_file:
      parser.parse(template_file.read())

      for line in parser.nat_header():
        print line

      print "\nCOMMIT\n"

      for header in parser.filter_header(hostname):
        for rule in header:
          print rule
        print ""

      if args.allow_established:
        print "-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT"
        print ""

      for chain in parser.get_chains(hostname):
        print chain

      print ""

      for ruleset in parser.get_rules_for(hostname):
        for rule in ruleset:
          print rule
        print ""

      print "COMMIT"
  except IOError:
    print 'Cannot access file: %s' % args.templatefile
    sys.exit(1)

