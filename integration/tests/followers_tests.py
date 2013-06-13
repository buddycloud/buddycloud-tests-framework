from requests import Request, Session
import json

headers = {'Content-Type' : 'application/json'}
data = {'username' : 'inspectorX@buddycloud.org', 'password' : 'senha', 'email' : 'inspector@gmail.com'}

req = Request('POST', 'http://api.buddycloud.org/account', data=json.dumps(data), headers=headers)

r = req.prepare()
s = Session()
print s.send(r)
