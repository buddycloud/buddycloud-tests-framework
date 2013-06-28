from requests import Request, Session
from random import random
import json, base64

API_LOCATION = 'https://demo.buddycloud.org/api/'
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

	# First of all, read or create a file with 5 different test usernames in the format test_user_<integer>.

	test_usernames = []
	test_channel_name = ""

	try:

		f = open("setup_test_usernames", 'r')
		for test_username in f.xreadlines():
		
			test_usernames.append(test_username)

		g = open("setup_test_channel_name", 'r')
		test_channel_name = g.read()

	except:

		f = open("setup_test_usernames", 'w')
		for i in range(5):
			
			test_username = "test_user_" + str(random()).split(".")[1]
			test_usernames.append(test_username+"\n")

		f.writelines(test_usernames)

		g = open("setup_test_channel_name", 'w')
		test_channel_name = "test_channel_" + str(random()).split(".")[1]
		g.write(test_channel_name+"\n")

	finally:
		f.close()
		g.close()

	status = 0
	briefing = ""
	message = ""

	# Then, create a user channel for each of these usernames, if that does not exist yet.

	for test_username in test_usernames:
		
		test_username = test_username.strip()

		if create_user_channel(test_username):
			continue
		else:
			status = 1
			briefing = "Could not create user channel for test user named " + test_username
			message = briefing
			return (status, briefing, message, None)


	# Then, have user[1] create a topics channel. Assert he is a producer of that channel.

#	headers = {'Authorization' : 'Basic ' + base64.b64encode(test_usernames[0]+":"+TEST_USER_PASSWORD)}
#	req = Request('POST', API_LOCATION + test_channel_name, headers=headers)

	# Then, have user[2] join the topic channel. Have user[1] make user[2] moderator of that channel. Assert user[2] is a moderator of that channel.	

#	headers = {'Authorization' : 'Basic ' + base64.b64encode(test_usernames[1]+":"+TEST_USER_PASSWORD)}
#	data = {
#		test_channel_name : "publisher"
#	}
#	req = Request('POST', API_LOCATION + "/subscribed", data=json.dumps(data), headers=headers)

	# Then, have user[3] join the topic channel. Have user[1] give posting permission to user[3]. Assert user[3] is a follower+post of that channel.

	# Then, have user[4] join the topic channel. Assert user[4] is a follower of that channel.

	# Then, have user[5] join the topic channel. Have user[1] ban user[5] in that channel. Assert user[5] is banned in that channel.

	briefing = "Could successfully create all test user channels needed for integration tests"
	message = briefing
	return (status, briefing, message, None)
