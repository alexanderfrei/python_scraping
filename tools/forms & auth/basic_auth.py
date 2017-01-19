import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('frei', 'password')
r = requests.post(url="http://pythonscraping.com/pages/auth/login.php", auth=auth)
print(r.text)
