from main import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", dest='train', help="training directory", action="store")
parser.add_argument("-l", dest='lint', help="page to be linted", action="store")
parser.add_argument("-r", dest='relations', help="json dump (rules) to be loaded", action="store")
args = parser.parse_args()

if args.train and args.lint:
    print('Got here correctly!')
    rule_composer_class = RuleComposer(threshold=0, train_set=args.train)
    rule_composer_class.compare_test_page(test_page=args.lint)
    rule_composer_class.print_parent_level_errors()
elif args.lint and args.relations:
    rule_composer_class = RuleComposer(threshold=0, train_set=None, json_rules_filename=args.relation)
    rule_composer_class.compare_test_page(test_page=args.lint)
    rule_composer_class.print_parent_level_errors()
else:
    print('bash.py -t <training_directory> -l <lint_page>')
