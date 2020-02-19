from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag, Doctype
import networkx as nx
from graph_base_case import plot_graph, draw_graph3, draw_fine_graph3, draw_fine_graph3_v2
from TAG import Relations
import os
import glob
import tracemalloc
from datetime import datetime
from termcolor import colored, cprint
from NN import NeuralNetwork

class RuleComposer(Relations, NeuralNetwork):
    TAG_OBJECT = None
    graph = None
    fine_graph = None
    sourceline_errors_for_NN = []

    def __init__(self, threshold, train_set, max_training_pages=None, star_depth_threshold=None):
        start_time = datetime.now()
        tracemalloc.start()
        Relations.__init__(self, threshold, star_depth_threshold)

        if os.path.isdir(train_set):
            cprint('Is a directory!', 'yellow')
            files_list = glob.glob(os.path.join(train_set, "*.htm*"))
            if max_training_pages and len(files_list) >= max_training_pages > 0:
                files_list = files_list[:max_training_pages]
            for file in files_list:
                cprint('Processing file: {}'.format(colored(file, 'blue')))
                with open(file, 'r') as tr_p:
                    train_soup = BeautifulSoup(tr_p, 'html.parser')
                    for child in train_soup.childGenerator():
                        if isinstance(child, Tag):
                            self.get_parents_recursively(child)

        elif os.path.isfile(train_set):
            cprint('Is a file!', 'yellow')
            with open(train_set, 'r') as tr_p:
                # print('Processing file: {}'.format(train_set))
                cprint('Processing file: {}'.format(colored(train_set, 'blue')))
                train_soup = BeautifulSoup(tr_p, 'html.parser')
                for child in train_soup.childGenerator():
                    if isinstance(child, Tag):
                        self.get_parents_recursively(child)

        end_time = datetime.now()
        total_seconds = (end_time - start_time).total_seconds()
        current, peak = tracemalloc.get_traced_memory()
        if not max_training_pages and files_list:
            max_training_pages = len(files_list)

        cprint('Total time for training {} pages: {} seconds'.format(colored(max_training_pages, 'cyan'), colored(total_seconds, 'cyan')))
        cprint('Total number of coarse rules learned: {}'.format(colored(self.get_number_of_coarse_rules_composed(), 'cyan')))
        cprint('Total number of coarse nodes: {}'.format(colored(self.get_number_of_coarse_nodes_composed(), 'cyan')))
        # cprint('Total number of coarse nodes (NetworkX): {}'.format(colored(number_of_coarse_nodes, 'cyan')))
        cprint('Total number of fine rules learned: {}'.format(colored(self.get_number_of_fine_rules_composed(), 'cyan')))
        cprint('Total number of fine nodes: {}'.format(colored(self.get_number_of_fine_nodes_composed(), 'cyan')))
        # cprint('Total number of fine nodes (NetworkX): {}'.format(colored(number_of_fine_nodes), 'cyan'))
        cprint('Total number of distinct bootstrap classes identified: {}'.format(colored(len(self.get_distinct_fine_grain_classes()), 'cyan')))
        cprint("Peak memory usage was {} MB".format(colored((peak / 10 ** 6), 'cyan')))
        tracemalloc.stop()

    def compare_test_page(self, test_page, allow_fine_grain_relations, ignore_unseen_classes, include_warnings=False, depth_cap=None):
        with open(test_page, 'r') as test_p:
            test_soup = BeautifulSoup(test_p, 'html.parser')

            for child in test_soup.childGenerator():
                if isinstance(child, Tag):
                    self.get_parents_recursively_for_test(child, allow_fine_grain_relations, ignore_unseen_classes, include_warnings, depth_cap)


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
        draw_graph3(self.graph, output_filename=filename)

    def plot_fine_directed_graph(self, filename):
        graph = self.create_fine_graph()
        # plot_graph(graph)
        draw_fine_graph3(graph, output_filename=filename)

    def plot_fine_directed_graph_v2(self, filename):
        self.fine_graph = self.create_fine_graph_v2()
        # plot_graph(graph)
        draw_fine_graph3_v2(self.fine_graph, output_filename=filename)

    def get_parents_recursively(self, tree):
        if not tree:
            return
        else:
            if "childGenerator" in dir(tree):
                for child in tree.childGenerator():
                    if isinstance(child, Tag):
                        child_class = child.get("class", [])
                        if child_class:
                            parents = [tuple(parent.get('class')) for parent in child.parents if parent.get('class', [])]
                            if not parents:
                                parents = [()]
                            self.add_parents(tuple(child_class), parents)
                    else:
                        continue
                    self.get_parents_recursively(child)
            else:
                if not tree.isspace(): #Just to avoid printing "\n" parsed from document.
                    pass



    def get_parents_recursively_for_test(self, tree, allow_fine_relations, ignore_unseen_classes, include_warnings, depth_cap):
        if not tree:
            return
        else:
            if "childGenerator" in dir(tree):
                for child in tree.childGenerator():
                    if isinstance(child, Tag):
                        child_class = child.get("class", [])
                        if child_class:
                            parents = [tuple(parent.get('class')) for parent in child.parents if parent.get('class', [])]
                            if not parents:
                                parents = [()]
                            passed, errors, errors_list_for_nn_processing = self.compare_child_and_its_parents_with_db(tuple(child_class), parents, child.sourceline, allow_fine_relations, ignore_unseen_classes, include_warnings, depth_cap)
                            if not passed:
                                # print("Error in line: {} {}".format(child.sourceline, "Errors: {}".format(errors) if errors else ""))
                                cprint(errors)
                                self.sourceline_errors_for_NN += errors_list_for_nn_processing
                    else:
                        continue
                    self.get_parents_recursively_for_test(child, allow_fine_relations, ignore_unseen_classes, include_warnings, depth_cap)
            else:
                if not tree.isspace(): #Just to avoid printing "\n" parsed from document.
                    pass

    def generate_nn_training_data(self):
        self.process_errors(self.sourceline_errors_for_NN)
        return