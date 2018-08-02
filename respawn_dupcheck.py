# Makes a list of content links in order to checked against for duplicates.

import pyodbc

# Connect to database

# Duplicate check file

## Empty dup file

dup_check = open("dup_check.txt","w")
dup_check.write('')

## Puts content links in a text file

for urls_tocheck in dup_check:
    url_tocheck = urls_tocheck[0]
    dup_check = open("dup_check.txt","a")
    dup_check.write(str(url_tocheck))
    dup_check.close()

print ("dup check has finished")
