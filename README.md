# For running a specific test with pytest and not capturing any print statements (i.e. be verbose)
```bash 
pytest -s test_all_scenarios.py::TestScenario22::test_shuffled_stuff
```

# How to execute the script
```bash
bash.py -t <training_directory> -l <lint_page>
OR
bash.py -l <lint_page> -r <relations_dump>
```

# How to train the linter
```python 
from main import RuleComposer
rule_composer_class = RuleComposer(threshold=1, 
                                   train_set='path/to/training/directory')
```

# If you want to train the linter and have * (any depth) relation when an x amount of distinct depths is encountered then use the parameter "star_depth_threshold" (default: None):
```python 
from main import RuleComposer
rule_composer_class = RuleComposer(threshold=1, 
                                   train_set='path/to/training/directory',
                                   star_depth_threshold=None)
```

# If you want the linter to be verbose while training then use the parameter "debug" (default: False):
```python 
from main import RuleComposer
rule_composer_class = RuleComposer(threshold=1, 
                                   train_set='path/to/training/directory',
                                   star_depth_threshold=None,
                                   debug=True)
```

# If you already have a json file with rules from a different training then import it with the parameter "json_rules_filename" (default: None):
```python 
from main import RuleComposer
rule_composer_class = RuleComposer(threshold=1, 
                                   train_set='path/to/training/directory',
                                   star_depth_threshold=None,
                                   debug=True,
                                   json_rules_filename=None)
```

# How to lint a page:
```python 
from main import RuleComposer
rule_composer_class = RuleComposer(threshold=1, 
                                   train_set='path/to/training/directory',
                                   star_depth_threshold=None,
                                   debug=True,
                                   json_rules_filename=None)
rule_composer_class.compare_test_page(test_page='path/to/test/page')
rule_composer_class.print_parent_level_errors()
```

# If you want to lint a page and only check for collocated class relations then use the parameter "allow_fine_grain_relations" (default: True)
```python 
from main import RuleComposer
rule_composer_class = RuleComposer(threshold=1, 
                                   train_set='path/to/training/directory',
                                   star_depth_threshold=None,
                                   debug=True,
                                   json_rules_filename=None)

rule_composer_class.compare_test_page(test_page='path/to/test/page',
                                      allow_fine_grain_relations=False)
rule_composer_class.print_parent_level_errors()
```

# If you want to considered untrain/unseen CSS classes then use the parameter "ignore_unseen_classes" (default: True)
```python 
from main import RuleComposer
rule_composer_class = RuleComposer(threshold=1, 
                                   train_set='path/to/training/directory',
                                   star_depth_threshold=None,
                                   debug=True,
                                   json_rules_filename=None)

rule_composer_class.compare_test_page(test_page='path/to/test/page',
                                      allow_fine_grain_relations=False,
                                      ignore_unseen_classes=False)
rule_composer_class.print_parent_level_errors()
```

# If you want to report errors regarding unseen classes as warnings, then use the parameter "include_warnings" (default: False)
```python 
from main import RuleComposer
rule_composer_class = RuleComposer(threshold=1, 
                                   train_set='path/to/training/directory',
                                   star_depth_threshold=None,
                                   debug=True,
                                   json_rules_filename=None)

rule_composer_class.compare_test_page(test_page='path/to/test/page',
                                      allow_fine_grain_relations=False,
                                      ignore_unseen_classes=True,
                                      include_warnings=True)
rule_composer_class.print_parent_level_errors()
```

# If you want to restrict the depth of the linter lookup during relations (i.e. how deep to look for violations, let us say 2) then you can use the parameter "depth_cap" (default: None)
```python 
from main import RuleComposer
rule_composer_class = RuleComposer(threshold=1, 
                                   train_set='path/to/training/directory',
                                   star_depth_threshold=None,
                                   debug=True,
                                   json_rules_filename=None)

rule_composer_class.compare_test_page(test_page='path/to/test/page',
                                      allow_fine_grain_relations=False,
                                      ignore_unseen_classes=True,
                                      include_warnings=True,
                                      depth_cap=2)
rule_composer_class.print_parent_level_errors()
```

# If you want to convert a CSS class (that has i.e. 3 relations with other classes) to a wildcard-class (can appear anywhere in the code) then use the parameter "relation_cap" (default: None)
```python 
from main import RuleComposer
rule_composer_class = RuleComposer(threshold=1, 
                                   train_set='path/to/training/directory',
                                   star_depth_threshold=None,
                                   debug=True,
                                   json_rules_filename=None)

rule_composer_class.compare_test_page(test_page='path/to/test/page',
                                      allow_fine_grain_relations=False,
                                      ignore_unseen_classes=True,
                                      include_warnings=True,
                                      depth_cap=2,
                                      relation_cap=3)
rule_composer_class.print_parent_level_errors()
```

#Termnal command for coverage report
```bash
coverage report -m TAG.py graph_base_case.py main.py > report4.txt
```
