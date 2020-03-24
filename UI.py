import PySimpleGUI as sg
from PySimpleGUI import Checkbox, OK, Text, Popup
import json

sg.theme('DarkBlue1')


class UserInterface():
    global_dict = {}

    def error_decode(self,error):
        '''Parent: {} has not been trained to have a relation to child: {} which is on line {} and depth {}'''
        parent_cls = error.split('Parent: ')[1].split(' ')[0].strip()
        child_cls = error.split('child: ')[1].split(' ')[0].strip()
        depth = error.split('depth ')[1].split('.')[0].strip()
        return parent_cls, child_cls, depth

    def present_errors(self, errors, rules_filename=None, star_depth_threshold=None):
        layout = []

        counter = 0
        for pln, lst in errors.items():
            initial_line = 'Error in line {} ---|\n'.format(pln)
            layout.append([Text(initial_line)])
            for err in lst:
                parent_cls, child_cls, depth = self.error_decode(err)
                self.global_dict[counter] = {
                    'parent_cls': parent_cls,
                    'child_cls': child_cls,
                    'depth': depth
                }
                counter += 1
                layout.append([Checkbox(err)])
            # layout.append([Checkbox('Error in line: {}'.format(pln))])


        layout.append([OK()])

        window = sg.Window('Linting Errors', resizable=True).Layout([[sg.Column(layout, size=(1200,1000), scrollable=True)]])
        button, values = window.Read()


        popup_string = ''
        if rules_filename:
            with open(rules_filename) as json_file:
                rules = json.load(json_file)
        for i, value in enumerate(values):
            if value:
                parent_cls = self.global_dict[i]['parent_cls']
                child_cls = self.global_dict[i]['child_cls']
                depth = int(self.global_dict[i]['depth'])

                string = 'Parent: {} is allowed to have a relation to child: {} at depth: {}'.format(
                    parent_cls,
                    child_cls,
                    depth
                )
                popup_string += string + '\n'
                print(string)

                if rules_filename:
                    child_relation = rules.get(parent_cls, {}).get(child_cls, {})
                    if child_relation:
                        if star_depth_threshold:
                            if len(child_relation) + 1 >= star_depth_threshold:
                                rules[parent_cls][child_cls] = '*'
                            else:
                                rules[parent_cls][child_cls].append(depth)
                    else:
                        if rules.get(parent_cls, {}):
                            rules[parent_cls][child_cls] = [depth]
                        else:
                            rules[parent_cls] = {
                                child_cls: [depth]
                            }
        if rules_filename:
            with open(rules_filename, 'w') as fp:
                json.dump(rules, fp, indent=4)



        Popup('The GUI returned:', button, popup_string)



        # Popup('The GUI returned:', button, values)
