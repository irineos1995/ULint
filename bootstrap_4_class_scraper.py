from bs4 import BeautifulSoup
import requests
import os

w3_file = 'bootstrap-4.3.1/w3_css_classes.html'


def extract_classes(file):
    '''
        edge_cases = {
            .m-# / m-*-#'
            .flex-shrink-0|1

        }
    '''
    set_of_classes = set()
    with open(file, 'r') as tr_p:
        soup = BeautifulSoup(tr_p, 'html.parser')
    for clss in soup.find_all('code'):
        text = clss.get_text().strip().replace('.', '') # .blabla
        text = text.replace('#', '[0-9]+') # .m-#
        text = text.replace('*', '.*') # m-*-#
        text = text.replace('0|1', '[0-1]+') # .flex-shrink-0|1
        text = text.replace(' ', '') # .m-# / m-*-#'
        text = text.split('/') # .m-# / m-*-#'
        for cls in text:
            set_of_classes.add(cls)
    return set_of_classes

# classes = extract_classes(w3_file)
# print(classes)
# print(len(classes))


def get_html_from_w3_link(url, filename, destination):
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'html.parser')
    try:
        bootstrap_string = str(soup.find('textarea', {"autocomplete": 'off'}).find_all_next()[0])
        with open(os.path.join(destination, filename), 'w+') as wfl:
            wfl.writelines(bootstrap_string)
        print('GOT {}'.format(url))
        return
    except:
        print('ERROR {}'.format(url))
        return

def get_urls_from_w3_link(file):
    set_of_urls = set()
    with open(file, 'r') as tr_p:
        soup = BeautifulSoup(tr_p, 'html.parser')
    for a in soup.find_all('a', href=True):
        if a.get('href', '').startswith('tryit.asp'):
            set_of_urls.add('{}{}'.format('https://www.w3schools.com/bootstrap4/', a.get('href', '')))
    return set_of_urls

# set_of_urls = get_urls_from_w3_link(w3_file)
# print(set_of_urls)
# print(len(set_of_urls))

def all_together(w3_file):
    counter = 1
    urls = get_urls_from_w3_link(w3_file)
    for url in urls:
        filename = '{}.html'.format(counter)
        get_html_from_w3_link(url, filename, 'w3_bootstrap_examples')
        counter += 1
    return

all_together(w3_file)



