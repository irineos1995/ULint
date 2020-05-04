from main import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", dest='train', help="training directory", action="store", default=None)
parser.add_argument("-l", dest='lint', help="page to be linted", action="store", default=None)
parser.add_argument("-r", dest='relations', help="json dump (rules) to be loaded", action="store", default=None)
parser.add_argument("-c", dest='depth_cap', type=int, help="depth cap for relative depth relations", action="store", default=None)
parser.add_argument("-d", dest='documentation', help="file to save the verbose rule documentation in (has to be .html file)", default=None)
args = parser.parse_args()

if args.train == "None":
    args.train = None

if args.lint == "None":
    args.lint = None

if args.relations == "None":
    args.relations = None

if args.depth_cap == "None":
    args.depth_cap = None

if args.documentation == "None":
    args.documentation = None

rule_composer_class = None
if args.train and args.lint:
    rule_composer_class = RuleComposer(threshold=0, train_set=args.train)
    rule_composer_class.compare_test_page(test_page=args.lint, depth_cap=args.depth_cap)
    rule_composer_class.print_parent_level_errors()
elif args.lint and args.relations:
    rule_composer_class = RuleComposer(threshold=0, train_set=None, json_rules_filename=args.relations)
    rule_composer_class.compare_test_page(test_page=args.lint, depth_cap=args.depth_cap)
    rule_composer_class.print_parent_level_errors()
else:
    print('cli.sh -t <training_directory> -l <lint_page> -r <relations_dump_file> -c <depth_cap> -d <html_file_to_save_documentation>')

if (args.train or args.relations) and args.documentation:
    if rule_composer_class:
        rule_composer_class.create_documentation(filename=args.documentation)
