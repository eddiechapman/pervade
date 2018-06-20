# Import libraries
import os
import csv
import xml.etree.ElementTree as ET

def initialize_settings():
    os.chdir('C:\\Users\\chapman4\\PycharmProjects\\pervade_nsf_dmps\\dmps')
    data_mgmt_plan = []
    return data_mgmt_plan


def list_filenames():
    filenames = [name.split('.')[0] for name in os.listdir('.') if name.endswith('.xml')]
    return filenames


def list_search_terms():
    with open('search_terms.txt', 'r') as infile:
        search_terms = []
        for line in infile:
            search_terms.append(line)
        return search_terms


def initialize_parser(xmlfile):
    # create element tree object
    tree = ET.parse(xmlfile + '.xml')
    # get root element
    root = tree.getroot()
    return root


def check_relevance(root, search_terms, xmlfile):
    # initialize relevance
    relevance = 0
    try:
        # search for abstract
        abstract = root.find('./Award/AbstractNarration').text
        # compare abstract to search terms
        if any(x in abstract for x in search_terms):
            relevance += 1
    except TypeError:
        print(xmlfile, 'No Abstract')
    return relevance


def collect_xml_data(root):
    # initialize storage for extracted XML data
    data_mgmt_plan = {}

    # top-level XML nodes. Most content is located in child node ('fields').
    nodes = [
        'Investigator', 'Institution', 'FoaInformation', 'ProgramElement',
        'ProgramReference'
    ]

    multi_fields = [
        'FirstName', 'LastName', 'EmailAddress',
        'StartDate', 'EndDate', 'RoleCode', 'Name', 'CityName', 'ZipCode',
        'PhoneNumber', 'StreetAddress', 'CountryName', 'StateName', 'StateCode',
        'Code', 'Text'
    ]

    for node in nodes:
        sections = root.findall('./Award/' + node)
        for count, section in enumerate(sections, 1):
            for field in multi_fields:
                try:
                    element = section.find(field).text
                    key = ''.join([node, field, str(count)])
                    data_mgmt_plan[key] = element
                    print(key, ' = ', element)
                except Exception:
                    print(field, Exception)

    single_fields = [
        'AwardID', 'AwardTitle', 'AwardEffectiveDate', 'AwardExpirationDate',
        'AwardAmount', 'MinAmdLetterDate', 'MaxAmdLetterDate', 'ARRAAmount',
        'AbstractNarration', 'AwardID'
    ]

    for field in single_fields:
        element = root.find('./Award/' + field).text
        data_mgmt_plan[field] = element
        print(field, ' = ', element)

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

    return data_mgmt_plan


