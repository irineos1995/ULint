import unittest
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from main import *


class TestScenario1(unittest.TestCase):
    def test_identical_pages_threshold_1(self):
        rule_composer_class = RuleComposer(threshold=1, train_page='scenario_1/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_1/test.html')
        
        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(len(errors), 0)

    def test_identical_pages_threshold_0(self):
        rule_composer_class = RuleComposer(threshold=0, train_page='scenario_1/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_1/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(len(errors), 0)

class TestScenario2(unittest.TestCase):
    def test_nested_children_permissively(self):
        rule_composer_class = RuleComposer(threshold=1, train_page='scenario_2/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_2/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

    def test_nested_children_not_permissively(self):
        rule_composer_class = RuleComposer(threshold=0, train_page='scenario_2/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_2/test.html')
        
        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [4])

class TestScenario3(unittest.TestCase):
    def test_threshold_matters_1(self):
        rule_composer_class = RuleComposer(threshold=0.6, train_page='scenario_3/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_3/test.html')
        
        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [4])

class TestScenario4(unittest.TestCase):
    def test_threshold_matters_2(self):
        rule_composer_class = RuleComposer(threshold=0.6, train_page='scenario_4/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_4/test.html')
        
        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [4])

    def test_threshold_matters_3(self):
        rule_composer_class = RuleComposer(threshold=1, train_page='scenario_4/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_4/test.html')
        
        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

class TestScenario5(unittest.TestCase):
    def test_threshold_matters_4(self):
        rule_composer_class = RuleComposer(threshold=0.6, train_page='scenario_5/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_5/test.html')
        
        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

    def test_threshold_matters_5(self):
        rule_composer_class = RuleComposer(threshold=0, train_page='scenario_5/train.html')
        rule_composer_class.compare_test_page(test_page='scenario_5/test.html')
        
        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [5])

class TestGraphPlot(unittest.TestCase):
    def test_plot_graph(self):
        rule_composer_class = RuleComposer(threshold=0, train_page='scenario_5/big_training_data.html')
        rule_composer_class.plot_directed_graph()

        
