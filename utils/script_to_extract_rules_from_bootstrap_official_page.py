from bs4 import BeautifulSoup
import requests

counter = 0
urls = [
    'https://getbootstrap.com/docs/4.0/layout/overview/',
    'https://getbootstrap.com/docs/4.0/layout/grid/',
    'https://getbootstrap.com/docs/4.0/layout/media-object/',
    'https://getbootstrap.com/docs/4.0/layout/utilities-for-layout/',
    'https://getbootstrap.com/docs/4.0/content/reboot/',
    'https://getbootstrap.com/docs/4.0/content/typography/',
    'https://getbootstrap.com/docs/4.0/content/code/',
    'https://getbootstrap.com/docs/4.0/content/images/',
    'https://getbootstrap.com/docs/4.0/content/tables/',
    'https://getbootstrap.com/docs/4.0/content/figures/',
    'https://getbootstrap.com/docs/4.0/components/alerts/',
    'https://getbootstrap.com/docs/4.0/components/badge/',
    'https://getbootstrap.com/docs/4.0/components/breadcrumb/',
    'https://getbootstrap.com/docs/4.0/components/buttons/',
    'https://getbootstrap.com/docs/4.0/components/button-group/',
    'https://getbootstrap.com/docs/4.0/components/card/',
    'https://getbootstrap.com/docs/4.0/components/carousel/',
    'https://getbootstrap.com/docs/4.0/components/collapse/',
    'https://getbootstrap.com/docs/4.0/components/dropdowns/',
    'https://getbootstrap.com/docs/4.0/components/forms/',
    'https://getbootstrap.com/docs/4.0/components/input-group/',
    'https://getbootstrap.com/docs/4.0/components/jumbotron/',
    'https://getbootstrap.com/docs/4.0/components/list-group/',
    'https://getbootstrap.com/docs/4.0/components/modal/',
    'https://getbootstrap.com/docs/4.0/components/navs/',
    'https://getbootstrap.com/docs/4.0/components/navbar/',
    'https://getbootstrap.com/docs/4.0/components/pagination/',
    'https://getbootstrap.com/docs/4.0/components/popovers/',
    'https://getbootstrap.com/docs/4.0/components/progress/',
    'https://getbootstrap.com/docs/4.0/components/scrollspy/',
    'https://getbootstrap.com/docs/4.0/components/tooltips/',
    'https://getbootstrap.com/docs/4.0/utilities/borders/',
    'https://getbootstrap.com/docs/4.0/utilities/clearfix/',
    'https://getbootstrap.com/docs/4.0/utilities/close-icon/',
    'https://getbootstrap.com/docs/4.0/utilities/colors/',
    'https://getbootstrap.com/docs/4.0/utilities/display/',
    'https://getbootstrap.com/docs/4.0/utilities/embed/',
    'https://getbootstrap.com/docs/4.0/utilities/flex/',
    'https://getbootstrap.com/docs/4.0/utilities/float/',
    'https://getbootstrap.com/docs/4.0/utilities/image-replacement/',
    'https://getbootstrap.com/docs/4.0/utilities/position/',
    'https://getbootstrap.com/docs/4.0/utilities/screenreaders/',
    'https://getbootstrap.com/docs/4.0/utilities/sizing/',
    'https://getbootstrap.com/docs/4.0/utilities/spacing/',
    'https://getbootstrap.com/docs/4.0/utilities/text/',
    'https://getbootstrap.com/docs/4.0/utilities/vertical-align/',
    'https://getbootstrap.com/docs/4.0/utilities/visibility/',
]

def extract_rules(url):
    global counter
    content = requests.get(url).content
    page = BeautifulSoup(content, 'html.parser')
    all_examples_in_page = page.findAll("code", {"class": "language-html"})
    for example in all_examples_in_page:
        counter += 1
        with open('boot4_official_examples/{}.html'.format(counter), 'w+') as rfl:
            rfl.write(example.get_text())


for url in urls:
    print('Extracting code from {}'.format(url))
    extract_rules(url)