# I would like to personally express my gratitute to Professor <a href="https://www.cs.york.ac.uk/people/dkolovos" target="_blank"><u><b>Dimitris Kolovos</b></u></a> and to Doctoral student <a href="https://smadani.github.io/" target="_blank"><u><b>Sina Madani</b></u></a> for all their help in this project!
<details>
<summary><a>Training & Linting through bash (CLI)</a></summary>

```bash
sh cli.sh -t <training_directory> -l <lint_page> -r <relations_dump_file> -c <depth_cap> -d <html_file_to_save_documentation>
```
</details>

<details>
<summary><a>Loading dumped rules & Linting through bash (CLI)</a></summary>

```bash
sh cli.sh -l <lint_page> -r <relations_dump_file>
```
# Example
```bash
sh cli.sh -l 'scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html' -r 'exported_rules_files/rules.json'
```
</details>

<details>
<summary><a>Create an HTML documentation page with the rules constructed from the training pages</a></summary>

<a href="http://htmlpreview.github.io/?https://github.com/irineos1995/ULint/blob/master/documentation.html" target="_blank">Click here for a demo</a>

```bash
sh cli.sh -r <relations_dump_file> -d <html_file_to_save_documentation>
OR
sh cli.sh -t <training_directory>> -d <html_file_to_save_documentation>
```

# Example
```bash
sh cli.sh -r 'exported_rules_files/rules.json' -d 'documentation.html'
```
</details>

# If you are not using the shell script then load the Virtual Environment to have all the dependencies installed
```bash 
source venv/bin/activate
```

<details>
<summary><a>For running a specific test with pytest and not capturing any print statements (i.e. be verbose)</a></summary>

```bash
pytest -s test_all_scenarios.py::TestScenario22::test_shuffled_stuff
```
</details>

<details>
<summary><a>How to train the linter</a></summary>

```python 
from main import RuleComposer
rule_composer_class = RuleComposer(threshold=1, 
                                   train_set='path/to/training/directory')
```
</details>

<details>
<summary><a>If you want to train the linter and have * (any depth) relation when an x amount of distinct depths is encountered then use the parameter "star_depth_threshold" (default: None)</a></summary>

```python 
from main import RuleComposer
rule_composer_class = RuleComposer(threshold=1, 
                                   train_set='path/to/training/directory',
                                   star_depth_threshold=None)
```
</details>

<details>
<summary><a>If you want the linter to be verbose while training then use the parameter "debug" (default: False)</a></summary>

```python 
from main import RuleComposer
rule_composer_class = RuleComposer(threshold=1, 
                                   train_set='path/to/training/directory',
                                   star_depth_threshold=None,
                                   debug=True)
```
</details>

<details>
<summary><a>If you already have a json file with rules from a different training then import it with the parameter "json_rules_filename" (default: None)</a></summary>

```python 
from main import RuleComposer
rule_composer_class = RuleComposer(threshold=1, 
                                   train_set='path/to/training/directory',
                                   star_depth_threshold=None,
                                   debug=True,
                                   json_rules_filename=None)
```
</details>

<details>
<summary><a>How to lint a page</a></summary>

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
</details>

<details>
<summary><a>If you want to lint a page and only check for collocated class relations then use the parameter "allow_fine_grain_relations" (default: True)</a></summary>

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
</details>

<details>
<summary><a>If you want to considered untrain/unseen CSS classes then use the parameter "ignore_unseen_classes" (default: True)</a></summary>

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
</details>

<details>
<summary><a>If you want to report errors regarding unseen classes as warnings, then use the parameter "include_warnings" (default: False)</a></summary>

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
</details>

<details>
<summary><a>If you want to restrict the depth of the linter lookup during relations (i.e. how deep to look for violations, let us say 2) then you can use the parameter "depth_cap" (default: None)</a></summary>

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
</details>

<details>
<summary><a>If you want to convert a CSS class (that has i.e. 3 relations with other classes) to a wildcard-class (can appear anywhere in the code) then use the parameter "relation_cap" (default: None)</a></summary>

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
</details>
<script>
(function() {
  var links = document.getElementsByTagName('a');
  for (var i = 0; i < links.length; i++) {
    if (/^(https?:)?\/\//.test(links[i].getAttribute('href'))) {
      links[i].target = '_blank';
    }
  }
})();
</script>