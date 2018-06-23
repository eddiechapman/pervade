# Import libraries
import os
import re
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
        search_terms = set(word.strip().lower() for word in infile)
        print('search terms:', search_terms)
        return search_terms


def compile_regex(search_terms):
    search_terms_regex = set(re.compile(search) for search in search_terms)
    print(len(search_terms_regex))
    return search_terms_regex

# This still isn't working great...I think I should move on or try searching
# by phrases but that sounds complicated.
# def find_abstract(xml_elements):
#     print('finding abstract...')
#     for xml_element in xml_elements:
#         if xml_element.tag == 'AbstractNarration':
#             print('found abstract')
#             try:
#                 abstract = xml_element.text
#                 print()
#                 print(abstract)
#                 return abstract
#             except Exception:
#                 print('Abstract error')
#         else:
#             print('that wasnt an abstract')
#             continue


# def check_relevance(search_terms_regex, abstract):
#     relevance = set()
#     for regex in search_terms_regex:
#         match = regex.search(abstract)
#         if match:
#             relevance.update(match)
#     print(relevance)
#     return relevance

# gah I think i have a working search function but i can't figure out
# how to pass the relevant terms back to the next part where it's recorded
# in a dictionary. Getting there.
def check_relevance(xml_elements, search_terms_regex):
    print('checking relevance')
    relevance = set()
    for xml_element in xml_elements:
        if xml_element.tag == 'AbstractNarration':
            print()
            print('found abstract')
            print()
            for regex in search_terms_regex:
                try:
                    abstract = xml_element.text
                    match = regex.search(abstract)
                    if match:
                        print(match.string)
                        relevance.update(match.string)
                except Exception as e:
                    print(e)
            print(relevance)
        else:
            print('not an abstract')
            continue
    return relevance


def parse_xml_docs(xml_docs):
    for xml_doc in xml_docs:
        print('starting document:', xml_doc)
        for (event, xml_elements) in iterparse(xml_doc):
            if event == 'end' and xml_elements.text != '\n':
                print('here is an element')
                yield xml_elements


def process_elements(xml_elements, relevance):
    doc_data = {}
    for xml_element in xml_elements:
        doc_data[xml_element.tag] = xml_element.text
        #print(xml_element.tag, '=', doc_data[xml_element.tag])
        #print('relevant terms:', doc_data['RelevantTerms'])
    doc_data['RelevantTerms'] = relevance
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
    search_terms = list_search_terms()
    search_terms_regex = compile_regex(search_terms)
    all_docs = []
    column_names = set()
    while True:
        xml_docs = generate_xml_docs()
        xml_elements = parse_xml_docs(xml_docs)
        relevance = check_relevance(xml_elements, search_terms_regex)
        doc_data = process_elements(xml_elements, relevance)
        update_column_names(doc_data, column_names)
        update_all_docs(doc_data, all_docs)
    write_csv(all_docs, column_names)


if __name__ == '__main__':
    main()
