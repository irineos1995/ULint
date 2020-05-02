import unittest
import os,sys,inspect
from termcolor import colored, cprint
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import json
import filecmp

from main import *


class TestScenario1(unittest.TestCase):
    def test_identical_pages_threshold_1(self):
        rule_composer_class = RuleComposer(threshold=1, train_set='scenarios/scenario_1/train.html')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_1/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(len(errors), 0)

    def test_identical_pages_threshold_0(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_1/train.html')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_1/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(len(errors), 0)

class TestScenario2(unittest.TestCase):
    def test_nested_children(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_2/train.html')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_2/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [4])

class TestScenario3(unittest.TestCase):
    def test_threshold_matters_1(self):
        rule_composer_class = RuleComposer(threshold=0.6, train_set='scenarios/scenario_3/train.html')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_3/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [4])

class TestGraphPlot(unittest.TestCase):
    def test_plot_big_graph(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_5/big_training_data.html')
        graph = rule_composer_class.plot_directed_graph(filename='graph_files/big_graph.html')
        self.assertEqual(graph.num_nodes(), 88)

    def test_plot_small_graph(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_5/train.html')
        graph = rule_composer_class.plot_directed_graph(filename='graph_files/small_graph.html')
        self.assertEqual(graph.num_nodes(), 9)

class TestFineGraphPlot(unittest.TestCase):

    def test_plot_small_fine_graph_v2(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_4/train.html')
        graph = rule_composer_class.plot_fine_directed_graph_v2(filename='graph_files/small_fine_graph_v2.html')
        self.assertEqual(graph.num_nodes(), 7)

class TestScenario6(unittest.TestCase):
    def test_allow_fine_relations(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_6/train.html')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_6/test.html', allow_fine_grain_relations=True)

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

    def test_disable_fine_relations(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_6/train.html')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_6/test.html', allow_fine_grain_relations=False)

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [4])

class TestScenario7(unittest.TestCase):
    def test_allow_fine_relations(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_7/train.html')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_7/test.html', allow_fine_grain_relations=True)

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

    def test_disable_fine_relations(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_7/train.html')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_7/test.html', allow_fine_grain_relations=False)

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [4])

class TestScenario8(unittest.TestCase):
    def test_training_a_directory(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_8')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_8/test.html', allow_fine_grain_relations=True)

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

class TestScenario9(unittest.TestCase):
    def test_start_threshold_small(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_9/train.html', star_depth_threshold=3)
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_9/test.html', allow_fine_grain_relations=True)
        rule_composer_class.plot_fine_directed_graph_v2(filename='graph_files/small_fine_graph_v2_with_star.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

    def test_start_threshold_large(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_9/train.html', star_depth_threshold=1000)
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_9/test.html', allow_fine_grain_relations=True)

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [7])

class TestScenario11(unittest.TestCase):
    def test_with_trained_page(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_11/vanilla_bootstrap_train_pages/')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_11/test.htm', allow_fine_grain_relations=True)

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

    def test_with_unseen_page(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_11b/vanilla_bootstrap_train_pages/')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_11b/test.htm', allow_fine_grain_relations=True)

        errors = rule_composer_class.get_line_number_errors()
        expected_errors = [24,25,26,27,28,29,31,35,36,40,41,43,45,47,53,56,58,60,62,68,71,73,75,77,83,88,89,90,91,92,94,96,105,107,114,116]
        self.assertEqual(list(errors), expected_errors)

class TestScenario13(unittest.TestCase):
    def test_real_data_with_w3_rules(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3)
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html',
                                              allow_fine_grain_relations=True,
                                              ignore_unseen_classes=True,
                                              include_warnings=False
                                              )

        errors = rule_composer_class.get_line_number_errors()

        set_of_errors = set(errors)
        self.assertEqual(len(set_of_errors), 168)

class TestScenario15(unittest.TestCase):
    def test_depth_cap(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3)
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html',
                                              allow_fine_grain_relations=True,
                                              ignore_unseen_classes=True,
                                              include_warnings=False,
                                              depth_cap=1,
                                              parent_level_errors=True
                                              )

        rule_composer_class.print_parent_level_errors()
        errors = rule_composer_class.get_line_number_errors()

        set_of_errors = set(errors)
        print(set_of_errors)
        print(len(set_of_errors))
        cprint(rule_composer_class.depth_of_errors_report())

        self.assertFalse(365 in set_of_errors)

class TestScenario17(unittest.TestCase):
    def test_relation_cap(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3, debug=False)
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html',
                                              allow_fine_grain_relations=True,
                                              ignore_unseen_classes=True,
                                              include_warnings=False,
                                              depth_cap=None,
                                              parent_level_errors=True,
                                              relation_cap=2
                                              )

        rule_composer_class.print_parent_level_errors()
        errors = rule_composer_class.get_line_number_errors()

        set_of_errors = set(errors)
        print(set_of_errors)
        print(len(set_of_errors))
        cprint(rule_composer_class.depth_of_errors_report())

        self.assertFalse(508 in set_of_errors)


class TestScenario19(unittest.TestCase):
    def test_data_dump(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3, debug=True, max_training_pages=225)
        rule_composer_class.dump_rules(filename="rules.json")

        fine_relations = rule_composer_class.construct_fine_relations()
        with open('rules.json') as json_file:
            rules = json.load(json_file)
        self.assertEqual(fine_relations, rules)

    def test_data_load(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3, debug=False, max_training_pages=225, json_rules_filename="rules.json")
        rule_composer_class.compare_test_page(
            test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html',
            allow_fine_grain_relations=True,
            ignore_unseen_classes=True,
            include_warnings=False,
            depth_cap=1,
            parent_level_errors=True,
            relation_cap=10
            )

        errors = rule_composer_class.get_line_number_errors()

        rule_composer_class_2 = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3, debug=False, max_training_pages=225)
        rule_composer_class_2.compare_test_page(
            test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html',
            allow_fine_grain_relations=True,
            ignore_unseen_classes=True,
            include_warnings=False,
            depth_cap=1,
            parent_level_errors=True,
            relation_cap=10
        )

        errors_2 = rule_composer_class.get_line_number_errors()
        os.remove("rules.json")
        self.assertEqual(errors, errors_2)