def write_csv(data_mgmt_plans):
    fieldnames = [
        'InvestigatorFirstName1', 'InvestigatorLastName1', 'InvestigatorEmailAddress1',
        'InvestigatorStartDate1', 'InvestigatorEndDate1', 'InvestigatorRoleCode1',
        'InvestigatorName1', 'InvestigatorCityName1', 'InvestigatorZipCode1',
        'InvestigatorPhoneNumber1', 'InvestigatorStreetAddress1', 'InvestigatorCountryName1',
        'InvestigatorStateName1', 'InvestigatorStateCode1', 'InvestigatorCode1',
        'InvestigatorText1', 'InvestigatorFirstName2', 'InvestigatorLastName2',
        'InvestigatorEmailAddress2', 'InvestigatorStartDate2', 'InvestigatorEndDate2',
        'InvestigatorRoleCode2', 'InvestigatorName2', 'InvestigatorCityName2',
        'InvestigatorZipCode2', 'InvestigatorPhoneNumber2', 'InvestigatorStreetAddress2',
        'InvestigatorCountryName2', 'InvestigatorStateName2', 'InvestigatorStateCode2',
        'InvestigatorCode2', 'InvestigatorText2', 'InstitutionFirstName1',
        'InstitutionLastName1', 'InstitutionEmailAddress1', 'InstitutionStartDate1',
        'InstitutionEndDate1', 'InstitutionRoleCode1', 'InstitutionName1',
        'InstitutionCityName1', 'InstitutionZipCode1', 'InstitutionPhoneNumber1',
        'InstitutionStreetAddress1', 'InstitutionCountryName1', 'InstitutionStateName1',
        'InstitutionStateCode1', 'InstitutionCode1', 'InstitutionText1',
        'ProgramElementFirstName1', 'ProgramElementLastName1', 'ProgramElementEmailAddress1',
        'ProgramElementStartDate1', 'ProgramElementEndDate1', 'ProgramElementRoleCode1',
        'ProgramElementName1', 'ProgramElementCityName1', 'ProgramElementZipCode1',
        'ProgramElementPhoneNumber1', 'ProgramElementStreetAddress1', 'ProgramElementCountryName1',
        'ProgramElementStateName1', 'ProgramElementStateCode1', 'ProgramElementCode1',
        'ProgramElementText1', 'ProgramElementFirstName2', 'ProgramElementLastName2',
        'ProgramElementEmailAddress2', 'ProgramElementStartDate2', 'ProgramElementEndDate2',
        'ProgramElementRoleCode2', 'ProgramElementName2', 'ProgramElementCityName2',
        'ProgramElementZipCode2', 'ProgramElementPhoneNumber2', 'ProgramElementStreetAddress2',
        'ProgramElementCountryName2', 'ProgramElementStateName2', 'ProgramElementStateCode2',
        'ProgramElementCode2', 'ProgramElementText2', 'ProgramReferenceFirstName1',
        'ProgramReferenceLastName1', 'ProgramReferenceEmailAddress1', 'ProgramReferenceStartDate1',
        'ProgramReferenceEndDate1', 'ProgramReferenceRoleCode1', 'ProgramReferenceName1',
        'ProgramReferenceCityName1', 'ProgramReferenceZipCode1', 'ProgramReferencePhoneNumber1',
        'ProgramReferenceStreetAddress1', 'ProgramReferenceCountryName1', 'ProgramReferenceStateName1',
        'ProgramReferenceStateCode1', 'ProgramReferenceCode1', 'ProgramReferenceText1',
        'ProgramReferenceFirstName2', 'ProgramReferenceLastName2', 'ProgramReferenceEmailAddress2',
        'ProgramReferenceStartDate2', 'ProgramReferenceEndDate2', 'ProgramReferenceRoleCode2',
        'ProgramReferenceName2', 'ProgramReferenceCityName2', 'ProgramReferenceZipCode2',
        'ProgramReferencePhoneNumber2', 'ProgramReferenceStreetAddress2', 'ProgramReferenceCountryName2',
        'ProgramReferenceStateName2', 'ProgramReferenceStateCode2', 'ProgramReferenceCode2',
        'ProgramReferenceText2', 'ProgramReferenceFirstName3', 'ProgramReferenceLastName3',
        'ProgramReferenceEmailAddress3', 'ProgramReferenceStartDate3', 'ProgramReferenceEndDate3',
        'ProgramReferenceRoleCode3', 'ProgramReferenceName3', 'ProgramReferenceCityName3',
        'ProgramReferenceZipCode3', 'ProgramReferencePhoneNumber3', 'ProgramReferenceStreetAddress3',
        'ProgramReferenceCountryName3', 'ProgramReferenceStateName3', 'ProgramReferenceStateCode3',
        'ProgramReferenceCode3', 'ProgramReferenceText3', 'ProgramReferenceFirstName4',
        'ProgramReferenceLastName4', 'ProgramReferenceEmailAddress4', 'ProgramReferenceStartDate4',
        'ProgramReferenceEndDate4', 'ProgramReferenceRoleCode4', 'ProgramReferenceName4',
        'ProgramReferenceCityName4', 'ProgramReferenceZipCode4', 'ProgramReferencePhoneNumber4',
        'ProgramReferenceStreetAddress4', 'ProgramReferenceCountryName4', 'ProgramReferenceStateName4',
        'ProgramReferenceStateCode4', 'ProgramReferenceCode4', 'ProgramReferenceText4', 'AwardID',
        'AwardTitle', 'AwardEffectiveDate', 'AwardExpirationDate', 'AwardAmount', 'MinAmdLetterDate',
        'MaxAmdLetterDate', 'ARRAAmount', 'AbstractNarration', 'OrganizationCode', 'DirectorateName',
        'DivisionName', 'ProgramOfficer', 'InvestigatorEndDate3', 'InvestigatorCityName3',
        'InvestigatorStreetAddress3', 'InvestigatorFirstName3', 'InvestigatorText3',
        'InvestigatorEmailAddress3', 'InvestigatorCode3', 'InvestigatorRoleCode3',
        'InvestigatorStateCode3', 'InvestigatorLastName3', 'InvestigatorStartDate3',
        'InvestigatorZipCode3', 'InvestigatorCountryName3', 'InvestigatorPhoneNumber3',
        'InvestigatorStateName3', 'InvestigatorName3', 'ProgramReferenceStateName5',
        'ProgramReferenceRoleCode5', 'ProgramReferenceLastName5', 'ProgramReferenceStreetAddress5',
        'ProgramReferenceStartDate5', 'ProgramReferenceZipCode5', 'ProgramReferenceStateCode5',
        'ProgramReferenceFirstName5', 'ProgramReferenceName5', 'ProgramReferenceText5',
        'ProgramReferenceCountryName5', 'ProgramReferenceCityName5', 'ProgramReferenceEndDate5',
        'ProgramReferenceCode5', 'ProgramReferenceEmailAddress5', 'ProgramReferencePhoneNumber5',
        'ProgramElementCode3', 'ProgramElementText3', 'InvestigatorLastName4', 'ProgramReferenceText6',
        'InvestigatorStartDate4', 'InvestigatorEmailAddress4', 'ProgramReferenceCode6', 'InvestigatorRoleCode4',
        'InvestigatorEndDate4', 'InvestigatorFirstName4', 'ProgramElementText4', 'ProgramElementCode4'
        ]

    with open('nsf_dmps.csv', 'w') as csv_file:

        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
        writer.writerows(data_mgmt_plans)


def main():
    data_mgmt_plans = initialize_settings()
    search_terms = list_search_terms()
    filenames = list_filenames()
    for xmlfile in filenames:
        root = initialize_parser(xmlfile)
        if check_relevance(root, search_terms, xmlfile) == True:
            data_mgmt_plan = collect_xml_data(root)
            data_mgmt_plans.append(data_mgmt_plan)
        else:
            continue
    write_csv(data_mgmt_plans)

main()
