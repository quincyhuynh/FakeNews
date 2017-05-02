import csv

# read tab-delimited file
with open('Data_3-31.csv','r') as fin:
    cr = csv.reader(fin, delimiter='\t')
    filecontents = [line for line in cr]

# write comma-delimited file (comma is the default delimiter)
with open('test_data.csv','w') as fou:
    cw = csv.writer(fou, quotechar='', quoting=csv.QUOTE_NONE)
    cw.writerows(filecontents)