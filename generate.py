import yaml
from jinja2 import Environment, FileSystemLoader
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--type", required=False, help="type of resume")
parser.add_argument("-o", "--outfile", required=True, help="output file name")
parser.add_argument("-j", "--template", required=True, help="jinja template")
args = parser.parse_args()

with open("resume.yaml", "r") as fin:
    resume = yaml.safe_load(fin)

# style.css which we will embed in the html directly
# to avoid requiring the stylesheet separately
with open("style.css") as fin:
    style = fin.read()
resume["style"] = style

# This modification is to make sure the syntax
# plays well with latex templates
env = Environment(
    block_start_string="\BLOCK{",
    block_end_string="}",
    variable_start_string="\VAR{",
    variable_end_string="}",
    comment_start_string="\#{",
    comment_end_string="}",
    line_statement_prefix="%%",
    line_comment_prefix="%#",
    trim_blocks=True,
    autoescape=False,
    loader=FileSystemLoader("./templates"),
)

template = env.get_template(args.template)
with open(args.outfile, "w") as fout:
    fout.write(template.render(resume=resume))
