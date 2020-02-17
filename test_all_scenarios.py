import unittest
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

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
    def test_nested_children_permissively(self):
        rule_composer_class = RuleComposer(threshold=1, train_set='scenarios/scenario_2/train.html')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_2/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

    def test_nested_children_not_permissively(self):
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

class TestScenario4(unittest.TestCase):
    def test_threshold_matters_2(self):
        rule_composer_class = RuleComposer(threshold=0.6, train_set='scenarios/scenario_4/train.html')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_4/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [4])

    def test_threshold_matters_3(self):
        rule_composer_class = RuleComposer(threshold=1, train_set='scenarios/scenario_4/train.html')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_4/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

class TestScenario5(unittest.TestCase):
    def test_threshold_matters_4(self):
        rule_composer_class = RuleComposer(threshold=0.6, train_set='scenarios/scenario_5/train.html')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_5/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

    def test_threshold_matters_5(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_5/train.html')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_5/test.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [5])

class TestGraphPlot(unittest.TestCase):
    def test_plot_big_graph(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_5/big_training_data.html')
        rule_composer_class.plot_directed_graph(filename='graph_files/big_graph.html')

    def test_plot_small_graph(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_5/train.html')
        rule_composer_class.plot_directed_graph(filename='graph_files/small_graph.html')

class TestFineGraphPlot(unittest.TestCase):

    def test_plot_small_fine_graph(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_4/train.html')
        # rule_composer_class.plot_fine_directed_graph(filename='small_fine_graph.html')
        # rule_composer_class.construct_fine_relations()

    def test_plot_small_fine_graph_v2(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_4/train.html')
        rule_composer_class.plot_fine_directed_graph_v2(filename='graph_files/small_fine_graph_v2.html')

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

class TestScenario10(unittest.TestCase):
    def test_training_algorithm_with_10_pages(self):
        max_training_pages = 10
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_10/train_set/', max_training_pages=max_training_pages)
        self.assertEqual([], [])

    def test_training_algorithm_with_20_pages(self):
        max_training_pages = 20
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_10/train_set/', max_training_pages=max_training_pages)
        self.assertEqual([], [])

    def test_training_algorithm_with_30_pages(self):
        max_training_pages = 30
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_10/train_set/', max_training_pages=max_training_pages)
        self.assertEqual([], [])

    def test_training_algorithm_with_40_pages(self):
        max_training_pages = 40
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_10/train_set/', max_training_pages=max_training_pages)
        self.assertEqual([], [])

    def test_training_algorithm_with_50_pages(self):
        max_training_pages = 50
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_10/train_set/', max_training_pages=max_training_pages)
        self.assertEqual([], [])

    def test_training_algorithm_with_60_pages(self):
        max_training_pages = 60
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_10/train_set/', max_training_pages=max_training_pages)
        self.assertEqual([], [])

    def test_training_algorithm_with_70_pages(self):
        max_training_pages = 70
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_10/train_set/', max_training_pages=max_training_pages)
        self.assertEqual([], [])

    def test_training_algorithm_with_over_the_limit_pages(self):
        max_training_pages = 1000
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_10/train_set/', max_training_pages=max_training_pages)

        rule_composer_class.plot_fine_directed_graph_v2(filename='graph_files/huge_fine_graph_v2.html')
        self.assertEqual([], [])

class TestScenario11(unittest.TestCase):
    def test_vanilla_bootstrap(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_11/vanilla_bootstrap_train_pages/')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_11/test.htm', allow_fine_grain_relations=True)
        # rule_composer_class.plot_fine_directed_graph_v2(filename='graph_files/fine_graph_v2_with_vanilla_bootstrap.html')

        errors = rule_composer_class.get_line_number_errors()
        self.assertEqual(list(errors), [])

    def test_memory_footprint_25_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=25)
        self.assertEqual([], [])

    def test_memory_footprint_50_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=50)
        self.assertEqual([], [])

    def test_memory_footprint_75_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=75)
        self.assertEqual([], [])

    def test_memory_footprint_100_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=100)
        self.assertEqual([], [])

    def test_memory_footprint_125_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=125)
        self.assertEqual([], [])

    def test_memory_footprint_150_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=150)
        self.assertEqual([], [])

    def test_memory_footprint_175_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=175)
        self.assertEqual([], [])

    def test_memory_footprint_200_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=200)
        self.assertEqual([], [])

    def test_memory_footprint_225_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=225)
        self.assertEqual([], [])

    def test_memory_footprint_233_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=233)
        self.assertEqual([], [])

class TestScenario12(unittest.TestCase):
    def test_real_data(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='scenarios/scenario_12/bootstrap_4_html_files/', star_depth_threshold=3)
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html', allow_fine_grain_relations=True, ignore_unseen_classes=True)

        errors = rule_composer_class.get_line_number_errors()

        set_of_errors = set(errors)
        print(set_of_errors)
        print(len(set_of_errors))
        self.assertEqual([], [])

class TestScenario13(unittest.TestCase):
    def test_real_data_with_w3_rules(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3)
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html',
                                              allow_fine_grain_relations=True,
                                              ignore_unseen_classes=True,
                                              include_warnings=True
                                              )

        errors = rule_composer_class.get_line_number_errors()

        set_of_errors = set(errors)
        print(set_of_errors)
        print(len(set_of_errors))
        self.assertEqual([], [])

class TestScenario14(unittest.TestCase):
    def test_nn_data_processing(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/')
        processed_data = rule_composer_class.process_data(rule_composer_class.construct_fine_relations())

        print(processed_data)
        self.assertEqual([], [])

    def test_nn_data_processing_to_csv(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/')
        processed_data = rule_composer_class.process_data(rule_composer_class.construct_fine_relations())
        rule_composer_class.write_process_data_to_csv(processed_data, 'processed_data.csv')

        print(processed_data)
        self.assertEqual([], [])

    def test_nn_errors_processing_to_csv(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html', allow_fine_grain_relations=True, ignore_unseen_classes=True)
        rule_composer_class.generate_nn_training_data('working.csv')

    def test_nn_prediction(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/')
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html', allow_fine_grain_relations=True, ignore_unseen_classes=True)

        rule_composer_class.generate_nn_training_data('working.csv')
        rule_composer_class.train()

        print(rule_composer_class.predict([[128,212,2], [128,2,-1]]))
        self.assertEqual([], [])