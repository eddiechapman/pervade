import os
import csv
import itertools
import xml.etree.ElementTree as ET


def set_directory():
    """Specify where the xml and txt files are located on the user's computer."""
    os.chdir('C:\\Users\\chapman4\\PycharmProjects\\pervade_nsf_dmps\\test')


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
        award['tree'] = ET.parse(filename)
        yield award


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


def split_abstract(award_fields):
    """Split the abstract text into sentences and store them in the dictionaries."""
    for award in award_fields:
        abstract = award['abstract']
        award['lines_abstract'] = abstract.split('. ')
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
                print(elem.tag + '===' + elem.text)
        for multi_field in multi_fields:
            elem_blocks = tree.findall('./Award/' + multi_field)
            for i, block in enumerate(elem_blocks, 1):
                for sub_elem in block.iter():
                    if sub_elem is None:
                        continue
                    else:
                        award[multi_field + str(i) + sub_elem.tag] = sub_elem.text
                        print(sub_elem.tag + '===' + sub_elem.text)
        yield award


# def add_title(award_fields):
#     """Find and add the XML title field to the dictionary."""
#     single_fields = [
#         'AwardTitle', 'AwardEffectiveDate', 'AwardExpirationDate', 'AwardAmount',
#         'Value', 'SignBlockName', 'MinAmdLetterDate', 'MaxAmdLetterDate', 'AwardID',
#     ]
#     nested_fields = {'Organization': 'Org'}
#     multi_fields = {
#         'Investigator': 'Inv', 'Institution': 'Inst', 'ProgramElement': 'ProElem',
#         'ProgramReference': 'ProRef',
#     }
#     for award in award_fields:
#         tree = award['tree']
#         for single_field in single_fields:
#             elem = tree.find(single_field)
#             if elem is None:
#                 continue
#             else:
#                 award[elem.tag] = elem.text
#                 print('single', elem.tag, elem.text)
#         for nested_field in nested_fields:
#             elems = award['tree'].find('.//' + nested_field + '/*')
#             for elem in elems:
#                 if elem is None:
#                     continue
#                 else:
#                     award[nested_fields[nested_field] + elem.tag] = elem.text
#                     print('nested', elem.tag, elem.text)
#         for multi_field in multi_fields:
#             elems = award['tree'].findall(multi_field)
#             for i, elem in enumerate(elems):
#                 for e in elem.iter():
#                     if e is None:
#                         continue
#                     else:
#                         award[multi_field[multi_field] + str(i) + e.tag] = e.text
#                         print('multi', e.tag, e.text)
#     yield award

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
    award_fields = split_abstract(award_fields)
    award_fields = query_abstract(award_fields, search_terms)
    award_fields = add_title(award_fields)
    award_fields = remove_unused_fields(award_fields)
    compile_relevant_awards(award_fields, relevant_awards)
    update_column_names(relevant_awards, column_names)
    write_csv(relevant_awards, column_names)

if __name__ == '__main__':
    main()
