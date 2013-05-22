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

  out = []

  templatefile = args.templatefile
  hostname = args.hostname

  try:
    with open(templatefile) as template_file:
      parser = Parser()
      parser.parse(template_file.read())

      print_list(parser.nat_header())
      print "COMMIT\n"

      print_list(parser.filter_header(hostname))

      if args.allow_established:
        print "-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT\n"

      print_list(parser.get_chains(hostname))
      print_list(parser.get_rules_for(hostname))
      print "COMMIT\n"
  except IOError:
    print 'Cannot access file: %s' % args.templatefile
    sys.exit(1)

def print_list(list_):
  print "\n".join(list_), "\n"
