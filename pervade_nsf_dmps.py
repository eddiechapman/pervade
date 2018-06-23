# Import libraries
import os
import csv
from xml.etree.ElementTree import iterparse


def set_directory():
    os.chdir('C:\\Users\\chapman4\\PycharmProjects\\pervade_nsf_dmps\\test')


def generate_xml_docs():
    for xml_docs in os.listdir('.'):
        if xml_docs.endswith('.xml'):
            yield xml_docs


def list_search_terms():
    with open('search_terms.txt', 'r') as infile:
        search_terms = set()
        for line in infile:
            words = line.split()
            search_terms.update(words)
        print('search terms:', search_terms)
        return search_terms

# This still isn't working great...I think I should move on or try searching
# by phrases but that sounds complicated. 
def check_relevance(xml_elements, search_terms):
    for xml_element in xml_elements:
        print(xml_element.tag, ':', xml_element.text)
        if xml_element.tag == 'AbstractNarration':
            print('Checking abstract...')
            try:
                abstract_words = set()
                abstract = xml_element.text.split()
                abstract_words.update(abstract)
                print('found abstract')
                relevance = search_terms & abstract_words
                print('relevant terms:', relevance)
                return relevance
            except Exception:
                print('Abstract error')
        else:
            continue


def parse_xml_docs(xml_docs):
    for xml_doc in xml_docs:
        print('starting document: ', xml_doc)
        for (event, xml_elements) in iterparse(xml_doc):
            if event == 'end' and xml_elements.text != '\n':
                yield xml_elements
            xml_elements.clear()


def process_elements(xml_elements, relevance):
    doc_data = {}
    for xml_element in xml_elements:
        # Will this break the iteration or the entire function loop?
        if relevance == False:
            print('not relevant! time to break.')
            break
        else:
            doc_data[xml_element.tag] = xml_element.text
            print(xml_element.tag, '=', doc_data[xml_element.tag])
            doc_data['RelevantTerms'] = relevance
            print('relevant terms:', doc_data['RelevantTerms'])
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
    search_terms = list_search_terms()
    all_docs = []
    column_names = set()
    xml_docs = generate_xml_docs()
    xml_elements = parse_xml_docs(xml_docs)
    relevance = check_relevance(xml_elements, search_terms)
    doc_data = process_elements(xml_elements, relevance)
    update_column_names(doc_data, column_names)
    update_all_docs(doc_data, all_docs)
    write_csv(all_docs, column_names)


if __name__ == '__main__':
    main()
