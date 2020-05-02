from main import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", dest='train', help="training directory", action="store")
parser.add_argument("-l", dest='lint', help="page to be linted", action="store")
parser.add_argument("-r", dest='relations', help="json dump (rules) to be loaded", action="store")
parser.add_argument("-d", dest='documentation', help="file to save the verbose rule documentation in (has to be .html file)")
args = parser.parse_args()

rule_composer_class = None
if args.train and args.lint:
    rule_composer_class = RuleComposer(threshold=0, train_set=args.train)
    rule_composer_class.compare_test_page(test_page=args.lint)
    rule_composer_class.print_parent_level_errors()
elif args.lint and args.relations:
    rule_composer_class = RuleComposer(threshold=0, train_set=None, json_rules_filename=args.relation)
    rule_composer_class.compare_test_page(test_page=args.lint)
    rule_composer_class.print_parent_level_errors()

if (args.train or args.relations) and args.decumentation:
    if rule_composer_class:
        rule_composer_class.create_documentation(filename=args.documentation)

else:
    print('bash.py -t <training_directory> -l <lint_page>')
