import xml.etree.ElementTree as ET
import os
import re


def set_directory():
    os.chdir('C:\\Users\\chapman4\\PycharmProjects\\pervade_nsf_dmps\\test')


def generate_xml_docs():
    for xml_docs in os.listdir('.'):
        if xml_docs.endswith('.xml'):
            yield xml_docs


def initialise_filenames():
    filenames = []
    return filenames


def list_search_terms():
    with open('search_terms.txt', 'r') as infile:
        search_terms = set(word.strip().lower() for word in infile)
        print('search terms:', search_terms)
        return search_terms


def compile_regex(search_terms):
    search_terms_regex = set()
    for term in search_terms:
        search_term_regex = re.compile(term)
        search_terms_regex.add(search_term_regex)
    return search_terms_regex


def parse_xml(xml_docs, filenames):
    for xml_doc in xml_docs:
        filenames.append(xml_doc)
        tree = ET.parse(xml_doc)
        for element in tree.iter(tag='AbstractNarration'):
            if element.text:
                yield element.text
            else:
                continue


def check_relevance(abstracts, search_terms_regex, filenames):
    for abstract in abstracts:
        relevance = set()
        for regex in search_terms_regex:
            match = regex.search(abstract)
            if match:
                relevance.add(match.group())
        if relevance:
            print(relevance)
            yield relevance
        else:
            filenames.pop()
            pass


def update_relevant_docs(relevance, filenames, all_docs):
    for relevant in relevance:
        relevant_doc = {'Filename': filenames[-1], 'RelevantTerms': relevant}
        all_docs.append(relevant_doc)


def main():
    set_directory()
    search_terms = list_search_terms()
    search_terms_regex = compile_regex(search_terms)
    all_docs = []
    filenames = initialise_filenames()
    xml_docs = generate_xml_docs()
    abstracts = parse_xml(xml_docs, filenames)
    relevance = check_relevance(abstracts, search_terms_regex, filenames)
    update_relevant_docs(relevance, filenames, all_docs)
    print(all_docs)
    return all_docs


if __name__ == '__main__':
    main()
