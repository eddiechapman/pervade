# Import libraries
import os
import re
import csv
import xml.etree.ElementTree as ET


def set_directory():
    os.chdir('C:\\Users\\chapman4\\PycharmProjects\\pervade_nsf_dmps\\dmps')


def list_search_terms():
    with open('search_terms.txt', 'r') as infile:
        search_terms = [line.strip().lower() for line in infile]
        print('Search terms:', search_terms)
        return search_terms


def compile_regex_queries(search_terms):
    regex_queries = [re.compile(term) for term in search_terms]
    return regex_queries


def generate_filenames():
    for filenames in os.listdir('.'):
        if filenames.endswith('.xml'):
            yield filenames


def determine_relevancy(filenames, regex_queries):
    relevant_docs = []
    for file in filenames:
        file_info = {}
        relevance = query_abstract(file, regex_queries)
        if relevance:
            print(file, 'RELEVANT:', relevance)
            file_info['Filename'] = file
            file_info['MatchingTerms'] = relevance
            relevant_docs.append(file_info)
        else:
            continue
    return relevant_docs


def query_abstract(file, regex_queries):
    tree = ET.parse(file)
    abstract = tree.findtext('./Award/AbstractNarration')
    if abstract:
        relevance = set()
        for query in regex_queries:
            match = query.search(abstract)
            if match:
                relevance.add(match.group())
            else:
                continue
        if relevance:
            return '; '.join(list(relevance))
        else:
            return False
    else:
        return False


# def parse_xml(relevant_docs):
#     single_fields = [
#         'AwardTitle', 'AwardEffectiveDate', 'AwardExpirationDate', 'AwardAmount',
#         'AwardInstrument/Value', 'Organization/Code',
#         'Organization/Directorate/LongName', 'Organization/Division/Longname',
#         'ProgramOfficer/SignBlockName', 'AbstractNarration', 'MinAmdLetterDate',
#         'MaxAmdLetterDate', 'ARRAAmount', 'AwardID'
#     ]
#     repeat_fields = [
#         'Investigator', 'Institution', 'ProgramElement', 'ProgramReference'
#     ]
#     for doc in relevant_docs:
#         tree = ET.parse(doc['Filename'])
#         for single_field in single_fields:
#             single_elem = tree.find('./Award/' + single_field)
#             if single_elem:
#                 doc[single_elem.tag] = single_elem.text
#                 print(single_elem.tag, ':', single_elem.text)
#             else:
#                 continue
#             single_elem.clear()
#         for repeat_field in repeat_fields:
#             repeat_elems = tree.findall(repeat_field)
#             for index, repeat_elem in enumerate(repeat_elems, 1):
#                 repeat_sub_elems = repeat_elem.iter()
#                 for repeat_sub_elem in repeat_sub_elems:
#                     doc[repeat_sub_elem.tag + index] = repeat_sub_elem.text
#                     print(repeat_sub_elem.tag, ':', repeat_sub_elem.text)
#                     repeat_sub_elem.clear()


def parse_xml(relevant_docs):
    for doc in relevant_docs:
        repeat_elem_count = {}
        for event, elem in ET.iterparse(doc['Filename']):
            if event == 'end' and elem.text != '\n':
                if elem.tag not in doc:
                    doc[elem.tag] = elem.text
                elif elem.tag in doc:
                    if elem.tag in repeat_elem_count:
                        repeat_elem_count[elem.tag] += 1
                    else:
                        repeat_elem_count[elem.tag] = 1
                    doc[elem.tag + str(repeat_elem_count[elem.tag])] = elem.text
            elem.clear()
        repeat_elem_count.clear()
        print(doc)


def record_column_names(relevant_docs):
    column_names = []
    for doc in relevant_docs:
        for key in doc.keys():
            if key not in column_names:
                column_names.append(key)
            else:
                continue
    print(column_names)
    return column_names


def write_csv(relevant_docs, column_names):
    with open('nsf_dmps.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, column_names)
        writer.writeheader()
        writer.writerows(relevant_docs)



def main():
    set_directory()
    search_terms = list_search_terms()
    regex_queries = compile_regex_queries(search_terms)
    filenames = generate_filenames()
    relevant_docs = determine_relevancy(filenames, regex_queries)
    parse_xml(relevant_docs)
    column_names = record_column_names(relevant_docs)
    write_csv(relevant_docs, column_names)


if __name__ == '__main__':
    main()
