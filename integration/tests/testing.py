from requests import Request, Session

headers = {
	'Accept' : '*/*',
	'Accept-Encoding' : 'gzip,deflate,sdch',
	'Accept-Language' : 'en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4',
	'Cache-Control' : 'no-cache',
	'Host' : 'demo.buddycloud.org'
}

req = Request('GET', 'https://demo.buddycloud.org/api/guilherme@buddycloud.org/metadata/posts', headers=headers)

r = req.prepare()

print r.url

s = Session()
resp = s.send(r, verify=False)
print resp
print resp.ok
print resp.text
print resp.content

