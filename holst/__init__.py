import sys, argparse
from jinja2 import Environment, PackageLoader
from holst.parser import Parser

def main():
  argparser = argparse.ArgumentParser(prog='holst', description='Transform DSL into iptables rule files.')
  argparser.add_argument('templatefile', help='template file to read data from')
  argparser.add_argument('hostname', help='name of host to generate files for')
  argparser.add_argument('--allow-established', help='accept established connections by default', action="store_true")
  argparser.add_argument('--nat-header', help='add default nat rules to the rule file', action="store_true")

  args = argparser.parse_args()
  process(args)

def process(args):
  templatefile = args.templatefile
  hostname = args.hostname

  parser = Parser()

  with open(templatefile) as template_file:
    parser.parse(template_file.read())

    opts = {  "nat": False,
                "chains" : [],
                "accept_established": False,
                "rules": [],
                "hosts": []
    }

    if args.allow_established:
      opts["accept_established"] = True

    if args.nat_header:
      opts["nat"] = True

    opts["chains"] = parser.hosts[hostname].get_service_names()

    print render(opts)

def render(opts):
  env = Environment(loader=PackageLoader('holst', 'templates'), trim_blocks=True, lstrip_blocks=True)
  template = env.get_template("rules.tpl")
  return template.render(opts)
