from bs4 import BeautifulSoup


file = 'source_file.html'

with open(file, 'r') as rfl:
    train_soup = BeautifulSoup(rfl, 'html.parser')
    all_elements = train_soup.findAll()

    all_codes = []

    html = u""
    for tag in all_elements:
        if tag.name == "h2":
            html = u""

        if tag.name == "figure":
            all_codes.append(html)
            html = u""

        if tag.name == "p":
            pass
        else:
            html += str(tag)


    print(all_codes)