import os
import csv
import itertools
import xml.etree.ElementTree as ET


def set_directory():
    """
    Specify the file path that the XML files and 'search_terms.txt' are located.
    """
    os.chdir('C:\\Users\\chapman4\\PycharmProjects\\pervade_nsf_dmps\\dmps')


def list_search_terms():
    """
    Open a text file. Change each line to lowercase and store it in a list.
    """
    with open('search_terms.txt', 'r') as infile:
        search_terms = {line.strip().lower() for line in infile}
        return search_terms


def generate_filenames():
    """
    Open current file directory and return filenames of XML files. Returns
    generator object.
    """
    for filenames in os.listdir('.'):
        if filenames.endswith('.xml'):
            yield filenames


def initialize_storage(filenames):
    """
    Create a dictionary for each iteration of the filename generator. Store the
    filename. This dictionary will be passed along and filled with other values.
    """
    for filename in filenames:
        document_fields = {}
        document_fields['filename'] = filename
        yield document_fields


def load_xml(document_fields):
    """
    Use the filename value from the iteration's dictionary to create and store
    an XML tree object.
    """
    for document in document_fields:
        filename = document['filename']
        document['tree'] = ET.parse(filename)
        yield document


def find_abstract(document_fields):
    """
    Use the tree value from the dictionary to retrieve the text of the Abstract
    element. If the Abstract element is blank, the file iteration is dropped.
    """
    for document in document_fields:
        tree = document['tree']
        abstract = tree.findtext('./Award/AbstractNarration')
        if abstract:
            document['abstract'] = abstract
            yield document
        else:
            pass


def split_abstract(document_fields):
    """
    Split the abstract text entry from the dictionary into sentences (roughly).
    Store them in a new entry in the dictionary.
    """
    for document in document_fields:
        abstract = document['abstract']
        document['lines_abstract'] = abstract.split('. ')
        yield document


def query_abstract(document_fields, search_terms):
    """
    Find and save matching pairs of search terms and abstract sentences.

    The abstract sentences are retrieved from the dictionary. They are passed
    to itertools.product along with the search terms which returns
    their combinations as tuples. Inspecting each tuple, if the search term
    is found in the abstract sentence, both values are stored. Abstract
    sentences are stored in a set to prevent duplication. Search terms can be
    stored multiple times. If there are values in both storage locations, they
    are joined as strings and saved as values in the dictionary. Otherwise, the
    iterating document is dropped.
    """
    for document in document_fields:
        abstract_matches = set()
        search_term_matches = []
        lines_abstract = document['lines_abstract']
        results = itertools.product(lines_abstract, search_terms)
        for line_abstract, search_term in results:
            if search_term in line_abstract:
                abstract_matches.add(line_abstract)
                search_term_matches.append(search_term)
        if abstract_matches and search_term_matches:
            document['relevant_lines'] = '; \n\n'.join(list(abstract_matches))
            document['relevant_terms'] = '; \n\n'.join(search_term_matches)
            yield document
        else:
            pass


def add_title(document_fields):
    """
    Find the title using the XML element tree stored in the dictionary. Create
    a new dictionary entry for the title.
    """
    for document in document_fields:
        tree = document['tree']
        title = tree.findtext('./Award/AwardTitle')
        document['title'] = title
        yield document


def remove_unused_fields(document_fields):
    """
    Remove the dictionary values for the XML tree and the individual abstract
    lines as they will not be needed when saving a CSV using the dictionary.
    """
    for document in document_fields:
        del document['tree']
        del document['lines_abstract']
        yield document


def compile_relevant_files(document_fields, relevant_files):
    """
    Store any document dictionaries that have made it this far in a list to
    be turned into a CSV.
    """
    for document in document_fields:
        relevant_files.append(document)


def write_csv(relevant_files):
    """
    Create a CSV file with one row for each XML file.
    """
    with open('nsf_dmps.csv', 'w') as csv_file:
        column_names = relevant_files[0].keys()
        writer = csv.DictWriter(csv_file, column_names)
        writer.writeheader()
        writer.writerows(relevant_files)


def main():
    set_directory()
    search_terms = list_search_terms()
    relevant_files = []
    filenames = generate_filenames()
    document_fields = initialize_storage(filenames)
    document_fields = load_xml(document_fields)
    document_fields = find_abstract(document_fields)
    document_fields = split_abstract(document_fields)
    document_fields = query_abstract(document_fields, search_terms)
    document_fields = add_title(document_fields)
    document_fields = remove_unused_fields(document_fields)
    compile_relevant_files(document_fields, relevant_files)
    write_csv(relevant_files)


if __name__ == '__main__':
    main()
