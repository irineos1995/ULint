import unittest
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from main import *


class TestScenario1(unittest.TestCase):
    def test_identical_pages_threshold_1(self):
        rule_composer_class = RuleComposer(threshold=1, train_set='scenario_1/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_1/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(len(errors), 0)

    def test_identical_pages_threshold_0(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenario_1/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_1/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(len(errors), 0)

class TestScenario2(unittest.TestCase):
    def test_nested_children_permissively(self):
        rule_composer_class = RuleComposer(threshold=1, train_set='scenario_2/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_2/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

    def test_nested_children_not_permissively(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenario_2/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_2/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [4])

class TestScenario3(unittest.TestCase):
    def test_threshold_matters_1(self):
        rule_composer_class = RuleComposer(threshold=0.6, train_set='scenario_3/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_3/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [4])

class TestScenario4(unittest.TestCase):
    def test_threshold_matters_2(self):
        rule_composer_class = RuleComposer(threshold=0.6, train_set='scenario_4/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_4/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [4])

    def test_threshold_matters_3(self):
        rule_composer_class = RuleComposer(threshold=1, train_set='scenario_4/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_4/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

class TestScenario5(unittest.TestCase):
    def test_threshold_matters_4(self):
        rule_composer_class = RuleComposer(threshold=0.6, train_set='scenario_5/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_5/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

    def test_threshold_matters_5(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenario_5/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_5/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [5])

class TestGraphPlot(unittest.TestCase):
    def test_plot_big_graph(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenario_5/big_training_data.html')
        rule_composer_class.plot_directed_graph(filename='graph_files/big_graph.html')

    def test_plot_small_graph(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenario_5/train.html')
        rule_composer_class.plot_directed_graph(filename='graph_files/small_graph.html')

class TestFineGraphPlot(unittest.TestCase):

    def test_plot_small_fine_graph(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenario_4/train.html')
        # rule_composer_class.plot_fine_directed_graph(filename='small_fine_graph.html')
        # rule_composer_class.construct_fine_relations()

    def test_plot_small_fine_graph_v2(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenario_4/train.html')
        rule_composer_class.plot_fine_directed_graph_v2(filename='graph_files/small_fine_graph_v2.html')

class TestScenario6(unittest.TestCase):
    def test_allow_fine_relations(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenario_6/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_6/test.html', allow_fine_grain_relations=True)

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

    def test_disable_fine_relations(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenario_6/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_6/test.html', allow_fine_grain_relations=False)

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [4])

class TestScenario7(unittest.TestCase):
    def test_allow_fine_relations(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenario_7/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_7/test.html', allow_fine_grain_relations=True)

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

    def test_disable_fine_relations(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenario_7/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_7/test.html', allow_fine_grain_relations=False)

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [4])

class TestScenario8(unittest.TestCase):
    def test_training_a_directory(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenario_8')
        rule_composer_class.compare_test_page(test_page='scenario_8/test.html', allow_fine_grain_relations=True)

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

class TestScenario9(unittest.TestCase):
    def test_start_threshold_small(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenario_9/train.html', star_depth_threshold=3)
        rule_composer_class.compare_test_page(test_page='scenario_9/test.html', allow_fine_grain_relations=True)

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

    def test_start_threshold_large(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenario_9/train.html', star_depth_threshold=1000)
        rule_composer_class.compare_test_page(test_page='scenario_9/test.html', allow_fine_grain_relations=True)

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [7])

