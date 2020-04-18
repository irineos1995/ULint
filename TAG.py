import re
from termcolor import colored, cprint
import json

class Relations:
    child_parents_dict = {}
    THRESHOLD = 1
    line_number_with_errors = set()
    star_depth_threshold = None
    depths_of_errors = []
    parent_level_errors_dict = {}
    plain_parent_level_errors_dict = {}
    independent_classes = []
    global_test_data_parent_children_dict = {}
    dumped_fine_relations = {}
    true_positives = 0
    true_negatives = 0

    def __init__(self, threshold, star_depth_threshold, dumped_fine_relations={}):
        self.child_parents_dict = {}
        self.THRESHOLD = threshold
        self.line_number_with_errors = set()
        self.star_depth_threshold = star_depth_threshold
        self.dumped_fine_relations = dumped_fine_relations

        with open('independent_classes', 'r') as rfl:
            self.independent_classes = [line.strip().replace(' ', '') for line in rfl.readlines() if line]

    def equal_list_of_tuples(self, list1, list2):
        if len(list1) != len(list2):
            return False
        else:
            for tpl in list1:
                match = False
                for tp in list1:
                    if self.equal_tuples(tpl, tp):
                        match = True
                if not match:
                    return False
            return True

    def equal_tuples(self, list1, list2):
        if isinstance(list1, str):
            list1 = eval(list1)
        if isinstance(list2, str):
            list2 = eval(list2)

        if isinstance(list1, list) and isinstance(list2, list):
            return self.equal_list_of_tuples(list1, list2)
        if len(list1) != len(list2):
            return False
        for element in list1:
            if element not in list2:
                return False
        return True

    def get_encountered_parent_orders_and_depths(self):
        # still need to search for unsorted child in keys of dict
        # still need to search for unsorted parent in keys of dict
        parent_child_depth_relation = {}
        child_parents_dict = self.child_parents_dict
        for child, data in child_parents_dict.items():
            child = tuple(sorted(child))
            parents_lists = data['encountered_parent_orders']
            for parent_list in parents_lists:
                for depth, parent in enumerate(parent_list):
                    parent = tuple(sorted(parent))
                    if parent not in parent_child_depth_relation:
                        parent_child_depth_relation[parent] = {
                            child : {depth+1}
                        }
                    else:
                        if child in parent_child_depth_relation[parent]:
                            parent_child_depth_relation[parent][child].add(depth+1)
                        else:
                            parent_child_depth_relation[parent][child] = {depth+1}

        if self.star_depth_threshold:
            for cls in parent_child_depth_relation:
                for ccls in parent_child_depth_relation[cls]:
                    if len(parent_child_depth_relation[cls][ccls]) >= self.star_depth_threshold:
                        parent_child_depth_relation[cls][ccls] = '*'
                    # flag = True
                    # for i in range(1, self.star_depth_threshold + 1):
                    #     if i not in parent_child_depth_relation[cls][ccls]:
                    #         flag = False
                    #         break
                    # if flag:
                    #     parent_child_depth_relation[cls][ccls] = '*'
        return parent_child_depth_relation

    def add_parents(self, child_tuple, parents_list):
        '''
            This is showing how many times we have seen a child in the big HTML tree ("occurences").
            Also shows how many times we have seen the parent of that child in those "occurences",
            as a dictionary ("parents") with key: "parent_name", value: "probability_of_presence_above_child"

            child_parents_dict = {
                ('a', 'x', 'y'): {
                    "parents": {
                        ('q', 'w'): 0.5,
                        ('b', 'z'): 0.7
                    },
                    "occurences": 2,
                    "encountered_parent_orders": [
                        [('a' 'b'), ('d', 'e')]
                    ]
                },
            }
        '''

        '''
            parents_list = [
                ("test", "niaou"),
                ("re", "ra"),
                ("w, "q")
            ]
        '''
        stored_children = self.child_parents_dict.keys()
        found = False
        for child in stored_children:
            if self.equal_tuples(child, child_tuple):
                child_tuple = child
                found = True
                break
        
        if found:
            stored_parents = self.child_parents_dict[child_tuple]["parents"]
            current_occurences = self.child_parents_dict[child_tuple]["occurences"]
            for parent in parents_list:
                local_flag = False
                for stored_p in stored_parents:
                    if self.equal_tuples(parent, stored_p):
                        local_flag = True
                        stored_parents[stored_p] = ((stored_parents[stored_p] * current_occurences) + 1)/(current_occurences + 1)
                        break
                if not local_flag:
                    stored_parents[parent] = 1/(current_occurences + 1)

            for stored_p in stored_parents:
                local_flag = False
                for parent in parents_list:
                    if self.equal_tuples(stored_p, parent):
                        local_flag = True
                if not local_flag:
                    stored_parents[stored_p] = 1/(current_occurences + 1)
            self.child_parents_dict[child_tuple]["parents"] = stored_parents
            self.child_parents_dict[child_tuple]["occurences"] += 1
            self.child_parents_dict[child_tuple]["encountered_parent_orders"].append(parents_list)
        else:
            new_parents_dict = {}
            for parent in parents_list:
                new_parents_dict[parent] = 1

            self.child_parents_dict[child_tuple] = {
                "parents": new_parents_dict,
                "occurences": 1,
                "encountered_parent_orders": [
                    parents_list
                ]
            }
        return

    def get_number_of_coarse_rules_composed(self):
        '''
            parent_child_depth_relation[parent] = {
                            child : {depth+1}
                        }
        '''
        rule_counter = 0
        parent_child_depth_relation = self.get_encountered_parent_orders_and_depths()
        for parent in parent_child_depth_relation:
            for child in parent_child_depth_relation[parent]:
                rule_counter += 1
        return rule_counter

    def get_number_of_coarse_nodes_composed(self):
        '''
            parent_child_depth_relation[parent] = {
                            child : {depth+1}
                        }
        '''
        nodes = set()
        parent_child_depth_relation = self.get_encountered_parent_orders_and_depths()
        for parent in parent_child_depth_relation:
            nodes.add(parent)
            for child in parent_child_depth_relation[parent]:
                nodes.add(child)
        return len(nodes)

    def get_number_of_fine_rules_composed(self):
        '''
            parent_child_depth_relation[parent] = {
                            child : {depth+1}
                        }
        '''
        rule_counter = 0
        fine_relations = self.construct_fine_relations()
        for parent in fine_relations:
            for child in fine_relations[parent]:
                rule_counter += 1
        return rule_counter

    def get_number_of_fine_nodes_composed(self):
        '''
            parent_child_depth_relation[parent] = {
                            child : {depth+1}
                        }
        '''
        nodes = set()
        fine_relations = self.construct_fine_relations()
        for parent in fine_relations:
            nodes.add(parent)
            for child in fine_relations[parent]:
                nodes.add(child)
        return len(nodes)

    def can_parent_can_contain_any_class(self, parent, relation_cap):
        if parent not in self.global_test_data_parent_children_dict:
            return False
        else:
            if len(self.global_test_data_parent_children_dict[parent]) > relation_cap:
                # print('parent {} : children{}\n'.format(parent, self.global_test_data_parent_children_dict[parent]))
                return True

    def compare_child_with_parents_list_fine_relations(self, child_tuple, parents_list, source_line, ignore_unseen_classes, include_warnings, depth_cap, parent_line_numbers, parent_level_errors, relation_cap, source_pos):
        combined_errors = []
        neural_network_list = [] # [[sourceLine, parent, child, depth], [sourceLine, parent, child, depth]]
        fine_relations = self.construct_fine_relations()
        parent_classes = [i for i in fine_relations.keys()]


        child_unprocessed_dicts = [i.keys() for i in fine_relations.values()]
        child_classes_lists = [list(key) for key in child_unprocessed_dicts]
        child_classes = []
        for lst in child_classes_lists:
            for key in lst:
                child_classes.append(key)

        for ccls in child_tuple:
            for depth, parent in enumerate(parents_list):
                if parent_line_numbers:
                    parent_line_number = parent_line_numbers[depth]
                depth += 1
                for cls in parent:
                    if cls in self.independent_classes or ccls in self.independent_classes:
                        self.true_negatives += 1
                        continue
                    if relation_cap and self.can_parent_can_contain_any_class(cls, relation_cap):
                        self.true_negatives += 1
                        continue
                    if cls not in parent_classes or ccls not in child_classes: # BUG HERE
                        if ignore_unseen_classes:
                            if include_warnings:
                                warning = 'Warning in line {} ---> Parent: {} has not been trained to have a relation to child: {}'.format(
                                    colored(source_line, 'magenta'), colored(cls, 'blue'), colored(ccls, 'blue'))
                                self.depths_of_errors.append(depth)
                                combined_errors.append(warning)
                            continue
                        if parent_level_errors and parent_line_numbers:
                            if parent_line_number not in self.parent_level_errors_dict:
                                self.parent_level_errors_dict[parent_line_number] = [
                                    '                  ---> Parent: {} has not been trained to have a relation to child: {} which is on line {}:{} and depth {}'.format(
                                        colored(cls, 'blue',),
                                        colored(ccls, 'blue'),
                                        colored(source_line, 'cyan'),
                                        colored(source_pos, 'blue'),
                                        colored(depth, 'red')
                                    )
                                ]
                                self.plain_parent_level_errors_dict[parent_line_number] = [
                                    '                  ---> Parent: {} has not been trained to have a relation to child: {} which is on line {}:{} and depth {}'.format(
                                        cls,
                                        ccls,
                                        source_line,
                                        source_pos,
                                        depth,
                                    )
                                ]
                                self.true_positives += 1
                            else:
                                self.parent_level_errors_dict[parent_line_number].append(
                                    '                  ---> Parent: {} has not been trained to have a relation to child: {} which is on line {}:{} and depth {}'.format(
                                        colored(cls, 'blue', ),
                                        colored(ccls, 'blue'),
                                        colored(source_line, 'cyan'),
                                        colored(source_pos, 'blue'),
                                        colored(depth, 'red')
                                    )
                                )
                                self.plain_parent_level_errors_dict[parent_line_number].append(
                                    '                  ---> Parent: {} has not been trained to have a relation to child: {} which is on line {}:{} and depth {}'.format(
                                        cls,
                                        ccls,
                                        source_line,
                                        source_pos,
                                        depth,
                                    )
                                )
                                self.true_positives += 1

                        error = 'Error in line {} ---> Parent: {} at line: {} has not been trained to have a relation to child: {}'.format(colored(source_line, 'red'), colored(cls, 'blue'), colored(parent_line_number, 'cyan'), colored(ccls, 'blue'))
                        # print(error)
                        # return False, error
                        self.depths_of_errors.append(depth)
                        combined_errors.append(error)
                    else:
                        if depth_cap and depth > depth_cap:
                            self.true_negatives += 1
                            continue
                        if fine_relations.get(cls, {}).get(ccls, {}) == "*":
                            # print('Success! Line--->: {}  Parent: {} has relation to child: {} at depth: {} because depth = "*"'.format(
                            #         source_line, cls,
                            #         ccls, depth))
                            self.true_negatives += 1
                            pass
                        else:
                            if depth not in fine_relations.get(cls, {}).get(ccls, {}):
                                error = 'Error in line {} ---> Parent: {} at line: {} has not been trained to have a relation to child: {} at depth: {}. Depths encountered: {}'.format(
                                    colored(source_line, 'red'), colored(cls, 'blue'), colored(parent_line_number, 'cyan'), colored(ccls, 'blue'), colored(depth, 'red'), colored(fine_relations.get(cls, {}).get(ccls, {}), 'green'))
                                # print(error)
                                self.depths_of_errors.append(depth)
                                combined_errors.append(error)
                                neural_network_list.append([
                                    source_line,
                                    cls,
                                    ccls,
                                    depth
                                ])
                                if parent_level_errors and parent_line_numbers:
                                    if parent_line_number not in self.parent_level_errors_dict:
                                        self.parent_level_errors_dict[parent_line_number] = [
                                            '                  ---> Parent: {} has not been trained to have a relation to child: {} which is on line {}:{} and depth {}. Depths encountered during training: {}'.format(
                                                colored(cls, 'blue', ),
                                                colored(ccls, 'blue'),
                                                colored(source_line, 'cyan'),
                                                colored(source_pos, 'blue'),
                                                colored(depth, 'red'),
                                                colored(fine_relations.get(cls, {}).get(ccls, None), 'yellow')
                                            )
                                        ]
                                        self.plain_parent_level_errors_dict[parent_line_number] = [
                                            '                  ---> Parent: {} has not been trained to have a relation to child: {} which is on line {}:{} and depth {}. Depths encountered during training: {}'.format(
                                                cls,
                                                ccls,
                                                source_line,
                                                source_pos,
                                                depth,
                                                fine_relations.get(cls, {}).get(ccls, None)
                                            )
                                        ]
                                        self.true_positives += 1
                                    else:
                                        self.parent_level_errors_dict[parent_line_number].append(
                                            '                  ---> Parent: {} has not been trained to have a relation to child: {} which is on line {}:{} and depth {}. Depths encountered during training: {}'.format(
                                                colored(cls, 'blue', ),
                                                colored(ccls, 'blue'),
                                                colored(source_line, 'cyan'),
                                                colored(source_pos, 'blue'),
                                                colored(depth, 'red'),
                                                colored(fine_relations.get(cls, {}).get(ccls, None), 'yellow')
                                            )
                                        )
                                        self.plain_parent_level_errors_dict[parent_line_number].append(
                                            '                  ---> Parent: {} has not been trained to have a relation to child: {} which is on line {}:{} and depth {}. Depths encountered during training: {}'.format(
                                                cls,
                                                ccls,
                                                source_line,
                                                source_pos,
                                                depth,
                                                fine_relations.get(cls, {}).get(ccls, None)
                                            )
                                        )
                                        self.true_positives += 1

                            else:
                                # print('Success! Line--->: {}  Parent: {} has relation to child: {} at depth: {}'.format(source_line, cls,
                                #                                                                       ccls, depth))
                                self.true_negatives += 1
                                pass


        if combined_errors:
            return False, combined_errors
        return True, ''

    def store_test_data_parent_children_relation(self, immediate_parent_list, child_class):
        for cls in immediate_parent_list:
            if cls not in self.global_test_data_parent_children_dict:
                self.global_test_data_parent_children_dict[cls] = set(child_class)
            else:
                for ccls in child_class:
                    self.global_test_data_parent_children_dict[cls].add(ccls)
        return

    def compare_child_and_its_parents_with_db(self, child_tuple, parents_list, source_line, allow_fine_relations, ignore_unseen_classes, include_warnings, depth_cap, parent_line_numbers, parent_level_errors, relation_cap, source_pos):
        fine_relations_exists, errors = self.compare_child_with_parents_list_fine_relations(child_tuple, parents_list, source_line, ignore_unseen_classes, include_warnings, depth_cap, parent_line_numbers, parent_level_errors, relation_cap, source_pos)
        if not fine_relations_exists:
            self.line_number_with_errors.add(source_line)
            return False, '\n'.join(errors)
        else:
            return True, ''

    def get_line_number_errors(self):
        return self.line_number_with_errors

    def construct_fine_relations(self):
        if self.dumped_fine_relations:
            return self.dumped_fine_relations
        '''
            This is showing how many times we have seen a child in the big HTML tree ("occurences").
            Also shows how many times we have seen the parent of that child in those "occurences",
            as a dictionary ("parents") with key: "parent_name", value: "probability_of_presence_above_child"

            child_parents_dict = {
                ('a', 'x', 'y'): {
                    "parents": {
                        ('q', 'w'): 0.5,
                        ('b', 'z'): 0.7
                    },
                    "occurences": 2,
                    "encountered_parent_orders": [
                        [('a' 'b'), ('d', 'e')]
                    ]
                },
            }
        '''
        fine_relations = {}
        encountered_parent_orders = self.get_encountered_parent_orders_and_depths()
        for parent in encountered_parent_orders:
            if not parent:
                cls = str(parent)
                for child in encountered_parent_orders[parent]:
                    child_depth = encountered_parent_orders[parent][child]
                    for ccls in child:
                        if fine_relations.get(cls, ()):
                            if fine_relations[cls].get(ccls, ()):
                                if fine_relations[cls][ccls] == '*':
                                    continue
                                else:
                                    fine_relations[cls][ccls] = fine_relations[cls][ccls].union(child_depth)
                            else:
                                fine_relations[cls][ccls] = child_depth
                        else:
                            fine_relations[cls] = {ccls: child_depth}
            else:
                for cls in parent:
                    for child in encountered_parent_orders[parent]:
                        child_depth = encountered_parent_orders[parent][child]
                        for ccls in child:
                            if fine_relations.get(cls, ()):
                                if fine_relations[cls].get(ccls, ()):
                                    if fine_relations[cls][ccls] == '*':
                                        continue
                                    else:
                                        fine_relations[cls][ccls] = fine_relations[cls][ccls].union(child_depth)
                                else:
                                    fine_relations[cls][ccls] = child_depth
                            else:
                                fine_relations[cls] = {ccls: child_depth}

        if self.star_depth_threshold:
            for cls in fine_relations:
                for ccls in fine_relations[cls]:
                    if len(fine_relations[cls][ccls]) >= self.star_depth_threshold:
                        fine_relations[cls][ccls] = '*'
                    else:
                        if fine_relations[cls][ccls] == '*':
                            continue
                        else:
                            fine_relations[cls][ccls] = list(fine_relations[cls][ccls])
        return fine_relations


    def print_parent_level_errors(self):
        errors = self.parent_level_errors_dict
        plain_errors = self.plain_parent_level_errors_dict
        ordered_plain_errors = dict(sorted(plain_errors.items()))
        ordered_errors = dict(sorted(errors.items()))
        all_errors = 0
        print('\n')
        for pln, lst in ordered_errors.items():
            initial_line = 'Error in line {} ---|\n'.format(colored(pln, 'red'))
            cprint(initial_line + '\n'.join(lst))
            all_errors += len(lst)
        cprint('Number of "parent line number" errors = {}'.format(colored(len(ordered_errors), 'red')))
        cprint('Number of Total errors = {}'.format(colored(all_errors, 'red')))
        return ordered_plain_errors


    def dump_rules(self, filename="rules.json"):
        fine_relations = self.construct_fine_relations()
        with open(filename, 'w') as fp:
            json.dump(fine_relations, fp, indent=4)
        return

    def load_rules(self, filename="rules.json"):
        with open(filename) as json_file:
            rules = json.load(json_file)
        return rules


