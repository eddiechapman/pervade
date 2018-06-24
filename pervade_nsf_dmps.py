# Import libraries
import os
import re
import csv
from xml.etree.ElementTree import iterparse
import pervade_nsf_dmps_search


def set_directory():
    os.chdir('C:\\Users\\chapman4\\PycharmProjects\\pervade_nsf_dmps\\test')



def generate_xml_docs():
    for xml_docs in os.listdir('.'):
        if xml_docs in all_docs:
            yield xml_docs


def parse_xml_docs(xml_docs):
    for xml_doc in xml_docs:
        print('starting document:', xml_doc)
        for (event, xml_elements) in iterparse(xml_doc):
            if event == 'end' and xml_elements.text != '\n':
                print('here is an element')
                yield xml_elements


def process_elements(xml_elements,):
    doc_data = {}
    for xml_element in xml_elements:
        doc_data[xml_element.tag] = xml_element.text
    print(doc_data)
    return doc_data


def update_column_names(doc_data, column_names):
    current_columns = set(doc_data.keys())
    column_names.update(current_columns)
    print('updating columns names', len(column_names))


def update_all_docs(doc_data, all_docs):
    all_docs.append(doc_data)
    print('updating all docs', len(all_docs))

# I think this isn't working correctly. Maybe it only will write a
# row that contains all (max) columns? Only one is showing up.
def write_csv(all_docs, column_names):
    print('time to write a csv!')
    with open('nsf_dmps.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, column_names)
        writer.writeheader()
        writer.writerows(all_docs)

def main():
    set_directory()
    all_docs = pervade_nsf_dmps_search.main()
    column_names = set()
    while True:
        xml_docs = generate_xml_docs()
        xml_elements = parse_xml_docs(xml_docs)
        doc_data = process_elements(xml_elements)
        update_column_names(doc_data, column_names)
        update_all_docs(doc_data, all_docs)
    write_csv(all_docs, column_names)


if __name__ == '__main__':
    main()
