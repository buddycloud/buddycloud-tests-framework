import subprocess
from multiprocessing import Process
from request_utils import send_request

SERVER_URL = "http://0.0.0.0:5000"

def prepare_and_send_request(method, endpoint, client):
    headers = {
        "Accept": "application/json"
    }
    response = send_request(method, SERVER_URL + endpoint,
        headers=headers, client=client)
    return response

if __name__ == "__main__": 

    prepare_and_send_request('POST', '/shutdown', client='username')