class TestScenario20(unittest.TestCase):
    def test_proving_bootlint_wrong(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3, debug=True, max_training_pages=225, json_rules_filename="exported_rules_files/rules.json")
        # rule_composer_class.dump_rules(filename="rules.json")
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_13/test.html',
                                              allow_fine_grain_relations=True,
                                              ignore_unseen_classes=True,
                                              include_warnings=False,
                                              depth_cap=1,
                                              parent_level_errors=True,
                                              relation_cap=10
                                              )

        rule_composer_class.print_parent_level_errors()
        errors = rule_composer_class.get_line_number_errors()
        self.assertFalse(19 in errors)

class TestScenario22(unittest.TestCase):
    def test_UI(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3, debug=True, max_training_pages=225, json_rules_filename="rules.json")
        # rule_composer_class.dump_rules(filename="rules.json")
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html',
                                              allow_fine_grain_relations=True,
                                              ignore_unseen_classes=True,
                                              include_warnings=False,
                                              depth_cap=1,
                                              parent_level_errors=True,
                                              relation_cap=10
                                              )

        errors = rule_composer_class.print_parent_level_errors()
        rule_composer_class.present_errors(errors, rules_filename="rules.json", star_depth_threshold=3)

    def test_shuffled_stuff(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3, debug=False)
        rule_composer_class.compare_shuffled_test_page(test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html',
                                              allow_fine_grain_relations=True,
                                              ignore_unseen_classes=True,
                                              include_warnings=False,
                                              depth_cap=1,
                                              parent_level_errors=True,
                                              relation_cap=None
                                              )
        actual_file = 'scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html'
        shuffled_file = 'scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index_shuffled.html'
        self.assertFalse(filecmp.cmp(actual_file, shuffled_file))