import requests

params = {'firstname': 'name', 'lastname': 'ururu'}
r = requests.post("http://pythonscraping.com/files/processing.php", data=params)
print(r.text)