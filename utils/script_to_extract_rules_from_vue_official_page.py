from bs4 import BeautifulSoup
import requests

counter = 0
urls = [
    'https://vuematerial.io/components/app',
    'https://vuematerial.io/components/avatar',
    'https://vuematerial.io/components/badge',
    'https://vuematerial.io/components/bottom-bar',
    'https://vuematerial.io/components/button',
    'https://vuematerial.io/components/card',
    'https://vuematerial.io/components/content',
    'https://vuematerial.io/components/datepicker',
    'https://vuematerial.io/components/dialog',
    'https://vuematerial.io/components/divider',
    'https://vuematerial.io/components/drawer',
    'https://vuematerial.io/components/empty-state',
    'https://vuematerial.io/components/form',
    'https://vuematerial.io/components/autocomplete',
    'https://vuematerial.io/components/checkbox',
    'https://vuematerial.io/components/chips',
    'https://vuematerial.io/components/file',
    'https://vuematerial.io/components/input',
    'https://vuematerial.io/components/radio',
    'https://vuematerial.io/components/select',
    'https://vuematerial.io/components/switch',
    'https://vuematerial.io/components/icon',
    'https://vuematerial.io/components/list',
    'https://vuematerial.io/components/menu',
    'https://vuematerial.io/components/progress-bar',
    'https://vuematerial.io/components/progress-spinner',
    'https://vuematerial.io/components/snackbar',
    'https://vuematerial.io/components/speed-dial',
    'https://vuematerial.io/components/steppers',
    'https://vuematerial.io/components/subheader',
    'https://vuematerial.io/components/table',
    'https://vuematerial.io/components/tabs',
    'https://vuematerial.io/components/toolbar',
    'https://vuematerial.io/components/tooltip',
    'https://vuematerial.io/ui-elements/elevation',
    'https://vuematerial.io/ui-elements/layout',
    'https://vuematerial.io/ui-elements/scrollbar',
    'https://vuematerial.io/ui-elements/text-selection',
    'https://vuematerial.io/ui-elements/typography'
]

def extract_rules(url):
    global counter
    content = requests.get(url).content
    page = BeautifulSoup(content, 'html.parser')
    all_examples_in_page = page.findAll("div", {"class": "demo-content"})
    for example in all_examples_in_page:
        counter += 1
        with open('vue_md_official_examples/{}.html'.format(counter), 'w+') as rfl:
            rfl.write(example)


for url in urls:
    print('Extracting code from {}'.format(url))
    extract_rules(url)