# pervade

### About
A program to parse XML files from the National Science Foundation's database of successful grant applications. Returns a CSV file of the desired grant applications based on keywords provided in a text file. 

### Issues
Currently the process to loop through fields is wonky. Some fields (institution, investigator etc.) can appear multiple times and have multiple subfields. I need to reduce the amount of duplication because the current script is creating columns for fields that could never exist. 

I also need to improve the keyword searching feature. I didn't really test it out. It would be good if it saved the number of keywords or phrases that were a match. 

A number of applications do not have abstracts, which is how relevance is being determined. It would be good to save a list of these for future manual inspection. 

Also, code name references to "data management plans" are misleading because we don't actually have those yet. Rather, they should be called "grant applications". 
