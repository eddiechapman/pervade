import os
import csv
import itertools
import xml.etree.ElementTree as ET


def set_directory():
    """Specify where the xml and txt files are located on the user's computer."""
    os.chdir('C:\\Users\\chapman4\\PycharmProjects\\pervade_nsf_dmps\\dmps')


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
        award_fields = {}
        award_fields['filename'] = filename
        yield award_fields


def load_xml(award_fields):
    """Create and store an xml tree object in each dictionary."""
    for award in award_fields:
        filename = award['filename']
        try:
            award['tree'] = ET.parse(filename)
            yield award
        except Exception:
            print(filename, Exception)
            pass


def find_abstract(award_fields):
    """Find and store the xml abstract text in each dictionary, if found."""
    for award in award_fields:
        tree = award['tree']
        abstract = tree.findtext('./Award/AbstractNarration')
        if abstract:
            award['abstract'] = abstract
            yield award
        else:
            pass


def tokenize_abstract(award_fields):
    """Split the abstract text into sentences and store them in the dictionaries."""
    for award in award_fields:
        award['lines_abstract'] = award['abstract'].lower().split('. ')
        yield award


def query_abstract(award_fields, search_terms):
    """Compare abstract sentences to search terms. Save matching pairs."""
    for award in award_fields:
        abstract_matches = set()
        search_term_matches = []
        lines_abstract = award['lines_abstract']
        results = itertools.product(lines_abstract, search_terms)
        for line_abstract, search_term in results:
            if search_term in line_abstract:
                abstract_matches.add(line_abstract)
                search_term_matches.append(search_term)
        if abstract_matches and search_term_matches:
            award['relevant_lines'] = '; \n\n'.join(list(abstract_matches))
            award['relevant_terms'] = '; \n\n'.join(search_term_matches)
            yield award
        else:
            pass


def add_title(award_fields):
    """Find and add the XML title field to the dictionary."""
    single_fields = [
        'AwardTitle', 'AwardEffectiveDate', 'Award/AwardInstrument',
        'AwardExpirationDate', 'AwardAmount', 'AwardInstrument/Value',
        'Organization/Code', 'Organization/Directorate/LongName',
        'Organization/Division/LongName', 'ProgramOfficer/SignBlockName',
        'MinAmdLetterDate', 'MaxAmdLetterDate', 'AwardID',
    ]
    multi_fields = [
        'Investigator', 'Institution', 'FoaInformation',
        'ProgramElement', 'ProgramReference'
    ]
    for award in award_fields:
        tree = award['tree']
        for field in single_fields:
            element = tree.findall('./Award/' + field)
            for elem in element:
                award[field + elem.tag] = elem.text
        for multi_field in multi_fields:
            elem_blocks = tree.findall('./Award/' + multi_field)
            for i, block in enumerate(elem_blocks, 1):
                elems = block.findall('./*')
                for elem in elems:
                    if elem.text is None:
                        continue
                    else:
                        award[multi_field + str(i) + elem.tag] = elem.text
        yield award


def remove_unused_fields(award_fields):
    """Remove XML tree and abstract sentences from the dictionaries."""
    for award in award_fields:
        del award['tree']
        del award['lines_abstract']
        yield award


def update_column_names(relevant_awards, column_names):
    """Maintain list of all currently used dictionary key names, to be used
    as CSV column names."""
    for award in relevant_awards:
        for key in award.keys():
            if key not in column_names:
                column_names.append(key)


def compile_relevant_awards(award_fields, relevant_awards):
    """Store completed dictionaries in a list."""
    for award in award_fields:
        relevant_awards.append(award)


def write_csv(relevant_awards, column_names):
    """Store data from completed dictionaries in a CSV."""
    with open('nsf_dmps.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, column_names)
        writer.writeheader()
        writer.writerows(relevant_awards)


def main():
    set_directory()
    search_terms = retrieve_search_terms()
    relevant_awards = []
    column_names = []
    filenames = generate_filenames()
    award_fields = initialize_storage(filenames)
    award_fields = load_xml(award_fields)
    award_fields = find_abstract(award_fields)
    award_fields = tokenize_abstract(award_fields)
    award_fields = query_abstract(award_fields, search_terms)
    award_fields = add_title(award_fields)
    award_fields = remove_unused_fields(award_fields)
    compile_relevant_awards(award_fields, relevant_awards)
    update_column_names(relevant_awards, column_names)
    write_csv(relevant_awards, column_names)

if __name__ == '__main__':
    main()
