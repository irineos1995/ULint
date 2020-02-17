import re
import csv
from termcolor import colored, cprint
from sklearn.neural_network import MLPClassifier
from random import *


class NeuralNetwork():
    training_data = []
    target_data = []

    classifier = None
    bootstrap_classes_and_int_representation = \
        {
            'btn-outline-success': 0, 'flex-column': 1, 'alert-dark': 2, 'bg-info': 3, 'flex-.*-fill': 4, 'alert-secondary': 5,
             'bg-dark': 6, 'img-fluid': 7, 'thead-dark': 8, 'd-table': 9, 'w-50': 10, 'font-weight-lighter': 11, 'border': 12,
             'h1-h6': 13, 'btn-group': 14, 'navbar': 15, 'my-[0-9]+': 16, 'd-.*-none': 17, 'row-cols-.*': 18, 'pagination-sm': 19,
             'border-dark': 20, 'font-weight-normal': 21, 'rounded-left': 22, 'flex-row-reverse': 23, 'list-group-item-dark': 24,
             'alert-danger': 25, 'align-content-stretch': 26, 'custom-radio': 27, 'badge-dark': 28, 'color:inherit': 29,
             '<li>': 30, 'bg-light': 31, 'custom-select': 32, 'form-check-inline': 33, 'float-.*-left': 34,
             'form-check-input': 35, 'container': 36, 'border-0': 37, 'justify-content-.*-end': 38, 'list-group-item-warning': 39,
             'input-group-sm': 40, 'align-items-.*-stretch': 41, 'modal-dialog-centered': 42, 'justify-content-.*-around': 43,
             'btn-link': 44, 'font-weight-bold': 45, 'input-group-text': 46, 'border-right-0': 47, 'mt-.*-[0-9]+': 48,
             'align-items-.*-end': 49, 'input-sm': 50, 'progress-bar-animated': 51, 'dropdown-header': 52, 'btn-outline-primary': 53,
             'page-link': 54, 'jumbotron-fluid': 55, 'text-secondary': 56, 'border-light': 57, 'text-justify': 58,
             'embed-responsive-16by9': 59, 'container-.*': 60, 'btn-block': 61, 'card-info': 62, 'text-uppercase': 63,
             'badge': 64, 'progress-bar': 65, 'align-self-stretch': 66, 'h-50': 67, 'text-right': 68, 'rounded-0': 69,
             'form-inline': 70, 'justify-content-.*-start': 71, 'thead-light': 72, 'card-link': 73, 'align-content-.*-stretch': 74,
             'btn-group-sm': 75, 'spinner-border-sm': 76, 'px-.*-[0-9]+': 77, 'list-group-item-danger': 78, 'align-middle': 79,
             'pre-scrollable': 80, 'd-inline-flex': 81, 'stretched-link': 82, 'badge-light': 83, 'mark': 84, 'float-.*-right': 85,
             'py-.*-[0-9]+': 86, 'modal': 87, 'needs-validation': 88, 'list-group-horizontal-.*': 89, 'list-group-item-success': 90,
             'form-control': 91, 'input-group-prepend': 92, 'text-.*-center': 93, 'align-items-.*-center': 94, 'border-danger': 95,
             'pt-[0-9]+': 96, 'carousel-caption': 97, 'table-responsive-.*': 98, 'navbar-light': 99, 'margin-top:-375rem;margin-bottom:0;': 100,
             'custom-control': 101, 'align-items-end': 102, 'align-text-top': 103, 'input-group-append': 104, 'float-none': 105, 'd-block': 106,
             'card-img-top': 107, 'list-group-item-action': 108, 'col-.*': 109, 'list-group-item-info': 110, 'col-md-.*': 111, 'alert': 112,
             'border-white': 113, 'form-control-range': 114, 'rounded-bottom': 115, 'custom-control-inline': 116, 'border-success': 117,
             'd-none': 118, 'valid-feedback': 119, 'py-[0-9]+': 120, 'carousel-control-prev': 121, 'mb-.*-[0-9]+': 122, 'carousel-inner': 123,
             'mx-auto': 124, 'btn-dark': 125, 'd-.*-table-row': 126, 'tab-content': 127, 'card-body': 128, 'list-group-item': 129,
             'card-img-overlay': 130, 'badge-warning': 131, 'show': 132, 'ml-[0-9]+': 133, 'carousel-indicators': 134, 'border-lg': 135,
             'modal-xl': 136, 'alert-warning': 137, 'width:100%': 138, '<ul>': 139, 'nav-link': 140, 'card': 141, 'text-hide': 142,
             'btn-group-lg': 143, 'btn-secondary': 144, 'rounded-top': 145, 'pr-[0-9]+': 146, 'flex-.*-nowrap': 147, '<td>': 148,
             'initialism': 149, 'pt-.*-[0-9]+': 150, 'card-header-tabs': 151, 'pl-.*-[0-9]+': 152, 'carousel-control-next': 153,
             'align-content-center': 154, 'rounded': 155, 'shadow-lg': 156, 'list-unstyled': 157, 'flex-grow-[0-1]+': 158,
             'float-right': 159, 'card-header': 160, 'navbar-dark': 161, 'modal-sm': 162, 'd-.*-block': 163, 'small': 164,
             'btn-lg': 165, 'fade': 166, 'table-striped': 167, 'modal-lg': 168, 'd-.*-inline-flex': 169, 'm-.*-[0-9]+': 170,
             'table-hover': 171, 'form-control-file': 172, 'form-control-plaintext': 173, 'btn-light': 174, 'rounded-right': 175,
             'align-items-center': 176, 'btn-group-vertical': 177, 'visible': 178, 'align-self-start': 179, 'col-auto': 180,
             'alert-primary': 181, 'my-.*-[0-9]+': 182, 'toast': 183, 'btn-warning': 184, 'invalid-tooltip': 185, 'text-left': 186,
             'toast-body': 187, '<ol>': 188, 'text-info': 189, 'text-break': 190, 'pl-[0-9]+': 191, 'dropdown-menu-right': 192,
             'clearfix': 193, 'btn-success': 194, 'rounded-circle': 195, 'text-reset': 196, 'img-thumbnail': 197, 'pagination': 198,
             'align-top': 199, 'align-self-center': 200, 'badge-danger': 201, 'jumbotron': 202, 'card-success': 203, 'flex-.*-row': 204,
             'dropleft': 205, 'btn-outline-dark': 206, 'border-top-0': 207, 'toast-header': 208, 'd-.*-flex': 209, 'text-capitalize': 210,
             'h-100': 211, 'btn': 212, 'align-content-.*-around': 213, 'navbar-text': 214, 'mt-[0-9]+': 215, 'blockquote': 216, 'd-flex': 217,
             'btn-danger': 218, 'list-group-item-light': 219, 'card-light': 220, 'spinner-border': 221, 'pb-.*-[0-9]+': 222, 'progress': 223,
             'navnav-tabs': 224, 'bg-success': 225, 'was-validated': 226, 'justify-content-.*-between': 227, 'p-.*-[0-9]+': 228, 'col-xl-.*': 229,
             'bg-danger': 230, 'list-inline': 231, 'input-lg': 232, 'justify-content-.*': 233, 'mr-.*-[0-9]+': 234, 'sticky-top': 235,
             'form-check-label': 236, 'align-content-.*-start': 237, 'dropdown-divider': 238, 'navbar-expand-.*': 239, 'navbar-nav': 240,
             'alert-info': 241, 'w-75': 242, 'progress-bar-striped': 243, 'btn-info': 244, 'btn-outline-light': 245, 'input-group': 246,
             'dropdown-toggle': 247, 'table-dark': 248, 'align-self-.*-center': 249, 'carousel-control-next-icon': 250, 'invalid-feedback': 251,
             'text-muted': 252, 'fixed-bottom': 253, 'invisible': 254, 'container-fluid': 255, 'flex-.*-row-reverse': 256, 'border-warning': 257,
             'custom-switch': 258, 'mb-[0-9]+': 259, 'btn-primary': 260, 'text-white': 261, 'table-bordered': 262, 'dropdown': 263,
             'pr-.*-[0-9]+': 264, 'd-table-cell': 265, 'flex-nowrap': 266, 'custom-file-label': 267, 'nav-justified': 268, 'card-warning': 269,
             'modal-body': 270, 'carousel-control-prev-icon': 271, 'blockquote-footer': 272, 'card-danger': 273, 'navnav-pills': 274,
             'col-lg-.*': 275, 'text-.*-right': 276, 'border-bottom-0': 277, 'form-control-sm': 278, 'align-items-stretch': 279,
             'is-invalid': 280, 'h-25': 281, 'align-content-start': 282, 'input-group-lg': 283, '<tr>': 284, 'nav-item': 285,
             'alert-dismissible': 286, 'card-dark': 287, 'dropright': 288, 'dropup': 289, 'pb-[0-9]+': 290, 'close': 291,
             'modal-footer': 292, 'embed-responsive': 293, 'h-75': 294, 'no-gutters': 295, 'text-decoration-none': 296,
             'text-light': 297, 'mr-[0-9]+': 298, 'align-baseline': 299, 'modal-header': 300, 'media-body': 301, 'btn-outline-info': 302,
             'custom-checkbox': 303, 'align-content-around': 304, 'list-group-item-primary': 305, 'custom-control-label': 306,
             'px-[0-9]+': 307, 'card-header-pills': 308, 'text-primary': 309, 'alert-light': 310, 'page-item': 311, 'w-25': 312,
             '<abbr>': 313, 'list-group-flush': 314, 'media': 315, 'card-title': 316, 'breadcrumb-item': 317, 'ml-.*-[0-9]+': 318,
             'p-[0-9]+': 319, 'list-group-horizontal': 320, 'btn-outline-secondary': 321, 'shadow-sm': 322, 'align-self-.*-end': 323,
             'card-img-bottom': 324, 'collapse': 325, 'alert-success': 326, 'align-self-baseline': 327, 'd-table-row': 328, 'flex-fill': 329,
             'text-warning': 330, 'custom-select-lg': 331, 'bg-secondary': 332, 'd-.*-table-cell': 333, 'm-[0-9]+': 334, 'align-self-.*-baseline': 335,
             'lead': 336, '.*': 337, 'form-row': 338, 'text-danger': 339, 'embed-responsive-3by4': 340, 'table-active': 341, 'align-content-.*-center': 342,
             'flex-wrap-reverse': 343, 'form-group': 344, 'col-sm-.*': 345, 'badge-pill': 346, 'align-items-start': 347, 'alert-link': 348,
             'carousel': 349, 'shadow-none': 350, 'custom-control-input': 351, 'table-borderless': 352, 'badge-success': 353,
             'text-center': 354, 'd-.*-table': 355, 'row': 356, 'spinner-grow': 357, 'align-content-end': 358, 'border-info': 359,
             'bg-warning': 360, 'carousel-item': 361, 'tab-pane': 362, 'text-dark': 363, 'align-items-baseline': 364, 'max-height': 365,
             'flex-.*-wrap-reverse': 366, 'font-italic': 367, 'badge-primary': 368, 'alert-heading': 369, 'align-bottom': 370,
             'navbar-brand': 371, 'justify-content-.*-center': 372, 'card-subtitle': 373, 'table': 374, 'breadcrumb': 375,
             'pagination-lg': 376, 'flex-wrap': 377, 'flex-.*-column': 378, 'card-deck': 379, 'align-text-bottom': 380,
             'badge-secondary': 381, 'd-inline': 382, 'disabled': 383, 'align-items-.*-start': 384, 'font-weight-light': 385,
             'spinner-grow-sm': 386, 'custom-file': 387, 'flex-row': 388, 'text-lowercase': 389, 'navbar-toggler': 390,
             'navbar-collapse': 391, 'flex-.*-column-reverse': 392, 'border-primary': 393, 'card-primary': 394, 'sr-only-focusable': 395,
             'embed-responsive-item': 396, 'border-left-0': 397, 'border-secondary': 398, 'modal-content': 399, 'float-left': 400,
             'align-content-.*-end': 401, 'align-self-end': 402, 'flex-.*-wrap': 403, 'card-secondary': 404, 'text-nowrap': 405,
             'btn-sm': 406, 'align-self-.*-stretch': 407, 'valid-tooltip': 408, 'align-items-.*-baseline': 409, 'dropdown-item-text': 410,
             'card-group': 411, 'bg-primary': 412, 'custom-select-sm': 413, 'display:block': 414, 'fixed-top': 415, 'modal-dialog-scrollable': 416,
             'd-inline-block': 417, 'dropdown-item': 418, 'flex-column-reverse': 419, 'mx-.*-[0-9]+': 420, 'custom-file-input': 421,
             'shadow': 422, 'card-text': 423, 'form-check': 424, 'card-columns': 425, 'custom-range': 426, 'list-inline-item': 427,
             'flex-shrink-[0-1]+': 428, 'btn-outline-warning': 429, 'btn-toolbar': 430, 'is-valid': 431, 'text-.*-left': 432,
             'card-footer': 433, 'd-.*-inline-block': 434, 'align-self-.*-start': 435, 'table-condensed': 436, 'd-.*-inline': 437,
             'w-100': 438, 'badge-info': 439, 'mx-[0-9]+': 440, 'form-control-lg': 441, 'active': 442, 'font-weight-bolder': 443,
             'list-group': 444, 'text-success': 445, 'border-sm': 446, 'dropdown-menu': 447, '<pre>': 448, 'btn-outline-danger': 449, 'sr-only': 450
         }

    def process_data(self, fine_relations):
        valid_data_point = 1
        processed_data = []
        for parent in fine_relations:
            parent_value = None
            for rule, value in self.bootstrap_classes_and_int_representation.items():
                if re.match(rule, parent):
                    parent_value = value
                    break
            if not value:
                continue
            for child in fine_relations[parent]:
                child_value = None
                for rule, value in self.bootstrap_classes_and_int_representation.items():
                    if re.match(rule, child):
                        child_value = value
                        break

                if not child_value:
                    continue

                for depth in fine_relations[parent][child]:
                    processed_data.append([
                        parent_value,
                        child_value,
                        depth,
                        valid_data_point
                    ])
        return processed_data



    def write_process_data_to_csv(self, processed_data, csv_filename):
        with open(csv_filename, "w") as f:
            writer = csv.writer(f)
            writer.writerows(processed_data)
        return

    def process_errors(self, errors_list):
        random_or_manual = 'random'

        for lst in errors_list:
            parent_value = None
            child_value = None
            for rule, value in self.bootstrap_classes_and_int_representation.items():
                if re.match(rule, lst[1]):
                    parent_value = value
                    break

            for rule, value in self.bootstrap_classes_and_int_representation.items():
                if re.match(rule, lst[2]):
                    child_value = value
                    break

            if not parent_value or not child_value:
                return

            error = 'Error in line {} ---> Parent: {} has no relation to child: {} at depth: {}. correct?'.format(
                colored(lst[0], 'red'), colored(lst[1], 'blue'), colored(lst[2], 'blue'), colored(lst[3], 'red'))
            if not random_or_manual or 'ma' in random_or_manual.lower():
                input_answer = input(error)
                if 'y' in input_answer.lower():
                    processed_error = [
                        parent_value,
                        child_value,
                        lst[3]
                    ]
                    self.training_data.append(processed_error)
                    self.target_data.append(1)
                    # writer.writerows([processed_error])
                else:
                    processed_error = [
                        parent_value,
                        child_value,
                        lst[3]
                    ]
                    self.training_data.append(processed_error)
                    self.target_data.append(0)
            else:
                random_number = randint(0, 1)
                processed_error = [
                    parent_value,
                    child_value,
                    lst[3]
                ]
                self.training_data.append(processed_error)
                self.target_data.append(random_number)

        return

    def train(self):
        self.classifier = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes = (3, 100), random_state = 1)
        self.classifier.fit(self.training_data, self.target_data)
        return

    def predict(self, datapoints):
        return self.classifier.predict(datapoints)



