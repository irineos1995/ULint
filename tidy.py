class TAG():
    child_parents_dict = {}
    THRESHOLD = 1
    line_number_with_errors = set()

    def __init__(self, threshold):
        self.child_parents_dict = {}
        self.THRESHOLD = threshold
        self.line_number_with_errors = set()

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


    def compare_child_and_its_parents_with_db(self, child_tuple, parents_list, source_line):
        stored_children = self.child_parents_dict.keys()
        # stored_orders = self.child_parents_dict[child_tuple]["encountered_parent_orders"]
        found = False

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
            return False, "Parents order does not exist!"

        else:
            return True, ""
        
            

    def get_data(self):
        for data in self.child_parents_dict:
            print(data, ":", self.child_parents_dict[data])
        # return self.child_parents_dict

    def get_line_number_errors(self):
        return self.line_number_with_errors

