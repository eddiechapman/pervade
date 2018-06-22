# Import libraries
import os
import csv
from xml.etree.ElementTree import iterparse

def initialize_settings():
    os.chdir('C:\\Users\\chapman4\\PycharmProjects\\pervade_nsf_dmps\\test')


def list_filenames():
    filenames = [name for name in os.listdir('.')]
    return filenames


def list_search_terms():
    with open('search_terms.txt', 'r') as infile:
        search_terms = []
        for line in infile:
            for word in line:
                search_terms.append(word)
        return search_terms


def check_relevance(element, search_terms, grant_app):

    if element.text == True:


    else:
        print('Missing Abstract')

    terms = set(search_terms)

    matching_terms = terms & abstract

    print('; '.join(matching_terms))

    return relevance


def record_element(grant_app, element):
    """
    Create dictionary key/value pair based on XML element key/text.

    :param grant_app: dictionary of XML document data
    :param element: an individual XML element
    :return: dictionary with new key/value pair based on xml element
    """
     grant_app[element.tag] = element.text
     return grant_app


def parse_xml(xml_file, search_terms, column_names):
    # initialize storage for extracted XML data
    grant_app = {}

    for (event, element) in iterparse(xml_file):
        if event == 'end' and element.text != '\n':
            yield element


        if event == 'end' and element.text != '\n':
           grant_app = record_element(grant_app, element)

            if node.tag not in column_names:
                column_names.append(node.tag)

            if node.tag == 'AbstractNarration':
                relevance = check_relevance()

                if relevance == True:
                    continue
                else:
                    pass
    print(len(column_names), grant_app)
    return(grant_app)


def write_csv(grant_apps):
    with open('nsf_dmps.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
        writer.writerows(grant_apps)


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

if __name__ == '__main__':
    main()
