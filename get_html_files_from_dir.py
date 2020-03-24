import glob
import os
import shutil

def move_file_from_source_go_target(source, target):
    shutil.move(source, target)
    return


def get_list_of_all_html_files(dir):
    if os.path.isdir(dir):
        print('Is a directory!')
    files_list = glob.glob(os.path.join(dir, "**/*.html"), recursive=True)
    return files_list

def write_files_to_target(files, target):
    filename_counter = 1
    for file in files:
        with open(file, 'r') as rfl:
            lines = rfl.readlines()
            with open(os.path.join(target, str(filename_counter) + '.html'), 'w+') as wfl:
                wfl.writelines(lines)
        filename_counter += 1

        print('Processed: {}'.format(file))
    return
files_list = get_list_of_all_html_files('frameworks-examples/foundation-sites-develop/test-pages')
target_path = 'frameworks-examples/foundation-sites-develop'

write_files_to_target(files_list, target_path)


