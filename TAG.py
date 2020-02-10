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
                    flag = True
                    for i in range(1, self.star_depth_threshold + 1):
                        if i not in parent_child_depth_relation[cls][ccls]:
                            flag = False
                            break
                    if flag:
                        parent_child_depth_relation[cls][ccls] = '*'
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

    def compare_child_with_parents_list_fine_relations(self, child_tuple, parents_list, source_line):
        combined_errors = []
        fine_relations = self.construct_fine_relations()
        for ccls in child_tuple:
            for depth, parent in enumerate(parents_list):
                depth += 1
                for cls in parent:
                    if not fine_relations.get(cls, {}).get(ccls, {}):
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
                                error = 'Error in line: {};  Parent: {} has no relation to child: {} at depth: {}'.format(
                                    source_line, cls, ccls, depth)
                                # print(error)
                                combined_errors.append(error)
                            else:
                                # print('Success! Line--->: {}  Parent: {} has relation to child: {} at depth: {}'.format(source_line, cls,
                                #                                                                       ccls, depth))
                                pass
        if combined_errors:
            return False, combined_errors
        return True, ''



    def compare_child_and_its_parents_with_db(self, child_tuple, parents_list, source_line, allow_fine_relations=False):
        stored_children = self.child_parents_dict.keys()
        # stored_orders = self.child_parents_dict[child_tuple]["encountered_parent_orders"]
        found = False

        if allow_fine_relations:
            fine_relations_exists, errors = self.compare_child_with_parents_list_fine_relations(child_tuple, parents_list, source_line)
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

        bootstrap_4_rules = {'input-group', 'dropright', 'rounded', 'border-light', 'dropdown-item-text', 'navbar-toggler', 'carousel-fade', 'nav-pills with dropdown', 'mw-100', 'card-body', 'form-group', 'custom-radio', 'card-subtitle', 'col-lg-[0-9]+', 'btn-group', 'text-nowrap', 'pb-.*-[0-9]+', 'list-group-item-success', 'p-1', 'bg-info', 'dropup', 'form using the grid', 'table-info', 'custom-range', 'navbar-expand-.*', 'radio', 'text-monospace', 'd-.*-none', 'rounded-.*', 'active button', 'card-img-overlay', 'tooltip', 'fixed-bottom', 'form-control-file', 'badge-primary', 'nav-fill', 'card-img-bottom', 'border-dark', 'nav flex-column', 'mx-1', 'align-self-.*-start', 'm-.*-n[0-9]+', 'custom-switch', 'rounded-0', 'spinner-grow-sm', 'list-group-item active', 'pt-.*-[0-9]+', 'form-control-plaintext', 'text-lowercase', 'table-bordered', 'border-success', 'mh-100', 'text-decoration-none', 'list-group with d-flex', 'dropleft', 'pr-.*-[0-9]+', 'badge-secondary', 'page-item active', 'spinner-border text-.*', 'nav-tabs', 'dropdown-menu-right', 'table', 'alert-dismissible', 'card-columns', 'thead-dark', 'no-gutters', 'order-.*-[0-9]+', 'align-items-.*-stretch', 'bg-dark', 'text-muted', 'checkbox', 'border-.*-0', 'list-group-item-warning', 'modal-dialog-centered', 'card-header', 'font-weight-lighter', 'text-white-50', 'navbar-brand', 'list-group-item-secondary', 'custom-checkbox', 'nav.nav', 'card-text', 'd-flex align-self-center', 'flex-.*-column-reverse', 'card-title', 'text-dark', 'float-.*-none', 'middle image', 'pagination', 'font-italic', 'col-[0-9]+', 'alert-danger', 'progress-bar bg-.*', 'container-fluid', 'progress-bar with label', 'alert-light', 'badge-warning', 'readonly', 'progress-bar-striped bg-.*', 'list-group-item-light', 'shadow-none', 'btn-dark', 'table-hover', 'alert-warning', 'm-1', 'btn-info', 'col-sm-[0-9]+', 'text-justify', 'nested media', 'btn-toolbar', 'dropdown-header', 'card bg-... text-...', 'justify-content-.*-around', 'card', 'text-white', 'dismissible popover', 'my-1', 'modal-dialog-scrollable', 'h.*.card-header', 'thead-light', 'float-.*-left', 'text-.*-right', 'ml-1', 'pagination-lg', 'blockquote-footer', 'align-self-.*-baseline', 'row', 'img-fluid', 'mb-1', 'align-self-.*-stretch', 'list-group-item disabled', 'list-group-item-dark', 'flex-.*-wrap-reverse', 'alert-success', 'progress-bar-animated', 'btn-secondary', 'text-success', 'table-sm', 'btn-warning', 'text-black-50', 'align-items-.*-start', 'text-.*-center', 'font-weight-bolder', 'spinner-border-sm', 'dl-horizontal', 'flex-fill', 'list-group', 'stretched-link', 'my-.*-[0-9]+', 'btn-link', 'blockquote-reverse', 'collapse navbar-collapse', 'align-content-.*-stretch', 'border-danger', 'accordion', 'nested columns', 'form-control', 'progress-bar', 'pb-1', 'bg-secondary', 'alert-secondary', 'navbar', 'badge-pill', 'navbar with form', 'invisible', 'btn-block', 'border-primary', 'form-inline', 'radio as button', 'right aligned media', 'mr-.*-[0-9]+', 'align-self-.*-center', 'popovers', 'btn-outline-success', 'align-self-.*-end', 'flex-.*-grow-0', 'close', 'card-deck', 'flex-.*-row-reverse', 'border-info', 'text-info', 'd-.*-inline-flex', 'bg-primary', 'btn-outline-danger', 'card-footer', 'font-weight-normal', 'col-xl-[0-9]+', 'input-group-sm', 'btn-group-sm', 'text-secondary', 'border-white', 'list-group-item-danger', 'table-dark', 'd-.*-flex', 'dropdown-item disabled', 'pagination-sm', 'text-break', 'progress', 'order-[0-9]+', 'shadow-sm', 'btn-outline-warning', 'text-truncate', 'flex-.*-shrink-1', 'blockquote', 'checkbox as button', 'navbar-dark bg-dark', 'mr-1', 'disabled items', 'progress-bar with height', 'font-weight-light', 'flex-.*-row', 'bg-success', 'text-.*-left', 'spinner-grow', 'table-borderless', 'img-thumbnail', 'font-weight-bold', 'display-[0-9]+', 'mx-.*-[0-9]+', 'form-check-inline', 'list-group-item-action', 'col-.*', 'table-.*-responsive', 'text-hide', 'list-group with badges', 'px-.*-[0-9]+', 'btn-outline-info', 'd-.*-block', 'navbar-text', 'p-.*-[0-9]+', 'text-capitalize', 'btn-lg', 'justify-content-.*-end', 'custom-select', 'mt-.*-[0-9]+', 'form-control-sm', 'custom-file', 'flex-.*-wrap', 'align-items-.*-baseline', 'shadow', 'pr-1', 'alert-dark', 'ul.nav', 'bg-warning', 'alert-info', 'btn-success', 'badge-success', 'sticky-top', 'm-n1', 'table-light', 'collapse', 'multiple progress-bar', 'text-uppercase', 'col', 'form-control-lg', 'visible', 'table-danger', 'list-group-item-info', 'pl-1', 'card-img-top', 'badge-dark', 'btn-danger', 'align-content-.*-end', 'pt-1', 'ml-.*-[0-9]+', 'nav-justified', 'fixed-top', 'align-content-.*-center', 'btn-group-lg', 'list-inline', 'lead', 'float-.*-right', 'bg-danger', 'py-.*-[0-9]+', 'border-secondary', 'sr-only-focusable', 'badge-light', 'd-.*-inline', 'dropdown', 'btn-outline-light', 'modal-xl', 'form-check', 'modal-sm', 'd-flex align-self-end', 'py-1', 'rounded-lg', 'spinner-grow text-.*', 'table-reflow', 'align-content-.*-start', 'form-control-range', 'border-warning', 'align-content-.*-around', 'h-100', 'nav-tabs with dropdown', 'sr-only', 'bg-light', 'd-flex align-self-start', 'badge-danger', 'btn-outline-primary', 'modal', 'mt-1', 'nav justify-content-.*', 'jumbotron', 'justify-content-.*-start', 'navbar fixed-top', 'table-primary', 'table-secondary', 'align-items-.*-center', 'segmented buttons', 'd-.*-inline-block', 'badge-info', 'nav-pills', 'breadcrumb', 'table-striped', 'carousel-caption', 'btn-group-vertical', 'data-spy', 'navbar-light', 'text-light', 'jumbotron-fluid', 'alert-link', 'carousel-indicators', 'table-success', 'rounded-circle', 'clearfix', 'progress-bar-striped', 'badge', 'card-group', 'text-danger', 'embed-responsive', 'flex-.*-column', 'navbar fixed-bottom', 'card-link', 'btn-light', 'table-warning', 'btn-primary', 'alert-primary', 'btn-sm', 'table-active', 'spinner-border', 'list-unstyled', 'text-primary', 'd-.*-table', 'col-md-[0-9]+', 'list-group-item-primary', 'pl-.*-[0-9]+', 'align-items-.*-end', 'nav with flex utils', 'w-100', 'd-.*-table-cell', 'input-group-append', 'offset-.*-[0-9]+', 'flex-.*-shrink-0', 'text-body', 'media', 'carousel slide', 'disabled button', 'shadow-lg', 'btn-outline-secondary', 'modal fade', 'input-group-prepend', 'bg-white', 'page-item disabled', 'list-group-horizontal', 'container', 'd-print-...', 'flex-.*-grow-1', 'input-group-lg', 'justify-content-.*-center', 'mb-.*-[0-9]+', 'align-.*', 'alert-heading', 'rounded-sm', 'btn-outline-dark', 'border', 'm-.*-[0-9]+', 'flex-.*-nowrap', 'modal-lg', 'toast', 'px-1', 'dropdown-divider', 'justify-content-.*-between', 'text-warning', 'navbar sticky-top'}
        rules_found = set()
        fine_relations = self.construct_fine_relations()
        for parent in fine_relations:
            for rule in bootstrap_4_rules:
                if re.match(rule, parent):
                    rules_found.add(rule)
        return rules_found


