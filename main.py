import bibtexparser
from datetime import datetime
import pandas as pd

def generate_ESDL_tag(item):
    if item['ENTRYTYPE'] == 'inproceedings':
        if item['esdlid'] != '*':
            esdl_label = '[' + item['esdlid'] + ']'
        else:
            esdl_label = '[CXX]'
    elif item['ENTRYTYPE'] == 'article':
        if item['esdlid'] != '*':
            esdl_label = '[' + item['esdlid'] + ']'
        else:
            esdl_label = '[JXX]'
    return esdl_label

def get_additional_info(item):
    if item['ENTRYTYPE'] == 'inproceedings':
        add_info = 'In' + item['booktitle'] + ', ' + item.get('number', '') + ', ' + item.get('pages', '') + \
                   ', ' + item['address'] + ', ' + item['month'].capitalize() + ' ' + item['year'] + ' '
    elif item['ENTRYTYPE'] == 'article':
        add_info = item['journal'] + '. Vol: ' + item['volume'] + '(' + item['number'] + ')' + ', pp. ' + \
                   item['pages'] + ', ' + item.get('month', '') + ' ' + item['year'] + ' '
    return add_info


def generate_html_markup(item):
    esdl_id = generate_ESDL_tag(item) + ' '
    authors_str = item['author'] + '. '
    title_str = item['title'] + '. '
    other_info = get_additional_info(item)
    pdf_url = '<a href = "http://systemdesign.illinois.edu/publications/' + item['ID'] + '.pdf" target =' '"_blank">pdf</a>'
    try:
        doi_url = 'DOI: <a href = "http://dx.doi.org/' + item['doi'] + '" target = "_blank">' + item['doi'] + '</a>'
    except:
        doi_url = ''

    html_markup = esdl_id + authors_str + title_str + other_info + pdf_url + ' ' + doi_url
    return html_markup

def set_type_publication(entrytype):
    if entrytype == 'inproceedings':
        type_sub = 'Conference Peer Reviewed'
    elif entrytype == 'article':
        type_sub = 'Journal Publications'
    else:
        type_sub = None
    return type_sub

def set_conference_or_journal(entrytype):
    if entrytype == 'inproceedings':
        key = 'booktitle'
    elif entrytype == 'article':
        key = 'journal'
    return key

def generate_entry_data(item):
    item_dict = {'DATE OF ENTRY': '{}/{}/{}'.format(datetime.now().month, datetime.now().day, datetime.now().year),
                 'YOUR NAME': 'Dario Rodriguez',
                 'TYPE OF SUBMISSION': set_type_publication(item['ENTRYTYPE'].lower()),
                 'TITLE OF SUBMISSION': item['title'],
                 'IN WHAT CONFERENCE OR JOURNAL WILL THIS SUBMISSION APPEAR': item[set_conference_or_journal(item['ENTRYTYPE'].lower())],
                 'PUBLICATION STATE': 'Accepted, published in print',
                 'CO-AUTHORS/EXTERNAL COLLABORATORS': item['author'],
                 'DOI (when available)': item.get('doi', ''),
                 'ESDL PUBLICATION ID': item['esdlid'],
                 'html MARK UP CODE': generate_html_markup(item),
                 'Volume': item.get('volume', ''),
                 'Issue': item.get('number', ''),
                 'Pages': item.get('pages', ''),
                 'Publication Date': item.get('month', '') + ' ' + item['year'],
                 }
    return item_dict

def preprocess_excel_file(xls_file):
    df = pd.read_excel(xls_file)
    header = 1
    df.columns = df.iloc[header]
    df = df.iloc[header + 1:].reset_index(drop=True)
    return df


if __name__ == "__main__":

    # Specify .bib file
    bib_file_path = 'esdl_refs.bib'

    # Open the .bib file and parse it
    with open(bib_file_path, 'r') as bib_file:
        bib_database = bibtexparser.load(bib_file)

    # Read excel_file and process it as pandas dataframe
    df = preprocess_excel_file("Publications_Outputs Primary_jg.xlsx")

    # Iterate over .bib file (only for journals and proceedings)
    for entry in bib_database.entries:
        if entry['ENTRYTYPE'] == 'inproceedings' or entry['ENTRYTYPE'] == 'article':
            entry_data = generate_entry_data(entry)
            entry_data_df = pd.DataFrame.from_dict(entry_data, orient='index')
            df = pd.concat([df, entry_data_df.T])

    # Update datetime column
    df['DATE OF ENTRY'] = pd.to_datetime(df['DATE OF ENTRY'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')

    # Finally return and save a new modified spreadsheet
    df.to_excel('modified_publications.xlsx')

