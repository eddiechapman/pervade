import os
import csv
import itertools
import xml.etree.ElementTree as ET


def set_directory():
    """Specify where the xml and txt files are located on the user's computer."""
    os.chdir('C:\\Users\\chapman4\\PycharmProjects\\pervade_nsf_dmps\\dmps')

                                                                                 x
def retrieve_search_terms():
    """Open a text file. Store each line in a set. Return the set."""
    with open('search_terms.txt', 'r') as infile:
        search_terms = {line.strip().lower() for line in infile}
        return search_terms


def generate_filenames():
    """Generate a sequence of filenames ending in '.xml'."""
    for filenames in os.listdir('.'):
        if filenames.endswith('.xml'):
            yield filenames


def initialize_storage(filenames):
    """Generate a dictionary for each filename. Store the filename."""
    for filename in filenames:
        document_fields = {}
        document_fields['filename'] = filename
        yield document_fields


def load_xml(document_fields):
    """Create and store an xml tree object in each dictionary."""
    for document in document_fields:
        filename = document['filename']
        document['tree'] = ET.parse(filename)
        yield document


def find_abstract(document_fields):
    """Find and store the xml abstract text in each dictionary, if found."""
    for document in document_fields:
        tree = document['tree']
        abstract = tree.findtext('./Award/AbstractNarration')
        if abstract:
            document['abstract'] = abstract
            yield document
        else:
            pass


def split_abstract(document_fields):
    """Split the abstract text into sentences and store them in the dictionaries."""
    for document in document_fields:
        abstract = document['abstract']
        document['lines_abstract'] = abstract.split('. ')
        yield document


def query_abstract(document_fields, search_terms):
    """Compare abstract sentences to search terms. Save matching pairs."""
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
    """Find and add the XML title field to the dictionary."""
    for document in document_fields:
        tree = document['tree']
        title = tree.findtext('./Award/AwardTitle')
        document['title'] = title
        yield document


def remove_unused_fields(document_fields):
    """Remove XML tree and abstract sentences from the dictionaries."""
    for document in document_fields:
        del document['tree']
        del document['lines_abstract']
        yield document


def compile_relevant_files(document_fields, relevant_files):
    """Store completed dictionaries in a list."""
    for document in document_fields:
        relevant_files.append(document)


def write_csv(relevant_files):
    """Store data from completed dictionaries in a CSV."""
    with open('nsf_dmps.csv', 'w') as csv_file:
        column_names = relevant_files[0].keys()
        writer = csv.DictWriter(csv_file, column_names)
        writer.writeheader()
        writer.writerows(relevant_files)


def main():
    set_directory()
    search_terms = retrieve_search_terms()
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
