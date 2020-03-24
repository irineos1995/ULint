import unittest
import os,sys,inspect
from termcolor import colored, cprint
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import json

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
        print('Total training elements for 25 pages: {}'.format(rule_composer_class.get_total_training_elements()))
        self.assertEqual([], [])

    def test_memory_footprint_50_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=50)
        print('Total training elements for 50 pages: {}'.format(rule_composer_class.get_total_training_elements()))
        self.assertEqual([], [])

    def test_memory_footprint_75_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=75)
        print('Total training elements for 75 pages: {}'.format(rule_composer_class.get_total_training_elements()))
        self.assertEqual([], [])

    def test_memory_footprint_100_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=100)
        print('Total training elements for 100 pages: {}'.format(rule_composer_class.get_total_training_elements()))
        self.assertEqual([], [])

    def test_memory_footprint_125_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=125)
        print('Total training elements for 125 pages: {}'.format(rule_composer_class.get_total_training_elements()))
        self.assertEqual([], [])

    def test_memory_footprint_150_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=150)
        print('Total training elements for 150 pages: {}'.format(rule_composer_class.get_total_training_elements()))
        self.assertEqual([], [])

    def test_memory_footprint_175_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=175)
        print('Total training elements for 175 pages: {}'.format(rule_composer_class.get_total_training_elements()))
        self.assertEqual([], [])

    def test_memory_footprint_200_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=200)
        print('Total training elements for 200 pages: {}'.format(rule_composer_class.get_total_training_elements()))
        self.assertEqual([], [])

    def test_memory_footprint_225_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=225)
        print('Total training elements for 225 pages: {}'.format(rule_composer_class.get_total_training_elements()))
        self.assertEqual([], [])

    def test_memory_footprint_233_pages(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples', max_training_pages=233)
        print('Total training elements for 233 pages: {}'.format(rule_composer_class.get_total_training_elements()))
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
                                              include_warnings=False
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

class TestScenario15(unittest.TestCase):
    def test_depth_cap(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3)
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html',
                                              allow_fine_grain_relations=True,
                                              ignore_unseen_classes=True,
                                              include_warnings=False,
                                              depth_cap=None,
                                              parent_level_errors=True
                                              )

        rule_composer_class.print_parent_level_errors()
        errors = rule_composer_class.get_line_number_errors()

        set_of_errors = set(errors)
        print(set_of_errors)
        print(len(set_of_errors))
        cprint(rule_composer_class.depth_of_errors_report())

        self.assertFalse(365 in set_of_errors)

class TestScenario16(unittest.TestCase):
    def test_depth_report(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3)
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html',
                                              allow_fine_grain_relations=True,
                                              ignore_unseen_classes=True,
                                              include_warnings=False,
                                              depth_cap=None
                                              )

        errors = rule_composer_class.get_line_number_errors()

        set_of_errors = set(errors)
        print(set_of_errors)
        print(len(set_of_errors))

        cprint(rule_composer_class.depth_of_errors_report())

        self.assertFalse(False)

class TestScenario17(unittest.TestCase):
    def test_relation_cap(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3, debug=True)
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html',
                                              allow_fine_grain_relations=True,
                                              ignore_unseen_classes=True,
                                              include_warnings=False,
                                              depth_cap=None,
                                              parent_level_errors=True,
                                              relation_cap=None
                                              )

        rule_composer_class.print_parent_level_errors()
        errors = rule_composer_class.get_line_number_errors()

        set_of_errors = set(errors)
        print(set_of_errors)
        print(len(set_of_errors))
        cprint(rule_composer_class.depth_of_errors_report())

        # self.assertFalse(507 in set_of_errors)

class TestScenario18(unittest.TestCase):
    def test_linting_time(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=1, debug=False, max_training_pages=225, json_rules_filename="rules.json")
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_12/coreui-free-bootstrap-admin-template-3-next/src/index.html',
                                              allow_fine_grain_relations=True,
                                              ignore_unseen_classes=True,
                                              include_warnings=False,
                                              depth_cap=1,
                                              parent_level_errors=True,
                                              relation_cap=6
                                              )

        rule_composer_class.print_parent_level_errors()
        errors = rule_composer_class.get_line_number_errors()
        print(len(errors))
        # set_of_errors = set(errors)
        # print(set_of_errors)
        # print(len(set_of_errors))
        # cprint(rule_composer_class.depth_of_errors_report())

        # self.assertFalse(507 in set_of_errors)

class TestScenario19(unittest.TestCase):
    def test_data_dump(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3, debug=True, max_training_pages=225)
        rule_composer_class.dump_rules(filename="rules.json")

        fine_relations = rule_composer_class.construct_fine_relations()
        with open('rules.json') as json_file:
            rules = json.load(json_file)
        self.assertEqual(fine_relations, rules)

    def test_data_load(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3, debug=True, max_training_pages=225, json_rules_filename="rules.json")
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

        rule_composer_class_2 = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3, debug=True, max_training_pages=225)
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

        self.assertEqual(errors, errors_2)

class TestScenario20(unittest.TestCase):
    def test_proving_bootlint_wrong(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='w3_bootstrap_examples/', star_depth_threshold=3, debug=True, max_training_pages=225, json_rules_filename="rules.json")
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
        print(len(errors))

class TestScenario21(unittest.TestCase):
    def test_training_with_vue_framework(self):
        rule_composer_class = RuleComposer(threshold=0, train_set='vue-material-training_v2/', star_depth_threshold=3, debug=False, max_training_pages=225, json_rules_filename="rules_vue.json")
        # rule_composer_class.dump_rules(filename="rules_vue.json")
        rule_composer_class.compare_test_page(test_page='scenarios/scenario_14/test.vue',
                                              allow_fine_grain_relations=True,
                                              ignore_unseen_classes=True,
                                              include_warnings=False,
                                              depth_cap=6,
                                              parent_level_errors=True,
                                              relation_cap=None
                                              )
        rule_composer_class.print_parent_level_errors()

class TestScenario20(unittest.TestCase):
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

    def test_actual_stuff(self):
        # rule_composer_class = RuleComposer(threshold=0, train_set='frameworks-examples/foundation-sites-develop', star_depth_threshold=3, debug=True, max_training_pages=50, json_rules_filename="foundation_official_rules_150_pages.json")
        rule_composer_class = RuleComposer(threshold=0, train_set='frameworks-examples/foundation-sites-develop/training-pages',
                                           star_depth_threshold=3, debug=True, max_training_pages=1050)
        # rule_composer_class.dump_rules(filename="foundation_official_rules_150_pages.json")
        # rule_composer_class.compare_test_page(test_page='frameworks-examples/foundation-sites-develop/test-pages/docker.html',
        #                                       allow_fine_grain_relations=True,
        #                                       ignore_unseen_classes=True,
        #                                       include_warnings=False,
        #                                       depth_cap=1,
        #                                       parent_level_errors=True,
        #                                       relation_cap=None
        #                                       )

        errors = rule_composer_class.print_parent_level_errors()
        print('Total test elements: {}'.format(rule_composer_class.get_total_test_elements()))
        print('Total train elements: {}'.format(rule_composer_class.get_total_training_elements()))
