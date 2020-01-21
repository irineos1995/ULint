from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag
import networkx as nx
from graph_base_case import plot_graph, draw_graph3


from tidy import TAG

class RuleComposer():
    TAG_OBJECT = None

    def __init__(self, threshold, train_page):
        self.TAG_OBJECT = TAG(threshold)
        
        with open(train_page, 'r') as tr_p:
            train_soup = BeautifulSoup(tr_p, 'html.parser')


            for child in train_soup.childGenerator():
                self.get_parents_recursively(child, self.TAG_OBJECT)
                break

    def compare_test_page(self, test_page):
        with open(test_page, 'r') as test_p:
            test_soup = BeautifulSoup(test_p, 'html.parser')
            
            for child in test_soup.childGenerator():
                self.get_parents_recursively_for_test(child, self.TAG_OBJECT)
                break

    def get_line_number_errors(self):
        return self.TAG_OBJECT.get_line_number_errors()

    def get_data(self):
        return self.TAG_OBJECT.get_data()

    def get_encountered_parent_orders_and_depths(self):
        return self.TAG_OBJECT.get_encountered_parent_orders_and_depths()

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

    def plot_directed_graph(self):
        graph = self.create_graph()
        # plot_graph(graph)
        draw_graph3(graph)

    def get_parents_recursively(self, tree, class_obj):
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
                            class_obj.add_parents(tuple(child_class), parents)
                    else:
                        continue
                    self.get_parents_recursively(child, class_obj)
            else:
                if not tree.isspace(): #Just to avoid printing "\n" parsed from document.
                    pass



    def get_parents_recursively_for_test(self, tree, class_obj):
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
                            passed, errors = class_obj.compare_child_and_its_parents_with_db(tuple(child_class), parents, child.sourceline)
                            if not passed:
                                print("Error in line: {} {}".format(child.sourceline, "Errors: {}".format(errors) if errors else ""))
                    else:
                        continue
                    self.get_parents_recursively_for_test(child, class_obj)
            else:
                if not tree.isspace(): #Just to avoid printing "\n" parsed from document.
                    pass





# TAG().print_child_parents_dict()