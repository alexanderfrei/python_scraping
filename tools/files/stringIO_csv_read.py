from urllib.request import urlopen
from io import StringIO
import csv
import pandas as pd

data = urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv").read().decode('ascii', 'ignore')
dataFile = StringIO(data)

# csvReader = csv.reader(dataFile)
# for row in csvReader:
#     print("The album \""+row[0]+"\" was released in "+str(row[1]))

# convenient way:

dictReader = csv.DictReader(dataFile)
print(dictReader.fieldnames)
for row in dictReader:
    print(row)
