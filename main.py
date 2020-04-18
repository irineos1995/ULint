from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag, Doctype
import networkx as nx
from graph_base_case import plot_graph, draw_graph3, draw_fine_graph3, draw_fine_graph3_v2
from TAG import Relations
import os
import glob
import tracemalloc
import re
from datetime import datetime
from termcolor import colored, cprint
from NN import NeuralNetwork
from UI import UserInterface
import mutator

class RuleComposer(Relations, NeuralNetwork, UserInterface):
    TAG_OBJECT = None
    graph = None
    fine_graph = None
    max_training_pages = None
    total_training_elements = 0
    total_test_elements = 0

    def __init__(self, threshold, train_set, max_training_pages=None, star_depth_threshold=None, debug=False, json_rules_filename=None):
        start_time = datetime.now()
        tracemalloc.start()
        if json_rules_filename:
            dumped_fine_relations = self.load_rules(json_rules_filename)
            Relations.__init__(self, threshold, star_depth_threshold, dumped_fine_relations)

            end_time = datetime.now()
            total_seconds = (end_time - start_time).total_seconds()
            current, peak = tracemalloc.get_traced_memory()

            if debug:
                cprint('Total time for loading dumped rules: {} seconds'.format(colored(total_seconds, 'cyan')))
                cprint('Total number of fine rules learned: {}'.format(colored(self.get_number_of_fine_rules_composed(), 'cyan')))
                cprint('Total number of fine nodes: {}'.format(colored(self.get_number_of_fine_nodes_composed(), 'cyan')))
                cprint("Peak memory usage was {} MB".format(colored((peak / 10 ** 6), 'cyan')))
            tracemalloc.stop()
            return
        Relations.__init__(self, threshold, star_depth_threshold)

        if os.path.isdir(train_set):
            if debug: cprint('Is a directory!', 'yellow')
            files_list = glob.glob(os.path.join(train_set, "*.htm*"))
            files_list = sorted(files_list, key=lambda x: float(re.findall("(\d+)", x)[0]))
            files_list = self.distinguish_copy_and_original(files_list)
            if not files_list:
                files_list = glob.glob(os.path.join(train_set, "*.vue"))
                files_list = sorted(files_list, key=lambda x: float(re.findall("(\d+)", x)[0]))
                files_list = self.distinguish_copy_and_original(files_list)

            if not files_list:
                return
            if max_training_pages and len(files_list) >= max_training_pages > 0:
                files_list = files_list[:max_training_pages]
            self.max_training_pages = max_training_pages
            for file in files_list:
                if debug: cprint('Processing file: {}'.format(colored(file, 'blue')))
                with open(file, 'r') as tr_p:
                    train_soup = BeautifulSoup(tr_p, 'html.parser')
                    for child in train_soup.childGenerator():
                        if isinstance(child, Tag):
                            self.get_parents_recursively(child)

        elif os.path.isfile(train_set):
            if debug: cprint('Is a file!', 'yellow')
            files_list = []
            with open(train_set, 'r') as tr_p:
                # print('Processing file: {}'.format(train_set))
                if debug: cprint('Processing file: {}'.format(colored(train_set, 'blue')))
                train_soup = BeautifulSoup(tr_p, 'html.parser')
                for child in train_soup.childGenerator():
                    if isinstance(child, Tag):
                        self.get_parents_recursively(child)

        end_time = datetime.now()
        total_seconds = (end_time - start_time).total_seconds()
        current, peak = tracemalloc.get_traced_memory()
        if not max_training_pages and files_list:
            max_training_pages = len(files_list)

        if debug:
            cprint('Total time for training {} pages: {} seconds'.format(colored(max_training_pages, 'cyan'), colored(total_seconds, 'cyan')))
            cprint('Total number of coarse rules learned: {}'.format(colored(self.get_number_of_coarse_rules_composed(), 'cyan')))
            cprint('Total number of coarse nodes: {}'.format(colored(self.get_number_of_coarse_nodes_composed(), 'cyan')))
            # cprint('Total number of coarse nodes (NetworkX): {}'.format(colored(number_of_coarse_nodes, 'cyan')))
            cprint('Total number of fine rules learned: {}'.format(colored(self.get_number_of_fine_rules_composed(), 'cyan')))
            cprint('Total number of fine nodes: {}'.format(colored(self.get_number_of_fine_nodes_composed(), 'cyan')))
            # cprint('Total number of fine nodes (NetworkX): {}'.format(colored(number_of_fine_nodes), 'cyan'))
            cprint("Peak memory usage was {} MB".format(colored((peak / 10 ** 6), 'cyan')))
        tracemalloc.stop()

    def distinguish_copy_and_original(self, files_list):
        copy = []
        original = []
        for file in files_list:
            if 'copy' in file.lower():
                copy.append(file)
            else:
                original.append(file)
        return original + copy

    def compare_test_page(self, test_page, allow_fine_grain_relations=True, ignore_unseen_classes=True, include_warnings=False, depth_cap=None, parent_level_errors=True, relation_cap=None):
        start_time = datetime.now()
        if relation_cap:
            with open(test_page, 'r') as test_p:
                test_soup = BeautifulSoup(test_p, 'html.parser')

                for child in test_soup.childGenerator():
                    if isinstance(child, Tag):
                        self.identify_parent_that_contain_any(child, allow_fine_grain_relations, ignore_unseen_classes, include_warnings, depth_cap, parent_level_errors, relation_cap)


        with open(test_page, 'r') as test_p:
            test_soup = BeautifulSoup(test_p, 'html.parser')

            for child in test_soup.childGenerator():
                if isinstance(child, Tag):
                    self.get_parents_recursively_for_test(child, allow_fine_grain_relations, ignore_unseen_classes, include_warnings, depth_cap, parent_level_errors, relation_cap)
        end_time = datetime.now()
        total_seconds = (end_time - start_time).total_seconds()
        cprint('Total time for linting with {} training pages: {} seconds'.format(colored(self.max_training_pages, 'cyan'),
                                                                     colored(total_seconds, 'cyan')))

        print('True positives: {}'.format(self.true_positives))
        print('True negatives: {}'.format(self.true_negatives))

    def compare_shuffled_test_page(self, test_page, allow_fine_grain_relations, ignore_unseen_classes, include_warnings=False, depth_cap=None, parent_level_errors=False, relation_cap=None):
        start_time = datetime.now()
        if relation_cap:
            test_soup = mutator.shuffle(test_page)
            for child in test_soup.childGenerator():
                if isinstance(child, Tag):
                    self.identify_parent_that_contain_any(child, allow_fine_grain_relations, ignore_unseen_classes, include_warnings, depth_cap, parent_level_errors, relation_cap)


        shuffle_page_name = test_page.replace('.html', '_shuffled.html')
        test_soup = mutator.shuffle(test_page)
        with open(shuffle_page_name, 'w') as outfl:
            outfl.write(str(test_soup))

        for child in test_soup.childGenerator():
            if isinstance(child, Tag):
                self.get_parents_recursively_for_test(child, allow_fine_grain_relations, ignore_unseen_classes, include_warnings, depth_cap, parent_level_errors, relation_cap)
        end_time = datetime.now()
        total_seconds = (end_time - start_time).total_seconds()
        cprint('Total time for linting with {} training pages: {} seconds'.format(colored(self.max_training_pages, 'cyan'),
                                                                     colored(total_seconds, 'cyan')))

        print('True positives: {}'.format(self.true_positives))
        print('True negatives: {}'.format(self.true_negatives))

    def get_graph_distinct_nodes(self, graph):
        nodes = set()
        for node in graph.nodes:
            print(node)
            eval_node = eval(node)
            sorted_node = tuple(sorted(eval_node))
            nodes.add(sorted_node)
        return nodes


    def create_graph(self):
        '''
            {
                (): {
                    ('a', 'y'): {1}
                }, 
                ('a', 'y'): {
                    ('b', 'c'): {1}, 
                    ('a', 'x'): {2}, 
                    ('c',): {3}, 
                    ('y', 'z'): {1}, 
                    ('i',): {2}, 
                    ('q',): {2}
                }, 
                ('b', 'c'): {
                    ('a', 'x'): {1}, 
                    ('c',): {2}
                }, 
                ('a', 'x'): {
                    ('c',): {1}
                }, 
                ('i',): {
                    ('c',): {1}
                }, 
                ('y', 'z'): {
                    ('c',): {2}, 
                    ('i',): {1}, 
                    ('q',): {1}
                }, 
                ('q',): {
                    ('c',): {1}
                }
            }
        '''
        parent_orders_and_depths = self.get_encountered_parent_orders_and_depths()
        G = nx.DiGraph()
        for node in parent_orders_and_depths:
            if not G.has_node(node):
                G.add_node(str(node))
            for child in parent_orders_and_depths[node]:
                if not G.has_node(child):
                    G.add_node(str(child))
                G.add_edge(str(node), str(child), depth = str(parent_orders_and_depths[node][child]))
        return G

    def create_fine_graph(self):
        '''
            {
                (): {
                    ('a', 'y'): {1}
                },
                ('a', 'y'): {
                    ('b', 'c'): {1},
                    ('a', 'x'): {2},
                    ('c',): {3},
                    ('y', 'z'): {1},
                    ('i',): {2},
                    ('q',): {2}
                },
                ('b', 'c'): {
                    ('a', 'x'): {1},
                    ('c',): {2}
                },
                ('a', 'x'): {
                    ('c',): {1}
                },
                ('i',): {
                    ('c',): {1}
                },
                ('y', 'z'): {
                    ('c',): {2},
                    ('i',): {1},
                    ('q',): {1}
                },
                ('q',): {
                    ('c',): {1}
                }
            }
        '''
        parent_orders_and_depths = self.get_encountered_parent_orders_and_depths()
        # print(parent_orders_and_depths)
        G = nx.DiGraph()
        for node in parent_orders_and_depths:
            # Now need to loop through individual classes in that node
            if not node: # means is an empty class
                cls = str(node)
                if not G.has_node(cls):
                    G.add_node(cls)
                for child in parent_orders_and_depths[node]:
                    # Now need to loop through individual classes in child
                    for ccls in child:
                        ccls = str(ccls)
                        if not G.has_node(ccls):
                            G.add_node(ccls)

                        if not G.get_edge_data(cls,ccls,default=0):
                            G.add_edge(cls, ccls, depth=str(parent_orders_and_depths[node][child]))
                        else:
                            G[cls][ccls]['depth'] = str(eval(G[cls][ccls]['depth']).union(parent_orders_and_depths[node][child]))

            else:
                for cls in node:
                    cls = str(cls)
                    if not G.has_node(cls):
                        G.add_node(cls)
                    for child in parent_orders_and_depths[node]:
                        # print('node: {} ---> child: {}'.format(node, child))
                        # Now need to loop through individual classes in child
                        for ccls in child:
                            ccls = str(ccls)
                            if not G.has_node(ccls):
                                G.add_node(ccls)
                            if not G.get_edge_data(cls,ccls,default=0):
                                G.add_edge(cls, ccls, depth=str(parent_orders_and_depths[node][child]))
                            else:
                                G[cls][ccls]['depth'] = str(eval(G[cls][ccls]['depth']).union(parent_orders_and_depths[node][child]))

        return G

    def create_fine_graph_v2(self):
        '''
            {
                '()':
                    {
                        'a': {1},
                        'y': {1}
                    },
                'a':
                    {
                        'b': {1},
                        'c': {1, 2, 3},
                        'a': {2},
                        'x': {2},
                        'y': {1},
                        'z': {1}
                    },
                'y':
                    {
                        'b': {1},
                        'c': {1, 2, 3},
                        'a': {2},
                        'x': {2},
                        'y': {1},
                        'z': {1}
                    },
                'b':
                    {
                        'a': {1},
                        'x': {1},
                        'c': {2}
                    },
                'c':
                    {
                        'a': {1},
                        'x': {1},
                        'c': {2}
                    },
                'x':
                    {
                        'c': {1}
                    },
                'z':
                    {
                        'c': {1}
                    }
            }
        '''
        fine_relations = self.construct_fine_relations()
        G = nx.DiGraph()
        for node in fine_relations:
            # Now need to loop through individual classes in that node
            if not G.has_node(node):
                G.add_node(node)
            for child in fine_relations[node]:
                depth = str(fine_relations[node][child])
                if not G.has_node(child):
                    G.add_node(child)
                G.add_edge(node, child, depth=depth)

        return G

    def plot_directed_graph(self, filename):
        self.graph = self.create_graph()
        # plot_graph(graph)
        plotted_graph = draw_graph3(self.graph, output_filename=filename)
        return plotted_graph

    def plot_fine_directed_graph(self, filename):
        graph = self.create_fine_graph()
        # plot_graph(graph)
        draw_fine_graph3(graph, output_filename=filename)

    def plot_fine_directed_graph_v2(self, filename):
        self.fine_graph = self.create_fine_graph_v2()
        # plot_graph(graph)
        plotted_graph = draw_fine_graph3_v2(self.fine_graph, output_filename=filename)
        return plotted_graph

    def get_parents_recursively(self, tree):
        if not tree:
            return
        else:
            if "childGenerator" in dir(tree):
                for child in tree.childGenerator():
                    self.total_training_elements += 1
                    if isinstance(child, Tag):
                        child_class = child.get("class", [])
                        if child_class:
                            # parents = [tuple(parent.get('class')) for parent in child.parents if parent.get('class', [])]
                            parents = [tuple(parent.get('class', ())) for parent in child.parents]
                            if not parents:
                                parents = [()]
                            self.add_parents(tuple(child_class), parents)
                    else:
                        continue
                    self.get_parents_recursively(child)
            else:
                if not tree.isspace(): #Just to avoid printing "\n" parsed from document.
                    pass

    def identify_parent_that_contain_any(self, tree, allow_fine_relations, ignore_unseen_classes, include_warnings, depth_cap, parent_level_errors, relation_cap):
        if not tree:
            return
        else:
            if "childGenerator" in dir(tree):
                for child in tree.childGenerator():
                    if isinstance(child, Tag):
                        child_class = child.get("class", ())
                        if child_class:
                            parents = [tuple(parent.get('class', ())) for parent in child.parents]
                            immediate_parent = parents[0]
                            parent_line_numbers = [parent.sourceline for parent in child.parents]
                            if not parents:
                                parents = []
                                parent_line_numbers = []
                            self.store_test_data_parent_children_relation(immediate_parent, child_class)

                    else:
                        continue
                    self.identify_parent_that_contain_any(child, allow_fine_relations, ignore_unseen_classes, include_warnings, depth_cap, parent_level_errors, relation_cap)
            else:
                if not tree.isspace(): #Just to avoid printing "\n" parsed from document.
                    pass


    def get_parents_recursively_for_test(self, tree, allow_fine_relations, ignore_unseen_classes, include_warnings, depth_cap, parent_level_errors, relation_cap):
        if not tree:
            return
        else:
            if "childGenerator" in dir(tree):
                for child in tree.childGenerator():
                    if isinstance(child, Tag):
                        self.total_test_elements += 1
                        child_class = child.get("class", [])
                        if child_class:
                            # parents = [tuple(parent.get('class')) for parent in child.parents if parent.get('class', [])]
                            parents = [tuple(parent.get('class', ())) for parent in child.parents]
                            # parent_line_numbers = [parent.sourceline for parent in child.parents if parent.get('class', [])]
                            parent_line_numbers = [parent.sourceline for parent in child.parents]
                            if not parents:
                                parents = [()]
                                parent_line_numbers = []
                            passed, errors = self.compare_child_and_its_parents_with_db(tuple(child_class), parents, child.sourceline, allow_fine_relations, ignore_unseen_classes, include_warnings, depth_cap, parent_line_numbers, parent_level_errors, relation_cap, child.sourcepos+1)
                            if not passed:
                                # print("Error in line: {} {}".format(child.sourceline, "Errors: {}".format(errors) if errors else ""))
                                # cprint(errors)
                                # print('-'*50)
                                pass
                    else:
                        continue
                    self.get_parents_recursively_for_test(child, allow_fine_relations, ignore_unseen_classes, include_warnings, depth_cap, parent_level_errors, relation_cap)
            else:
                if not tree.isspace(): #Just to avoid printing "\n" parsed from document.
                    pass


    def depth_of_errors_report(self):
        errors_list = self.depths_of_errors
        errors_set = sorted(set(errors_list))

        total_number_of_errors = len(errors_list)

        report = []

        total_percentage = 0
        for depth in errors_set:
            percentage = round((errors_list.count(depth)/total_number_of_errors)*100, 2)
            total_percentage += percentage
            error_msg = '{} of errors were found in depth {}'.format(colored(str(percentage) + ' %', 'blue'), colored(depth, 'red'))
            report.append(error_msg)
        report.append(
            'Total percentage for completeness {}'.format(colored(str(round(total_percentage, 2)) + ' %', 'blue'))
        )

        return '\n'.join(report)

    def get_total_training_elements(self):
        return self.total_training_elements
    def get_total_test_elements(self):
        return self.total_test_elements