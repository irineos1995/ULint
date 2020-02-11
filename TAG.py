import re
class Relations():
    child_parents_dict = {}
    THRESHOLD = 1
    line_number_with_errors = set()
    star_depth_threshold = None

    def __init__(self, threshold, star_depth_threshold):
        self.child_parents_dict = {}
        self.THRESHOLD = threshold
        self.line_number_with_errors = set()
        self.star_depth_threshold = star_depth_threshold

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

    def compare_child_with_parents_list_fine_relations(self, child_tuple, parents_list, source_line, ignore_unseen_classes):
        combined_errors = []
        fine_relations = self.construct_fine_relations()
        for ccls in child_tuple:
            # if not self.seen_class(ccls) and ignore_unseen_classes:
            #     continue
            for depth, parent in enumerate(parents_list):
                depth += 1
                for cls in parent:
                    # if not self.seen_class(cls) and ignore_unseen_classes:
                    #     continue
                    if not fine_relations.get(cls, {}).get(ccls, {}):
                        if ignore_unseen_classes:
                            continue
                        error = 'Error in line: {};  Parent: {} has no relation to child: {}'.format(source_line, cls, ccls)
                        # print(error)
                        # return False, error
                        combined_errors.append(error)
                    else:
                        if fine_relations.get(cls, {}).get(ccls, {}) == "*":
                            # print('Success! Line--->: {}  Parent: {} has relation to child: {} at depth: {} because depth = "*"'.format(
                            #         source_line, cls,
                            #         ccls, depth))
                            pass
                        else:
                            if depth not in fine_relations.get(cls, {}).get(ccls, {}):
                                error = 'Error in line: {};  Parent: {} has no relation to child: {} at depth: {}. Depths encountered: {}'.format(
                                    source_line, cls, ccls, depth, fine_relations.get(cls, {}).get(ccls, {}))
                                # print(error)
                                combined_errors.append(error)
                            else:
                                # print('Success! Line--->: {}  Parent: {} has relation to child: {} at depth: {}'.format(source_line, cls,
                                #                                                                       ccls, depth))
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


    def compare_child_and_its_parents_with_db(self, child_tuple, parents_list, source_line, allow_fine_relations, ignore_unseen_classes):
        stored_children = self.child_parents_dict.keys()
        # stored_orders = self.child_parents_dict[child_tuple]["encountered_parent_orders"]
        found = False

        if allow_fine_relations:
            fine_relations_exists, errors = self.compare_child_with_parents_list_fine_relations(child_tuple, parents_list, source_line, ignore_unseen_classes)
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
                    flag = True
                    for i in range(1, self.star_depth_threshold + 1):
                        if fine_relations[cls][ccls] == "*":
                            continue
                        else:
                            if i not in fine_relations[cls][ccls]:
                                flag = False
                                break
                    if flag:
                        fine_relations[cls][ccls] = '*'


        # print('fine_relations ', fine_relations)
        return fine_relations

    def get_distinct_fine_grain_classes(self):
        '''
            parent_child_depth_relation[parent] = {
                            child : {depth+1}
                        }
        '''

        bootstrap_4_rules = ['row', 'align-self-end', 'navbar-brand', 'toast', 'navbar-dark', 'btn-outline-dark', 'badge-warning', 'spinner-border', 'form-control-file', 'py-1', 'form-control-sm', 'text-.*-center', 'custom-checkbox', 'align-content-.*-start', 'image', 'list-group-item-action', 'alert-light', 'table-secondary', 'd-.*-none', 'col-lg-[0-9]+', 'middle', 'card-img-bottom', 'align-self-.*-start', 'popovers', 'border-info', 'font-weight-lighter', 'page-item', 'card-group', 'container', 'bg-info', 'list-group-item-warning', 'd-.*-table', 'bg-warning', 'nav.nav', 'clearfix', 'visible', 'img-fluid', 'shadow', 'collapse', 'text-success', 'modal-xl', 'card-link', 'flex-.*-column', 'flex-column', 'spinner-grow', 'sr-only-focusable', 'text-warning', 'align-content-.*-around', 'flex-.*-grow-0', 'progress-bar-striped', 'rounded', 'pt-.*-[0-9]+', 'bg-white', 'btn-primary', 'list-group-item-dark', 'nav-tabs', 'blockquote-reverse', 'dismissible', 'btn-secondary', 'alert-info', 'popover', 'embed-responsive', 'bg-.*', 'badge-dark', 'nested', 'font-italic', 'font-weight-normal', 'alert-danger', 'list-group-item-secondary', 'text-primary', 'spinner-grow-sm', 'flex-.*-shrink-0', 'form-control', 'btn-group-sm', 'list-group-item', 'border-white', 'btn-group-lg', 'card-header', 'col-.*', 'list-group-item-success', 'flex-.*-wrap-reverse', 'align-.*', 'align-items-.*-end', 'h-100', 'button', 'table-success', 'align-items-.*-baseline', 'pb-1', 'align-content-.*-stretch', 'btn-dark', 'table-active', 'progress-bar', 'text-body', 'border-success', 'list-unstyled', 'mx-.*-[0-9]+', 'p-1', 'form-check-inline', 'jumbotron-fluid', 'mw-100', 'items', 'badge-light', 'align-self-.*-stretch', 'shadow-lg', 'dropdown-header', 'invisible', 'custom-range', 'my-1', 'border-danger', 'mx-1', 'container-fluid', 'blockquote-footer', 'text-nowrap', 'badges', 'mr-.*-[0-9]+', 'd-print-...', 'table-sm', 'btn-outline-warning', 'ml-1', 'progress-bar-animated', 'flex-.*-row', 'm-1', 'd-.*-inline', 'form-check', 'float-.*-none', 'readonly', 'alert-heading', 'float-.*-left', 'align-self-start', 'order-[0-9]+', 'carousel-fade', 'text-dark', 'navbar', 'btn-light', 'dropdown-divider', 'shadow-none', 'alert-warning', 'navbar-expand-.*', 'dl-horizontal', 'col-[0-9]+', 'py-.*-[0-9]+', 'grid', 'btn-block', 'table-danger', 'table-borderless', 'list-group-item-primary', 'p-.*-[0-9]+', 'border-warning', 'spinner-border-sm', 'alert-secondary', 'd-flex', 'mt-1', 'carousel-caption', 'offset-.*-[0-9]+', 'custom-file', 'custom-select', 'text-...', 'stretched-link', 'label', 'pr-1', 'input-group-append', 'badge-secondary', 'list-group-item-danger', 'blockquote', 'align-self-.*-baseline', 'pr-.*-[0-9]+', 'badge-success', 'the', 'table-hover', 'table', 'px-1', 'btn-outline-info', 'btn-outline-danger', 'btn-info', 'text-secondary', 'btn-lg', 'text-break', 'bg-danger', 'align-content-.*-end', 'card-footer', 'order-.*-[0-9]+', 'rounded-0', 'card-img-top', 'thead-light', 'sr-only', 'alert-success', 'btn-link', 'border-light', 'font-weight-light', 'my-.*-[0-9]+', 'text-lowercase', 'display-[0-9]+', 'flex-.*-row-reverse', 'list-group', 'btn-outline-light', 'using', 'form-control-plaintext', 'card', 'badge-pill', 'col-md-[0-9]+', 'flex-.*-grow-1', 'mb-.*-[0-9]+', 'fade', 'align-content-.*-center', 'input-group-sm', 'text-info', 'form', 'btn-sm', 'dropdown', 'align-items-.*-start', 'btn-danger', 'btn-group', 'fixed-top', 'fixed-bottom', 'alert-dark', 'mb-1', 'flex-.*-column-reverse', 'bg-success', 'd-.*-inline-flex', 'aligned', 'sticky-top', 'breadcrumb', 'align-self-center', 'list-group-horizontal', 'columns', 'active', 'ml-.*-[0-9]+', 'with', 'border-dark', 'close', 'btn-toolbar', 'text-justify', 'badge-danger', 'float-.*-right', 'flex-.*-nowrap', 'border-secondary', 'border-primary', 'as', 'navbar-collapse', 'pl-.*-[0-9]+', 'mt-.*-[0-9]+', 'custom-switch', 'card-title', 'modal', 'navbar-toggler', 'card-text', 'img-thumbnail', 'badge-info', 'btn-group-vertical', 'modal-lg', 'align-items-.*-stretch', 'justify-content-.*-start', 'rounded-.*', 'text-capitalize', 'align-self-.*-center', 'text-white', 'text-truncate', 'navbar-light', 'modal-dialog-centered', 'align-items-.*-center', 'flex-fill', 'bg-...', 'dropup', 'pb-.*-[0-9]+', 'badge-primary', 'list-group-item-light', 'form-group', 'right', 'table-light', 'px-.*-[0-9]+', 'list-inline', 'text-.*', 'card-img-overlay', 'form-inline', 'text-white-50', 'btn-warning', 'alert-dismissible', 'table-bordered', 'justify-content-.*', 'alert-primary', 'text-decoration-none', 'form-control-lg', 'w-100', 'shadow-sm', 'utils', 'justify-content-.*-end', 'radio', 'table-primary', 'card-columns', 'tooltip', 'col', 'm-.*-n[0-9]+', 'pl-1', 'border-.*-0', 'accordion', 'modal-dialog-scrollable', 'd-.*-flex', 'rounded-lg', 'd-.*-table-cell', 'slide', 'justify-content-.*-center', 'dropdown-menu-right', 'buttons', 'font-weight-bold', 'bg-secondary', 'input-group', 'm-.*-[0-9]+', 'pt-1', 'table-warning', 'data-spy', 'jumbotron', 'font-weight-bolder', 'alert-link', 'card-subtitle', 'table-info', 'dropdown-item', 'modal-sm', 'pagination-lg', 'segmented', 'btn-success', 'flex', 'm-n1', 'rounded-circle', 'text-muted', 'lead', 'form-control-range', 'text-.*-right', 'flex-.*-wrap', 'input-group-lg', 'justify-content-.*-between', 'card-deck', 'flex-.*-shrink-1', 'carousel-indicators', 'card-body', 'dropleft', 'height', 'col-sm-[0-9]+', 'col-xl-[0-9]+', 'border', 'mr-1', 'text-hide', 'navbar-text', 'list-group-item-info', 'mh-100', 'bg-light', 'text-light', 'no-gutters', 'disabled', 'checkbox', 'pagination-sm', 'progress', 'h.*.card-header', 'multiple', 'nav', 'align-self-.*-end', 'carousel', 'nav-pills', 'table-.*-responsive', 'ul.nav', 'text-.*-left', 'table-dark', 'bg-dark', 'custom-radio', 'text-uppercase', 'badge', 'nav-justified', 'text-black-50', 'bg-primary', 'pagination', 'justify-content-.*-around', 'text-danger', 'btn-outline-success', 'dropdown-item-text', 'thead-dark', 'rounded-sm', 'd-.*-inline-block', 'dropright', 'btn-outline-primary', 'text-monospace', 'table-reflow', 'nav-fill', 'media', 'd-.*-block', 'input-group-prepend', 'table-striped', 'btn-outline-secondary']
        rules_found = set()
        fine_relations = self.construct_fine_relations()
        for parent in fine_relations:
            for rule in bootstrap_4_rules:
                if re.match(rule, parent):
                    rules_found.add(rule)
        return rules_found

