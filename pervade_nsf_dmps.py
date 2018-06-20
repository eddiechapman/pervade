# Import libraries
import os
import csv
import xml.etree.ElementTree as ET


def initialize_settings():
    os.chdir('C:\\Users\\chapman4\\PycharmProjects\\pervade_nsf_dmps\\dmps')
    data_mgmt_plans = []
    return data_mgmt_plans


def list_filenames():
    filenames = [name.split('.')[0] for name in os.listdir('.') if name.endswith('.xml')]
    return filenames


def list_keywords():
    search_terms = []
    with open('search_terms.txt', 'r') as infile:
        for line in infile:
            search_terms.append(line)
        return search_terms


def initialize_parser(xmlfile):

    # clear storage for data mangagement plan fields
    data_mgmt_plan = {}

    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()


def check_relevence(search_terms):

    # find abstract
    abstract = root.find('./Award/AbstractNarration').text

    # compare abstract to search terms
    if any(x in abstract for x in search_terms:
        data_mgmt_plan = collect_xml_data(root)
        return data_mgmt_plan

def collect_xml_data(root):
    # parse top level elements
    award = root.find('Award')
    award_fields = ['AwardID', 'AwardTitle', 'AwardEffectiveDate',
                    'AwardExpirationDate', 'AwardAmount', 'MinAmdLetterDate',
                    'MaxAmdLetterDate', 'ARRAAmount', 'AbstractNarration',
                    'AwardID']
    for field in award_fields:
        element = award.find(field).text
        data_mgmt_plan[field] = element
        print(field, ' = ',  element)

    org_code = root.find('./Award/Organization/Code').text
    data_mgmt_plan['OrganizationCode'] = org_code
    print('OrganizationCode', ' = ', org_code)

    org_directorate_name = root.find('./Award/Organization/Directorate/LongName').text
    data_mgmt_plan['DirectorateName'] = org_directorate_name
    print('DirectorateName', ' = ', org_directorate_name)

    org_division_name = root.find('./Award/Organization/Division/LongName').text
    data_mgmt_plan['DivisionName'] = org_division_name
    print('DivisionName', ' = ', org_division_name)

    program_officer_name = root.find('./Award/ProgramOfficer/SignBlockName').text
    data_mgmt_plan['ProgramOfficer'] = program_officer_name
    print('ProgramOfficer', ' = ', program_officer_name)

    investigators = root.findall('./Award/Investigator')
    investigator_fields = ['FirstName', 'LastName', 'EmailAddress', 'StartDate',
                           'EndDate', 'RoleCode']
    for count, investigator in enumerate(investigators, 1):
        for field in investigator_fields:
            element = investigator.find(field).text
            key = ''.join(['Investigator', field, str(count)])
            data_mgmt_plan[key] = element
            print(key, ' = ', element)

    institutions = root.findall('./Award/Institution')
    institution_fields = ['Name', 'CityName', 'ZipCode', 'PhoneNumber',
                          'StreetAddress', 'CountryName', 'StateName',
                          'StateCode']
    for count, institution in enumerate(institutions, 1):
        for field in institution_fields:
            element = institution.find(field).text
            key = ''.join(['Institution', field, str(count)])
            data_mgmt_plan[key] = element
            print(key, ' = ', element)

    foa_infos = root.findall('./Award/FoaInformation')
    foa_info_fields = ['Code', 'Text']
    for count, foa_info in enumerate(foa_infos, 1):
        for field in foa_info_fields:
            element = foa_info.find(field).text
            key = ''.join(['FOA', field, str(count)])
            data_mgmt_plan[key] = element
            print(key, ' = ', element)

    program_elements = root.findall('./Award/ProgramElement')
    program_element_fields = ['Code', 'Text']
    for count, program_element in enumerate(program_elements, 1):
        for field in program_element_fields:
            element = program_element.find(field).text
            key = ''.join(['ProgramElement', field, str(count)])
            data_mgmt_plan[key] = element
            print(key, ' = ', element)

    program_references = root.findall('./Award/ProgramReference')
    program_reference_fields = ['Code', 'Text']
    for count, program_reference in enumerate(program_references, 1):
        for field in program_reference_fields:
            element = program_reference.find(field).text
            key = ''.join(['ProgramReference', field, str(count)])
            data_mgmt_plan[key] = element
            print(key, ' = ', element)

    return data.mgmt.plan

parseXML('1764454.xml')

def main():
    data_mgmt_plan = []
    initialize_settings()
    search_terms = list_search_terms()
    filenames = list_filenames()
    for xmlfile in filenames:
        data_mgmt_plan = {}
        root = initialize_parser(xmlfile)
        if check_relevence(root, search_terms) == True:
            data = collect_xml_data(root)
            data_mgmt_plan.append(data)

        else:
            break

