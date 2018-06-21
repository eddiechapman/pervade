# Import libraries
import os
import csv
from xml.etree.ElementTree import iterparse

def initialize_settings():
    os.chdir('C:\\Users\\chapman4\\PycharmProjects\\pervade_nsf_dmps\\test')


def list_filenames():
    filenames = [name.split('.')[0] for name in os.listdir('.') if name.endswith('.xml')]
    return filenames


def list_search_terms():
    with open('search_terms.txt', 'r') as infile:
        search_terms = []
        for line in infile:
            for word in line:
                search_terms.append(word)
        return search_terms


def check_relevance(abstract_narration, search_terms):

    try:
        abstract = set(abstract_narration.split())
    except AttributeError:
        print('No abstract')
        pass

    terms = set(search_terms)

    matching_terms = terms & abstract

    print('; '.join(matching_terms))

    return matching_terms



def parse_xml(xml_file, search_terms, column_names):

    # initialize storage for extracted XML data
    grant_app = {}

    for (event, node) in iterparse(xml_file + '.xml'):

        if event == 'end' and node.text != '\n':

            grant_app[node.tag] = node.text

            if node.tag not in column_names:
                column_names.append(node.tag)

            if node.tag == 'AbstractNarration':

                abstract_narration = node.text

                if abstract_narration == True:

                    matching_terms = check_relevance(abstract_narration, search_terms)

                    if matching_terms == True:
                        grant_app['matchingTerms'] = '; '.join(matching_terms)
                    else:
                        pass
                else:
                    print('no abstract')
                    pass

    print(len(column_names), grant_app)
    return(grant_app)


def write_csv(data_mgmt_plans):
    with open('nsf_dmps.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
#         writer.writerows(data_mgmt_plans)


def main():
    initialize_settings()
    search_terms = list_search_terms()
    filenames = list_filenames()
    grant_apps = []
    column_names = []

    for xml_file in filenames:
        grant_app = parse_xml(xml_file, search_terms, column_names)
        grant_apps.append(grant_app)

    write_csv(grant_apps, column_names)

main()
