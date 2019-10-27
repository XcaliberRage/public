# This was used purely to grab info off of wikipedia
# Ultimately I used it to make a txt file that populates the Breeds list
# I have not integrated it automatically because parsing wiki html into a
# sensible list looks like black magic atm

import urllib.request
from bs4 import BeautifulSoup


def grabSite():
    url = 'https://en.wikipedia.org/wiki/List_of_cat_breeds'
    req = urllib.request.urlopen(url)
    article = req.read().decode()

    with open('Cat_Breeds.html', 'w') as fo:
        fo.write(article)

def parseSite():

    # Load article, soup it and get the tables
    article = open('Cat_Breeds.html').read()
    soup = BeautifulSoup(article, 'html.parser')
    tables = soup.find_all('table', class_='sortable')

    # Search through the tables for the heading we want
    for table in tables:
        ths = table.find_all('th')
        headings = [th.text.strip() for th in ths]
        if headings[:1] == ['Breed']:
            break

    # Extract the column and write to a txt.file
    with open('CatBreeds.txt', 'w') as fo:
        for tr in table.find_all('tr'):
            tds = tr.find_all('th')
            if not tds:
                continue
            breed = [td.text.strip() for td in tds[:4]]
            # Wikipedia does something funny with country names containing
            # accented characters: extract the correct string form.
            print(', '.join(breed), file=fo)


grabSite()
parseSite()