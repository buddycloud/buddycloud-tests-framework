from requests import Request, Session
from random import random
import json

API_LOCATION = 'http://api.buddycloud.org/'
TEST_USER_EMAIL = 'email'
TEST_USER_PASSWORD = 'passwd' #Those are not actually used for authentication

def user_exists(username):

	req = Request('GET', API_LOCATION + username +'@buddycloud.org/metadata/posts')

	r = req.prepare()
	s = Session()

	if (s.send(r, verify=False)).ok :
		return True
	return False

def create_user_channel(username):

	if user_exists(username):
		return True

	headers = {'Content-Type' : 'application/json'}
	data = {'username' : username + '@buddycloud.org', 'password' : TEST_USER_PASSWORD, 'email' : TEST_USER_EMAIL}

	req = Request('POST', API_LOCATION + 'account', data=json.dumps(data), headers=headers)

	r = req.prepare()
	s = Session()

	if (s.send(r, verify=False)).ok :
		return True
	return False

def testFunction(domain_url):

	test_usernames = []

	try:

		f = open("setup_test_usernames", 'r')
		for test_username in f.xreadlines():
		
			test_usernames.append(test_username)

	except:

		f = open("setup_test_usernames", 'w')
		for i in range(5):
			
			test_username = "test_user_" + str(random()).split(".")[1]
			test_usernames.append(test_username+"\n")

		f.writelines(test_usernames)


	status = 0
	briefing = ""
	message = ""

	for test_username in test_usernames:
		
		test_username = test_username.strip()

		if create_user_channel(test_username):
			continue
		else:
			status = 1
			briefing = "Could not create user channel for test user named " + test_username
			message = briefing
			return (status, briefing, message, None)

	briefing = "Could successfully create all test user channels needed for integration tests"
	message = briefing
	return (status, briefing, message, None)
