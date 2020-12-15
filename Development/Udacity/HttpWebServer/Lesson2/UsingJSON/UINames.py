import requests

uri = 'http://uinames.com/api?'
param = 'ext&region=Italy'
print(uri+param)
r = requests.get(uri+param)
print(r)
