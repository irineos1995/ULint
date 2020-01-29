from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag, Doctype
import networkx as nx
from graph_base_case import plot_graph, draw_graph3, draw_fine_graph3, draw_fine_graph3_v2
from tidy import TAG

class RuleComposer(TAG):
    TAG_OBJECT = None

    def __init__(self, threshold, train_page):
        TAG.__init__(self, threshold)
        
        with open(train_page, 'r') as tr_p:
            train_soup = BeautifulSoup(tr_p, 'html.parser')

            for child in train_soup.childGenerator():
                if isinstance(child, Tag):
                    self.get_parents_recursively(child)
                    break

    def compare_test_page(self, test_page, allow_fine_relations):
        with open(test_page, 'r') as test_p:
            test_soup = BeautifulSoup(test_p, 'html.parser')
            
            for child in test_soup.childGenerator():
                self.get_parents_recursively_for_test(child, allow_fine_relations)
                break


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
        print(parent_orders_and_depths)
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
                        print('node: {} ---> child: {}'.format(node, child))
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
        graph = self.create_graph()
        # plot_graph(graph)
        draw_graph3(graph, output_filename=filename)

    def plot_fine_directed_graph(self, filename):
        graph = self.create_fine_graph()
        # plot_graph(graph)
        draw_fine_graph3(graph, output_filename=filename)

    def plot_fine_directed_graph_v2(self, filename):
        graph = self.create_fine_graph_v2()
        # plot_graph(graph)
        draw_fine_graph3_v2(graph, output_filename=filename)

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



    def get_parents_recursively_for_test(self, tree, allow_fine_relations=False):
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
                            passed, errors = self.compare_child_and_its_parents_with_db(tuple(child_class), parents, child.sourceline, allow_fine_relations)
                            if not passed:
                                print("Error in line: {} {}".format(child.sourceline, "Errors: {}".format(errors) if errors else ""))
                    else:
                        continue
                    self.get_parents_recursively_for_test(child, allow_fine_relations)
            else:
                if not tree.isspace(): #Just to avoid printing "\n" parsed from document.
                    pass