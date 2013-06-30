import sys, argparse
from jinja2 import Environment, PackageLoader
from holst.parser import YAMLParser

def main():
  argparser = argparse.ArgumentParser(prog='holst', description='Transform DSL into iptables rule files.')
  argparser.add_argument('templatefile', help='template file to read data from')
  argparser.add_argument('hostname', help='name of host to generate files for')
  argparser.add_argument('--accept-established', help='accept established connections by default', action="store_true")
  argparser.add_argument('--nat-header', help='add default nat rules to the rule file', action="store_true")
  argparser.add_argument('--loopback', help='allow loopback on input/output', action="store_true")

  args = argparser.parse_args()
  process(args)

def process(args):
  templatefile = args.templatefile
  hostname = args.hostname

  parser = YAMLParser()
  parser.load(templatefile)
  parser.parse()

  opts = {  "nat": False,
              "chains" : [],
              "accept_established": False,
              "loopback": False,
              "incoming_rules": [],
              "outgoing_rules": [],
              "hosts": []
  }

  if args.accept_established:
    opts["accept_established"] = True

  if args.nat_header:
    opts["nat"] = True

  if args.loopback:
    opts["loopback"] = True

  opts["chains"] = parser.chains(hostname)

  opts["incoming_rules"] = parser.incoming_rules(hostname)
  opts["outgoing_rules"] = parser.outgoing_rules(hostname)
   
  print(render(opts))

def render(opts):
  env = Environment(loader=PackageLoader('holst', 'templates'), trim_blocks=True, lstrip_blocks=True)
  template = env.get_template("rules.tpl")
  return template.render(opts)
