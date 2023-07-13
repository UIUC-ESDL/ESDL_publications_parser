import requests
import re
from bs4 import BeautifulSoup
import bibtexparser

# Define the URL of the webpage
url = "https://ise.illinois.edu/directory/profile/jtalliso"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the element containing the publications
publications_div = soup.find('div', id='article_[postid]')

# Find the header element within the selected articles div
header_selected_articles = publications_div.find('h2', string='Selected Articles in Journals')
# Find the unordered list within the selected articles div
ul_selected_articles = header_selected_articles.find_next_sibling('ul')
# Extract the list items within the unordered list
journal_publications_list = ul_selected_articles.find_all('li')


# Find the header element within the selected articles div
header_selected_articles = publications_div.find('h2', string='Articles in Conference Proceedings')
# Find the unordered list within the selected articles div
ul_selected_articles = header_selected_articles.find_next_sibling('ul')
# Extract the list items within the unordered list
conference_publications_list = ul_selected_articles.find_all('li')

all_publications_ls = []

# Print the publications
for publication in journal_publications_list:
    all_publications_ls.append(publication)
for publication in conference_publications_list:
    all_publications_ls.append(publication)

# Get the titles of the publications
title_ls = []
wrong_ls = []
for publication in all_publications_ls:
    try:
        title_ls.append(re.findall(r"'([^']+)'", publication.text)[0])
    except:
        wrong_ls.append(publication.text)

print('The following publications from the website have a wrong format:\n')
for wrong in wrong_ls:
    print(wrong)

# Parse .bib file
# Specify .bib file
bib_file_path = 'esdl_refs.bib'
# Open the .bib file and parse it
with open(bib_file_path, 'r') as bib_file:
    bib_database = bibtexparser.load(bib_file)

# Get the titles of the publications from bibfile
bib_title_ls = []
for entry in bib_database.entries:
    bib_title_ls.append(entry['title'])

# Compare the titles from the webpage and the bibfile
first_word_bib_file_ls = [bib_title_ls[i].split()[0] for i in range(len(bib_title_ls))]
not_in_bib = []
for title in title_ls:
    try:
        if title.split()[0] not in first_word_bib_file_ls:
            not_in_bib.append(title)
    except:
        not_in_bib.append(title)

print('The following publications are not in the bib file:\n')
for pub in not_in_bib:
    print(pub)
print('\n Please update the bib file with the new publications')


