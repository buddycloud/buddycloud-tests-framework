from requests import Request, Session
from requests.exceptions import Timeout, SSLError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import json


clients = {}

class SSLAdapter(HTTPAdapter):
    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_version = ssl_version
        super(SSLAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
            maxsize=maxsize, block=block,
            ssl_version=self.ssl_version)

def send_request(method, url, payload=None, headers=None, client=None):

    if ( client == None ):
        s = Session()
        s.mount('https://', SSLAdapter('TLSv1'))
    elif ( clients.get(client, False) ):
        s = clients[client]
    else:
        s = Session()
        s.mount('https://', SSLAdapter('TLSv1'))
        clients[client] = s

    if ( payload == None ):
        request = Request(method, url, headers=headers)
        r = s.prepare_request(request)
    else:
        if ( headers == None ):
            headers = {}
        request = Request(method, url,
            data=json.dumps(payload), headers=headers)
        r = s.prepare_request(request)

    try:
        response = s.send(r, verify=False, timeout=1)
    except Timeout, SSLError:
        return send_request(method, url, payload, client)

    return {
        'success': response.ok,
        'code': response.status_code,
        'content': response.content
    }
