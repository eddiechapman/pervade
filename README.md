# PERVADE Award Parser

This program parses National Science Foundataion (NSF) award data in XML format and stores elements of relevant awards in a CSV file. 

Part of the PERVADE project on internet research ethics: https://pervade.umd.edu/about/


## Getting Started

Download the NSF award data dumps by year from https://www.nsf.gov/awardsearch/download.jsp. Extract all XML files to a shared folder. 

Modify or create a text file called 'search_terms.txt'. Add one search term per line. Store the file in the folder with the XML files.

In pervade_award_parser.py, edit the path in set_directory() to reflect the location of the XML files. 

