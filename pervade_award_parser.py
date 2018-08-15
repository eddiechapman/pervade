import os
import csv
import itertools
import xml.etree.ElementTree as ET
from nltk import sent_tokenize, word_tokenize
from nltk.util import ngrams


def set_directory():
    """Specify where the xml and txt files are located on the user's computer."""
    os.chdir('/home/eddie/Downloads/nsf_awards')


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
            del award


def replace_abstract_html(award_fields):
    """Replace html <br/> tags with actual linebreaks."""
    for award in award_fields:
        award['abstract'] = award['abstract'].replace('<br/>', '\n')
        yield award


def tokenize_sentences(award_fields):
    """Split the abstract text into individual sentences."""
    for award in award_fields:
        award['sentence_tokens'] = sent_tokenize(award['abstract'])
        yield award


def lower_sentence_tokens(award_fields):
    """Change uppercase letters in sentence tokens to lowercase."""
    for award in award_fields:
        award['sentence_tokens'] = [token.lower() for token in award['sentence_tokens']]
        yield award


def tokenize_words(award_fields):
    """Split the abstract sentences into individual words."""
    for award in award_fields:
        award['word_tokens'] = []
        for sentence_token in award['sentence_tokens']:
            word_tokens = word_tokenize(sentence_token)
            award['word_tokens'].append(word_tokens)
        yield award


def ngram_word_tokens(award_fields):
    """Create uni-, bi-, and trigrams from abstract word tokens."""
    for award in award_fields:
        award['ngrams'] = []
        # n represents uni- bi- and trigrams
        for n in [1, 2, 3]:
            # keep ngrams sorted by sentence
            for sentence_group in award['word_tokens']:
                # create list of ngram tuples
                ngrams_array = ngrams(sentence_group, n)
                # join tuples as strings
                ngrams_joined = [' '.join(ngrams) for ngrams in ngrams_array]
                # convert list to set
                ngrams_set = set(ngrams_joined)
                award['ngrams'].append(ngrams_set)
        yield award


def query_ngrams(award_fields, search_terms):
    """By sentence, compare ngrams to search terms and save results."""
    for award in award_fields:
        award['query_hits'] = set()
        for sentence in award['ngrams']:
            query_hits = sentence.intersection(search_terms)
            if query_hits:
                print(query_hits)
                award['query_hits'] = award['query_hits'].union(query_hits)
        if award['query_hits']:
            yield award
        else:
            del award


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
        del award['word_tokens']
        del award['ngrams']
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
    award_fields = replace_abstract_html(award_fields)
    award_fields = tokenize_sentences(award_fields)
    award_fields = lower_sentence_tokens(award_fields)
    award_fields = tokenize_words(award_fields)
    award_fields = ngram_word_tokens(award_fields)
    award_fields = query_ngrams(award_fields, search_terms)
    award_fields = add_title(award_fields)
    award_fields = remove_unused_fields(award_fields)
    compile_relevant_awards(award_fields, relevant_awards)
    update_column_names(relevant_awards, column_names)
    write_csv(relevant_awards, column_names)

if __name__ == '__main__':
    main()
