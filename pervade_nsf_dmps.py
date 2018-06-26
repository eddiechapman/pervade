import os
import re
import csv
import xml.etree.ElementTree as ET


def set_directory():
    """
    Specify the file path that the XML files and 'search_terms.txt' are located.
    """
    os.chdir('C:\\Users\\chapman4\\PycharmProjects\\pervade_nsf_dmps\\dmps')


def list_search_terms():
    """
    Open a text file. Change each line to lowercase and store it in a list.
    Display the entries for the user.
    """
    with open('search_terms.txt', 'r') as infile:
        search_terms = [line.strip().lower() for line in infile]
        print('Search terms:', search_terms)
        return search_terms


def compile_regex_queries(search_terms):
    """
    Create list of compiled regex queries that the XML abstracts will be checked
    against. Regex pattern specifies exact match.
    """
    regex_queries = [re.compile(term) for term in search_terms]
    return regex_queries


def generate_filenames():
    """
    Open current file directory and return filenames of XML files. Returns
    generator object.
    """
    for filenames in os.listdir('.'):
        if filenames.endswith('.xml'):
            yield filenames


def determine_relevancy(filenames, search_terms):
    """
    Inspect each XML file and list the relevant hits.

    Loop through all XML files in directory. Call relevance-checking function.
    For relevant files, store filename and matching search terms in a dictionary
    ('file_info). Each relevant file's dictionary is stored in a list
    ('relevant_docs').
    """
    relevant_docs = []
    for file in filenames:
        file_info = {}
        relevance = query_abstract(file, search_terms)
        if relevance:
            print(file, 'RELEVANT:', relevance)
            file_info['Filename'] = file
            file_info['MatchingTerms'] = relevance
            relevant_docs.append(file_info)
        else:
            continue
    return relevant_docs


def query_abstract(file, regex_queries):
    """
    Find the document's abstract. Search abstract for regex matches. Return hits.

    Iterate through each element of the XML tree. Wait until end of
    'AbstractNarration' element and grab the text. If there is text in the
    abstract element, run all regex queries against abstract text. Store results
    in a set to prevent duplicate entries. Return set of relevant terms if not
    empty. Otherwise, return boolean, False.
    """
    for event, elem in ET.iterparse(file):
        if event == 'end' and elem.tag == 'AbstractNarration':
            abstract = elem.text
            if abstract:
                relevance = set()
                for query in regex_queries:
                    match = query.search(abstract)
                    if match:
                        relevance.add(match.group())
                    else:
                        continue
                if relevance:
                    return relevance
                else:
                    return False
            else:
                return False
        else:
            elem.clear()


def parse_xml(relevant_docs):
    """
    Iterate through XML document tree and save text fields in a dictionary.

    Loop through each relevant document's dictioanry. Open the XML document using
    the 'Filename' key. Iterate through all elements in XML tree. Wait until the
    end of a tag to add the element's tag and text as a key/value pair in the
    document's dictionary.

    Some XML elements may be repeated (institution, investigator). To prevent
    overwriting dictionary entries, a 'repeat_elem_count' dictionary counts the
    number of times that duplicate elements appear. This count is added to the
    end of the document dictionary key to differenciate from previous repeat
    entries.

    The XML element is cleared from the tree each time the text value is stored.
    """
    for doc in relevant_docs:
        repeat_elem_count = {}
        for event, elem in ET.iterparse(doc['Filename']):
            if event == 'end':
                if elem.tag in doc:
                    doc[elem.tag] = elem.text
                elif elem.tag in doc:
                    if elem.tag in repeat_elem_count:
                        repeat_elem_count[elem.tag] += 1
                    else:
                        repeat_elem_count[elem.tag] = 1
                    doc[elem.tag + str(repeat_elem_count[elem.tag])] = elem.text
            elem.clear()
        repeat_elem_count.clear()


def record_column_names(relevant_docs):
    """
    List all possible key values in document dictionary to be used as CSV fieldnames.

    The number of unique key values cannot be predetermined because some documents
    may have many repeated elements.
    """
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
    """
    Create a CSV file with one row for each XML file.
    """
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
