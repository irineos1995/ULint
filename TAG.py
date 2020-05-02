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

        with open('configuration_file', 'r') as rfl:
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

    def remove_elements_below_threshold(self, child_tuple, list_of_tuples):
        '''
            list_of_list_of_tuples = [
                [
                    ('b',), ('line-gutter-backdrop',)
                ]
            ]
        '''
        parents_that_are_mandatory_due_to_threshold = []
        for p, prob in self.child_parents_dict[child_tuple]['parents'].items():
            if prob >= self.THRESHOLD:
                parents_that_are_mandatory_due_to_threshold.append(p)

        new_list = []
        new_list_of_tuples = []
        parents_and_probs = self.child_parents_dict[child_tuple]["parents"]
        for tpl in list_of_tuples:
            local_flag = False
            for parent_tuple in parents_and_probs:
                if self.equal_tuples(tpl, parent_tuple):
                    local_flag = True
                    if parents_and_probs[parent_tuple] >= self.THRESHOLD:
                        new_list_of_tuples.append(tpl)
                    break
            if not local_flag:
                new_list_of_tuples.append(tpl)
        for element in parents_that_are_mandatory_due_to_threshold:
            if element not in new_list_of_tuples:
                new_list_of_tuples += (element, )
        new_list.append(new_list_of_tuples)
        return tuple(new_list)

    def remove_elements_below_threshold_for_parents(self, child_tuple, list_of_tuples):
        '''
            list_of_list_of_tuples = [
                [
                    ('b',), ('line-gutter-backdrop',)
                ]
            ]
        '''
        parents_that_are_mandatory_due_to_threshold = []
        for p, prob in self.child_parents_dict[child_tuple]['parents'].items():
            if prob >= self.THRESHOLD:
                parents_that_are_mandatory_due_to_threshold.append(p)

        new_list = []
        new_list_of_tuples = []
        parents_and_probs = self.child_parents_dict[child_tuple]["parents"]
        for tpl in list_of_tuples:
            local_flag = False
            for parent_tuple in parents_and_probs:
                if self.equal_tuples(tpl, parent_tuple):
                    local_flag = True
                    if parents_and_probs[parent_tuple] >= self.THRESHOLD:
                        new_list_of_tuples.append(tpl)
                    break
            if not local_flag:
                new_list_of_tuples.append(tpl)
        new_list.append(new_list_of_tuples)
        return tuple(new_list)

    def child_and_given_parents_order_exists(self, child, parents_list):
        stored_orders = self.child_parents_dict[child]["encountered_parent_orders"]
        for order in stored_orders:
            if len(order) == len(parents_list):
                if len(order) == 1 and order[0] == ():
                    return True
                local_flag = True
                for i, class_tuple in enumerate(parents_list):
                    if not self.equal_tuples(class_tuple, order[i]):
                        local_flag = False
                        break
                if local_flag:
                    return True
        return False

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
            # if not self.seen_class(ccls) and ignore_unseen_classes:
            #     continue
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

    def seen_class(self, cls):
        regex_classes_found = self.get_distinct_fine_grain_classes()
        for regex in regex_classes_found:
            if re.match(regex, cls):
                return True
        return False

    def store_test_data_parent_children_relation(self, immediate_parent_list, child_class):
        for cls in immediate_parent_list:
            if cls not in self.global_test_data_parent_children_dict:
                self.global_test_data_parent_children_dict[cls] = set(child_class)
            else:
                for ccls in child_class:
                    self.global_test_data_parent_children_dict[cls].add(ccls)
        return

    def compare_child_and_its_parents_with_db(self, child_tuple, parents_list, source_line, allow_fine_relations, ignore_unseen_classes, include_warnings, depth_cap, parent_line_numbers, parent_level_errors, relation_cap, source_pos):
        stored_children = self.child_parents_dict.keys()
        # stored_orders = self.child_parents_dict[child_tuple]["encountered_parent_orders"]
        found = False

        if allow_fine_relations:
            fine_relations_exists, errors = self.compare_child_with_parents_list_fine_relations(child_tuple, parents_list, source_line, ignore_unseen_classes, include_warnings, depth_cap, parent_line_numbers, parent_level_errors, relation_cap, source_pos)
            if not fine_relations_exists:
                self.line_number_with_errors.add(source_line)
                return False, '\n'.join(errors)
            else:
                return True, ''

        # Base Case (if child exists)
        for child in stored_children:
            if self.equal_tuples(child, child_tuple):
                found = True
                child_tuple = child
                break

        if not found:
            self.line_number_with_errors.add(source_line)
            return False, "Class has not been trained!"

        net_stored_orders = [self.remove_elements_below_threshold(child_tuple, order) for order in self.child_parents_dict[child_tuple]["encountered_parent_orders"]]
        

        # Child has been found
        if not self.child_and_given_parents_order_exists(child_tuple, parents_list):
            net_parents_list = self.remove_elements_below_threshold_for_parents(child, parents_list)
        
            for order in net_stored_orders:
                if len(order) == len(net_parents_list):
                    if len(order) == 1 and order[0] == ():
                        return True, ""
                    local_flag = True
                    for i, class_tuple in enumerate(net_parents_list):
                        if not self.equal_tuples(class_tuple, order[i]):
                            local_flag = False
                            break
                    if local_flag:
                        return True, ""
            self.line_number_with_errors.add(source_line)
            # return False, "Parents order does not exist!"
            return False, ""

        else:
            return True, ""

    def get_data(self):
        for data in self.child_parents_dict:
            print(data, ":", self.child_parents_dict[data])
        # return self.child_parents_dict

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

    def get_distinct_fine_grain_classes(self):
        '''
            parent_child_depth_relation[parent] = {
                            child : {depth+1}
                        }
        '''

        bootstrap_4_rules = \
            {'rounded-top', 'input-group-append', 'initialism', 'carousel-control-next-icon', 'form-check',
             'align-self-.*-center', 'card-link', 'border-info', 'badge-light', 'alert', 'w-25', 'text-right',
             'needs-validation', 'd-none', 'custom-file-input', 'form-control-sm', 'btn-outline-primary', 'custom-range',
             'bg-secondary', 'modal-body', 'col-md-.*', 'dropdown-menu-right', 'align-content-end', 'pagination', 'h-75',
             'flex-grow-[0-1]+', '<li>', 'align-content-.*-center', 'alert-link', 'align-items-stretch',
             'align-content-.*-around', 'alert-warning', 'btn-outline-warning', 'input-group-text', 'carousel-indicators',
             'bg-dark', 'custom-select', 'h-25', 'list-group-flush', 'text-reset', 'form-control-range',
             'align-items-start', 'border-0', 'h1-h6', 'dropright', 'pr-[0-9]+', 'modal-xl', 'mx-[0-9]+', 'carousel-item',
             'd-.*-inline-flex', 'float-.*-left', 'bg-danger', 'navbar-dark', 'form-check-input', 'card-text',
             'carousel-caption', 'd-.*-table-cell', 'border-dark', 'card-subtitle', 'align-bottom', 'mb-.*-[0-9]+',
             'float-none', 'd-.*-inline', 'card-img-overlay', 'nav-item', 'valid-tooltip', 'input-lg', 'font-weight-light',
             'form-control-plaintext', 'card-info', 'align-content-.*-stretch', 'border-light', 'sr-only', 'table-bordered',
             'custom-control-inline', 'badge-danger', 'rounded-left', 'bg-warning', 'badge-secondary', 'my-[0-9]+',
             'align-self-.*-baseline', 'badge-info', 'alert-heading', 'modal-dialog-centered', 'modal-sm', 'badge-dark',
             'sr-only-focusable', '<tr>', 'col-sm-.*', 'tab-content', 'mark', 'no-gutters', 'card-columns', 'col-auto',
             'toast-header', 'align-items-baseline', 'border-right-0', 'list-group', 'align-self-.*-end', 'mx-.*-[0-9]+',
             'w-50', 'rounded-bottom', 'list-group-item-info', 'blockquote-footer', 'page-link', 'pl-[0-9]+',
             'card-img-bottom', 'btn-success', 'btn-group-lg', 'collapse', 'navbar-collapse', 'text-.*-left',
             'collapse', 'show', 'mx-auto', 'card-body', 'text-warning', 'display:block', 'card-group', 'card-header-pills',
             'd-table', 'flex-row-reverse', 'carousel', 'align-self-start', 'text-dark', 'container-.*', 'form-inline',
             'media', 'btn-toolbar', 'flex-column', 'm-[0-9]+', 'navnav-tabs', 'd-.*-inline-block', 'flex-.*-wrap',
             'flex-column-reverse', 'invisible', 'align-items-.*-center', 'nav-link', 'text-left',
             'align-items-.*-baseline', 'shadow-none', 'align-text-top', 'mt-[0-9]+', 'embed-responsive-item',
             'align-text-bottom', 'embed-responsive-3by4', 'navbar-brand', 'max-height', 'alert-light', 'input-group',
             'dropdown-item-text', 'd-inline-flex', 'ml-.*-[0-9]+', 'shadow', 'lead', 'visible', 'align-self-baseline',
             'btn-outline-info', 'card-success', 'btn-light', 'alert-success', 'custom-control', 'form-control',
             'thead-light', 'border-sm', 'btn-secondary', 'text-primary', 'col-.*', 'text-break', 'sticky-top',
             'flex-.*-row-reverse', 'thead-dark', 'btn-outline-dark', 'rounded-0', '<ul>', 'align-items-.*-start',
             'custom-file', 'rounded-right', 'img-fluid', 'border-primary', 'align-content-around', 'badge-pill',
             'progress', 'btn-outline-light', 'text-decoration-none', 'list-inline', 'table-responsive-.*', '<ol>',
             'align-self-.*-start', 'btn-primary', 'img-thumbnail', 'py-.*-[0-9]+', 'mr-[0-9]+', 'align-items-end',
             'card-header-tabs', 'small', 'container', 'flex-.*-fill', 'flex-.*-nowrap', 'color:inherit', 'col-xl-.*',
             'card-danger', 'text-light', 'badge-primary', 'spinner-border', 'col-lg-.*', 'w-100', 'progress-bar',
             'pl-.*-[0-9]+', 'jumbotron', 'dropup', 'list-group-horizontal', 'custom-control-label',
             'flex-.*-column-reverse', 'alert-secondary', 'btn-sm', 'justify-content-.*-around', 'w-75', 'active', 'btn-lg',
             'flex-shrink-[0-1]+', 'd-.*-flex', 'h-50', 'dropdown-header', 'bg-primary', 'border-secondary',
             'custom-select-sm', 'flex-.*-row', 'custom-file-label', 'p-[0-9]+', 'card-img-top', 'd-.*-table',
             'pagination-sm', 'navnav-pills', 'custom-radio', 'breadcrumb', 'flex-row', 'form-control-file',
             'align-self-.*-stretch', 'border', 'pre-scrollable', 'border-left-0', 'badge-success', 'fixed-bottom',
             'form-check-label', 'list-group-item-dark', 'modal-header', 'card', 'font-weight-lighter', 'valid-feedback',
             'card-dark', 'list-inline-item', 'rounded', 'row-cols-.*', 'align-items-.*-stretch', 'btn-group-sm',
             'd-.*-table-row', 'flex-wrap-reverse', 'rounded-circle', 'progress-bar-striped', 'pr-.*-[0-9]+',
             'justify-content-.*-start', 'list-group-item-light', 'modal-dialog-scrollable', 'text-capitalize',
             'navbar-nav', 'modal-content', 'float-left', 'fade', 'text-center', '<pre>', 'btn-link', 'spinner-border-sm',
             'table-striped', 'carousel-control-prev', 'text-justify', 'dropdown-menu', 'my-.*-[0-9]+', 'pt-.*-[0-9]+',
             'h-100', 'text-secondary', 'text-.*-right', 'toast-body', 'card-secondary', 'clearfix', 'dropdown-item',
             'badge-warning', 'table-active', 'alert-primary', 'input-sm', 'align-middle', 'text-uppercase', 'bg-info',
             'border-bottom-0', 'table-hover', 'form-group', 'p-.*-[0-9]+', 'navbar-light', 'is-invalid',
             'align-content-stretch', 'text-nowrap', 'jumbotron-fluid', 'align-content-.*-start',
             'list-group-horizontal-.*', 'modal-lg', 'text-white', 'border-danger', '<abbr>', 'align-self-center',
             'text-hide', 'text-muted', 'fixed-top', 'nav-justified', 'd-table-row', 'list-group-item-success', 'mb-[0-9]+',
             'pb-[0-9]+', 'card-title', 'list-group-item-warning', 'modal-footer', 'table', 'navbar-text',
             'container-fluid', 'is-valid', 'alert-dark', 'embed-responsive', 'btn-group-vertical', 'float-.*-right',
             'navbar-toggler', 'text-danger', 'text-success', 'carousel-control-prev-icon', 'flex-nowrap', 'py-[0-9]+',
             'embed-responsive-16by9', 'font-italic', 'btn', 'card-header', 'btn-dark', 'align-self-stretch', 'btn-block',
             'flex-.*-wrap-reverse', 'text-lowercase', 'card-footer', 'list-group-item-action', 'btn-outline-danger',
             'width:100%', 'px-.*-[0-9]+', 'btn-outline-success', 'invalid-feedback', 'align-self-end',
             'custom-control-input', 'border-lg', 'dropleft', 'justify-content-.*', 'px-[0-9]+', 'pagination-lg', 'd-block',
             'flex-fill', 'justify-content-.*-center', 'navbar-expand-.*', 'shadow-lg', 'alert-dismissible', 'd-table-cell',
             'card-primary', 'stretched-link', 'list-group-item-primary', 'bg-light', 'alert-danger', 'align-items-.*-end',
             'justify-content-.*-between', 'font-weight-bold', 'align-top', 'toast', 'dropdown-toggle', 'border-white',
             'input-group-prepend', 'list-group-item', 'btn-group', 'list-group-item-danger', 'bg-success',
             'align-content-.*-end', 'btn-warning', 'd-.*-none', 'shadow-sm', 'input-group-sm', 'align-content-start',
             'mr-.*-[0-9]+', 'was-validated', 'text-.*-center', 'margin-top:-375rem;margin-bottom:0;', 'align-items-center',
             'custom-checkbox', '.*', 'flex-wrap', 'list-unstyled', 'carousel-inner', 'border-top-0', 'custom-switch',
             'page-item', 'align-baseline', 'disabled', 'btn-info', 'form-control-lg', 'flex-.*-column', 'm-.*-[0-9]+',
             'progress-bar-animated', 'badge', 'alert-info', 'font-weight-normal', 'tab-pane', 'close', 'card-deck',
             'dropdown', 'navbar', 'spinner-grow-sm', 'table-dark', 'pt-[0-9]+', 'd-.*-block', 'ml-[0-9]+',
             'breadcrumb-item', 'card-warning', 'align-content-center', 'custom-select-lg', 'table-borderless',
             'media-body', 'blockquote', 'justify-content-.*-end', 'border-success', 'font-weight-bolder',
             'carousel-control-next', 'card-light', 'float-right', 'row', 'text-info', 'form-check-inline', 'd-flex',
             'd-inline', 'table-condensed', '<td>', 'mt-.*-[0-9]+', 'modal', 'dropdown-divider', 'invalid-tooltip',
             'btn-outline-secondary', 'input-group-lg', 'spinner-grow', 'border-warning', 'd-inline-block', 'btn-danger',
             'form-row', 'pb-.*-[0-9]+'}

        # bootstrap_4_rules = ['row', 'align-self-end', 'navbar-brand', 'toast', 'navbar-dark', 'btn-outline-dark', 'badge-warning', 'spinner-border', 'form-control-file', 'py-1', 'form-control-sm', 'text-.*-center', 'custom-checkbox', 'align-content-.*-start', 'image', 'list-group-item-action', 'alert-light', 'table-secondary', 'd-.*-none', 'col-lg-[0-9]+', 'middle', 'card-img-bottom', 'align-self-.*-start', 'popovers', 'border-info', 'font-weight-lighter', 'page-item', 'card-group', 'container', 'bg-info', 'list-group-item-warning', 'd-.*-table', 'bg-warning', 'nav.nav', 'clearfix', 'visible', 'img-fluid', 'shadow', 'collapse', 'text-success', 'modal-xl', 'card-link', 'flex-.*-column', 'flex-column', 'spinner-grow', 'sr-only-focusable', 'text-warning', 'align-content-.*-around', 'flex-.*-grow-0', 'progress-bar-striped', 'rounded', 'pt-.*-[0-9]+', 'bg-white', 'btn-primary', 'list-group-item-dark', 'nav-tabs', 'blockquote-reverse', 'dismissible', 'btn-secondary', 'alert-info', 'popover', 'embed-responsive', 'bg-.*', 'badge-dark', 'nested', 'font-italic', 'font-weight-normal', 'alert-danger', 'list-group-item-secondary', 'text-primary', 'spinner-grow-sm', 'flex-.*-shrink-0', 'form-control', 'btn-group-sm', 'list-group-item', 'border-white', 'btn-group-lg', 'card-header', 'col-.*', 'list-group-item-success', 'flex-.*-wrap-reverse', 'align-.*', 'align-items-.*-end', 'h-100', 'button', 'table-success', 'align-items-.*-baseline', 'pb-1', 'align-content-.*-stretch', 'btn-dark', 'table-active', 'progress-bar', 'text-body', 'border-success', 'list-unstyled', 'mx-.*-[0-9]+', 'p-1', 'form-check-inline', 'jumbotron-fluid', 'mw-100', 'items', 'badge-light', 'align-self-.*-stretch', 'shadow-lg', 'dropdown-header', 'invisible', 'custom-range', 'my-1', 'border-danger', 'mx-1', 'container-fluid', 'blockquote-footer', 'text-nowrap', 'badges', 'mr-.*-[0-9]+', 'd-print-...', 'table-sm', 'btn-outline-warning', 'ml-1', 'progress-bar-animated', 'flex-.*-row', 'm-1', 'd-.*-inline', 'form-check', 'float-.*-none', 'readonly', 'alert-heading', 'float-.*-left', 'align-self-start', 'order-[0-9]+', 'carousel-fade', 'text-dark', 'navbar', 'btn-light', 'dropdown-divider', 'shadow-none', 'alert-warning', 'navbar-expand-.*', 'dl-horizontal', 'col-[0-9]+', 'py-.*-[0-9]+', 'grid', 'btn-block', 'table-danger', 'table-borderless', 'list-group-item-primary', 'p-.*-[0-9]+', 'border-warning', 'spinner-border-sm', 'alert-secondary', 'd-flex', 'mt-1', 'carousel-caption', 'offset-.*-[0-9]+', 'custom-file', 'custom-select', 'text-...', 'stretched-link', 'label', 'pr-1', 'input-group-append', 'badge-secondary', 'list-group-item-danger', 'blockquote', 'align-self-.*-baseline', 'pr-.*-[0-9]+', 'badge-success', 'the', 'table-hover', 'table', 'px-1', 'btn-outline-info', 'btn-outline-danger', 'btn-info', 'text-secondary', 'btn-lg', 'text-break', 'bg-danger', 'align-content-.*-end', 'card-footer', 'order-.*-[0-9]+', 'rounded-0', 'card-img-top', 'thead-light', 'sr-only', 'alert-success', 'btn-link', 'border-light', 'font-weight-light', 'my-.*-[0-9]+', 'text-lowercase', 'display-[0-9]+', 'flex-.*-row-reverse', 'list-group', 'btn-outline-light', 'using', 'form-control-plaintext', 'card', 'badge-pill', 'col-md-[0-9]+', 'flex-.*-grow-1', 'mb-.*-[0-9]+', 'fade', 'align-content-.*-center', 'input-group-sm', 'text-info', 'form', 'btn-sm', 'dropdown', 'align-items-.*-start', 'btn-danger', 'btn-group', 'fixed-top', 'fixed-bottom', 'alert-dark', 'mb-1', 'flex-.*-column-reverse', 'bg-success', 'd-.*-inline-flex', 'aligned', 'sticky-top', 'breadcrumb', 'align-self-center', 'list-group-horizontal', 'columns', 'active', 'ml-.*-[0-9]+', 'with', 'border-dark', 'close', 'btn-toolbar', 'text-justify', 'badge-danger', 'float-.*-right', 'flex-.*-nowrap', 'border-secondary', 'border-primary', 'as', 'navbar-collapse', 'pl-.*-[0-9]+', 'mt-.*-[0-9]+', 'custom-switch', 'card-title', 'modal', 'navbar-toggler', 'card-text', 'img-thumbnail', 'badge-info', 'btn-group-vertical', 'modal-lg', 'align-items-.*-stretch', 'justify-content-.*-start', 'rounded-.*', 'text-capitalize', 'align-self-.*-center', 'text-white', 'text-truncate', 'navbar-light', 'modal-dialog-centered', 'align-items-.*-center', 'flex-fill', 'bg-...', 'dropup', 'pb-.*-[0-9]+', 'badge-primary', 'list-group-item-light', 'form-group', 'right', 'table-light', 'px-.*-[0-9]+', 'list-inline', 'text-.*', 'card-img-overlay', 'form-inline', 'text-white-50', 'btn-warning', 'alert-dismissible', 'table-bordered', 'justify-content-.*', 'alert-primary', 'text-decoration-none', 'form-control-lg', 'w-100', 'shadow-sm', 'utils', 'justify-content-.*-end', 'radio', 'table-primary', 'card-columns', 'tooltip', 'col', 'm-.*-n[0-9]+', 'pl-1', 'border-.*-0', 'accordion', 'modal-dialog-scrollable', 'd-.*-flex', 'rounded-lg', 'd-.*-table-cell', 'slide', 'justify-content-.*-center', 'dropdown-menu-right', 'buttons', 'font-weight-bold', 'bg-secondary', 'input-group', 'm-.*-[0-9]+', 'pt-1', 'table-warning', 'data-spy', 'jumbotron', 'font-weight-bolder', 'alert-link', 'card-subtitle', 'table-info', 'dropdown-item', 'modal-sm', 'pagination-lg', 'segmented', 'btn-success', 'flex', 'm-n1', 'rounded-circle', 'text-muted', 'lead', 'form-control-range', 'text-.*-right', 'flex-.*-wrap', 'input-group-lg', 'justify-content-.*-between', 'card-deck', 'flex-.*-shrink-1', 'carousel-indicators', 'card-body', 'dropleft', 'height', 'col-sm-[0-9]+', 'col-xl-[0-9]+', 'border', 'mr-1', 'text-hide', 'navbar-text', 'list-group-item-info', 'mh-100', 'bg-light', 'text-light', 'no-gutters', 'disabled', 'checkbox', 'pagination-sm', 'progress', 'h.*.card-header', 'multiple', 'nav', 'align-self-.*-end', 'carousel', 'nav-pills', 'table-.*-responsive', 'ul.nav', 'text-.*-left', 'table-dark', 'bg-dark', 'custom-radio', 'text-uppercase', 'badge', 'nav-justified', 'text-black-50', 'bg-primary', 'pagination', 'justify-content-.*-around', 'text-danger', 'btn-outline-success', 'dropdown-item-text', 'thead-dark', 'rounded-sm', 'd-.*-inline-block', 'dropright', 'btn-outline-primary', 'text-monospace', 'table-reflow', 'nav-fill', 'media', 'd-.*-block', 'input-group-prepend', 'table-striped', 'btn-outline-secondary']
        rules_found = set()
        fine_relations = self.construct_fine_relations()
        for parent in fine_relations:
            for rule in bootstrap_4_rules:
                if re.match(rule, parent):
                    rules_found.add(rule)
            for child in fine_relations[parent]:
                for rule in bootstrap_4_rules:
                    if re.match(rule, child):
                        rules_found.add(rule)
        return rules_found


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

    def create_documentation(self, filename="documentation.html"):
        html_string_all = ''
        html_string_start = '''<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>*{box-sizing: border-box;}#myInput{background-image: url('/css/searchicon.png');background-position: 10px 10px;background-repeat: no-repeat;width: 100%;font-size: 16px;padding: 12px 20px 12px 40px;border: 1px solid #ddd;margin-bottom: 12px;}#myTable{border-collapse: collapse;width: 100%;border: 1px solid #ddd;font-size: 18px;}#myTable th, #myTable td{text-align: left;padding: 12px;}#myTable tr{border-bottom: 1px solid #ddd;}#myTable tr.header, #myTable tr:hover{background-color: #f1f1f1;}.collapsible{background-color: #777;color: white;cursor: pointer;padding: 18px;width: 100%;border: none;text-align: left;outline: none;font-size: 15px;}.active, .collapsible:hover{background-color: #555;}.content{padding: 0 18px;display: none;overflow: hidden;background-color: #f1f1f1;}ul.b{list-style-type: square;}</style></head><body><h2>CSS Class relations</h2><input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search for CSS classes.." title="Type in a name"><table id="myTable"><tr class="header"> <th style="width:60%;">CSS Class</th> <th style="width:40%;">Descendants</th></tr>''' 
        html_string_end = '''</table><script>function myFunction(){var input, filter, table, tr, td, i, txtValue;input=document.getElementById("myInput");filter=input.value.toUpperCase();table=document.getElementById("myTable");tr=table.getElementsByTagName("tr");for (i=0; i < tr.length; i++){td=tr[i].getElementsByTagName("td")[0]; if (td){txtValue=td.textContent || td.innerText; if (txtValue.toUpperCase().indexOf(filter) > -1){tr[i].style.display="";}else{tr[i].style.display="none";}}}}var coll=document.getElementsByClassName("collapsible");var i;for (i=0; i < coll.length; i++){coll[i].addEventListener("click", function(){this.classList.toggle("active"); var content=this.nextElementSibling; if (content.style.display==="block"){content.style.display="none";}else{content.style.display="block";}});}</script></body></html>'''
        row_string = '''<tr><td>{cls_name}</td><td><button type="button" class="collapsible">See descendants</button><div class="content"><ul class="b">{classes}</ul></div></td></tr>'''
        fine_relations = self.construct_fine_relations()
        table_string = ''
        
        for cls_name, descendants in fine_relations.items():
            classes_string = ''
            for desc in descendants:
                classes_string += '<li><span style="color: green">{}</span> --- Valid depths: <span style="color: blue">{}</span></li>'.format(desc, descendants[desc])
            table_string += row_string.format(cls_name=cls_name, classes=classes_string)
        html_string_all = html_string_start + table_string + html_string_end

        with open(filename, 'w+') as outfl:
            outfl.write(html_string_all)
        return

