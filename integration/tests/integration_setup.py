from requests import Request, Session
from random import random
import json, base64

#util_dependencies
from ssl_adapter import SSLAdapter

#installation_suite_dependencies
from api_server_lookup import testFunction as apiLookup


TEST_USER_EMAIL = 'email@email.com'
TEST_USER_PASSWORD = 'passwd' #Those are not actually used for authentication

def user_exists(api_host, api_location, username):

	headers = {
		'Accept' : '*/*',
		'Accept-Encoding' : 'gzip,deflate,sdch',
		'Accept-Language' : 'en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4',
		'Cache-Control' : 'no-cache',
		'Connection' : 'keep-alive',
	}

	req = Request('GET', api_location + username +'@' + api_host + '/metadata/posts', headers=headers)
	r = req.prepare()

	s = Session()
	s.mount('https://', SSLAdapter('TLSv1'))

	if (s.send(r, verify=False)).ok :
		return True
	return False

def create_user_channel(api_host, api_location, username):

	if user_exists(api_host, api_location, username):
		return True

	headers = {
		'Content-Type' : 'application/json',
		'Accept' : '*/*',
		'Accept-Encoding' : 'gzip,deflate,sdch',
		'Accept-Language' : 'en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4',
		'Cache-Control' : 'no-cache',
		'Connection' : 'keep-alive',
	}
	data = {'username' : username, 'password' : TEST_USER_PASSWORD, 'email' : TEST_USER_EMAIL}

	req = Request('POST', api_location + 'account', data=json.dumps(data), headers=headers)
	r = req.prepare()
	
	s = Session()
	s.mount('https://', SSLAdapter('TLSv1'))

	if (s.send(r, verify=False)).ok :
		return True
	return False

def topic_channel_exists(api_host, api_location, channel_name):

	headers = {
		'Accept' : '*/*',
		'Accept-Encoding' : 'gzip,deflate,sdch',
		'Accept-Language' : 'en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4',
		'Cache-Control' : 'no-cache',
		'Connection' : 'keep-alive',
	}
	
	req = Request('GET', api_location + channel_name +'@topics.' + api_host + '/metadata/posts', headers=headers)
	r = req.prepare()

	s = Session()
	s.mount('https://', SSLAdapter('TLSv1'))

	if (s.send(r, verify=False)).ok :
		return True
	return False

def create_topic_channel(api_host, api_location, username, channel_name):

	if topic_channel_exists(api_location, channel_name):
		return True

	headers = {
		'Content-Type' : 'application/json',
		'Accept' : '*/*',
		'Accept-Encoding' : 'gzip,deflate,sdch',
		'Accept-Language' : 'en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4',
		'Cache-Control' : 'no-cache',
		'Connection' : 'keep-alive',
		'Authorization' : 'Basic ' + base64.b64encode(username+":"+TEST_USER_PASSWORD)
	}

	req = Request('POST', api_location + channel_name + "@topics." + api_host + "", headers=headers)
	r = req.prepare()

	s = Session()
	s.mount("https://", SSLAdapter("TLSv1"))

	if (s.send(r, verify=False)).ok :

		data = {
			"default_affiliation": "member"
		}

		req = Request('POST', api_location + channel_name + "@topics." + api_host + "/metadata/posts", data=json.dumps(data), headers=headers)
		r = req.prepare()

		s = Session()
		s.mount("https://", SSLAdapter("TLSv1"))

		if (s.send(r, verify=False)).ok :
			return True
	return False

def subscribe_to_channel(api_host, api_location, username, channel_name, subscription):

	headers = {
		'Accept' : '*/*',
		'Accept-Encoding' : 'gzip,deflate,sdch',
		'Accept-Language' : 'en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4',
		'Cache-Control' : 'no-cache',
		'Connection' : 'keep-alive',
		'Content-Type' : 'application/json',
		'Authorization' : 'Basic ' + base64.b64encode(username+":"+TEST_USER_PASSWORD)
	}

	data = {
		channel_name + "@topics." + api_host + "/posts" : subscription
	}

	req = Request('POST', api_location + "/subscribed", data=json.dumps(data), headers=headers)
	r = req.prepare()

	s = Session()
	s.mount("https://", SSLAdapter("TLSv1"))

	if (not s.send(r, verify=False).ok):
		status = 1
		briefing = "User " + username + "@" + api_host + " could not subscribe to topic channel named " + channel_name + "@topics." + api_host + "."
		message = briefing
		return (status, briefing, message, None)

def is_subscribed_to_channel(api_host, api_location, username, channel_name, subscription):

	headers = {
		'Accept' : '*/*',
		'Accept-Encoding' : 'gzip,deflate,sdch',
		'Accept-Language' : 'en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4',
		'Cache-Control' : 'no-cache',
		'Connection' : 'keep-alive',
		'Authorization' : 'Basic ' + base64.b64encode(username+":"+TEST_USER_PASSWORD)
	}

	req = Request('GET', api_location + "/subscribed", headers=headers)
	r = req.prepare()

	s = Session()
	s.mount("https://", SSLAdapter("TLSv1"))

	resp = s.send(r, verify=False)

	if (not resp.ok):

		status = 1
		briefing = "Could not assert that user " + username + "@" + api_host + " is subscribed:'owner' of topic channel named " + channel_name + "@topics." + api_host + "."
		message = briefing
		return (status, briefing, message, None)
	else:

		resp = json.loads(resp.content)

		if (not (channel_name + "@topics." + api_host + "/posts") in resp) or (resp[(channel_name + "@topics." + api_host + "/posts")] != subscription):
			status = 1
			briefing = "Problem: " + username + "@" + api_host + " is not subscribed:'owner' of topic channel named " + channel_name + "@topics." + api_host + "."
			message = briefing
			return (status, briefing, message, None)

def testFunction(domain_url):

	#First of all, let's find the API server

	status, briefing, message, answers = apiLookup(domain_url)
	if ( status != 0 ):
		return (status, briefing, message, None)

	if ( len(answers) == 0 ):

		briefing = "No API server TXT record found!"
		status = 1
		message = "We could not find your API server TXT record!"
		message += "You must setup your DNS to point to the API server endpoint using a TXT record similat to the one below: "
		message += "<br/><br/>_buddycloud-api._tcp.EXAMPLE.COM.          IN TXT \"v=1.0\" \"host=buddycloud.EXAMPLE.COM\" \"protocol=https\" \"path=/api\" \"port=443\""
		return (status, briefing, message, None)

	api_host = answers[0]['domain']
	api_location = answers[0]['protocol'] + "://" + answers[0]['domain'] + answers[0]['path'] + "/"

	# Then, read or create a file with 5 different test usernames in the format test_user_<integer>.

	test_usernames = []
	test_channel_name = ""

	try:

		f = open("setup_test_usernames", 'r')
		for test_username in f.xreadlines():
		
			test_usernames.append(test_username.strip())

		g = open("setup_test_channel_name", 'r')
		test_channel_name = g.read().strip()

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

	# Then, create a user channel for each of these usernames, if that does not exist yet.

	for test_username in test_usernames:

		test_username = test_username.strip()

		if create_user_channel(api_host, api_location, test_username):
			continue
		else:
			status = 1
			briefing = "Could not create user channel for test user named " + test_username + "@" + api_host + "."
			message = briefing
			return (status, briefing, message, None)


	# Then, have user[1] create a topics channel. Assert he is a producer of that channel.

	test_channel_name = test_channel_name.strip()

	if not create_topic_channel(api_host, api_location, test_usernames[0], test_channel_name) :
		status = 1
		briefing = "Could not create topic channel named " + test_channel_name + "@topics." + api_host + "."
		message = briefing
		return (status, briefing, message, None)

	is_subscribed_to_channel(api_host, api_location, test_usernames[0], test_channel_name, "owner")

	# Then, have user[2] join the topic channel. Have user[1] make user[2] moderator of that channel. Assert user[2] is a moderator of that channel.	

	subscribe_to_channel(api_host, api_location, test_usernames[1], test_channel_name, "publisher")
	is_subscribed_to_channel(api_host, api_location, test_usernames[1], test_channel_name, "publisher")

	#TODO see how to promote test_user[1] to moderator (and not only a producer!!)

	# Then, have user[3] join the topic channel. Have user[1] give posting permission to user[3]. Assert user[3] is a follower+post of that channel.

	subscribe_to_channel(api_host, api_location, test_usernames[2], test_channel_name, "publisher")
	is_subscribed_to_channel(api_host, api_location, test_usernames[2], test_channel_name, "publisher")

	# Then, have user[4] join the topic channel. Assert user[4] is a follower of that channel.

	subscribe_to_channel(api_host, api_location, test_usernames[3], test_channel_name, "member")
	is_subscribed_to_channel(api_host, api_location, test_usernames[3], test_channel_name, "member")

	# Then, have user[5] join the topic channel. Have user[1] ban user[5] in that channel. Assert user[5] is banned in that channel.

	subscribe_to_channel(api_host, api_location, test_usernames[4], test_channel_name, "member")
	is_subscribed_to_channel(api_host, api_location, test_usernames[4], test_channel_name, "member")

	#TODO have this user test_usernames[4]@buddycloud.org be banned from this topic channel test_channel_name@topics.buddycloud.org

	briefing = "Integration test suite setup procedures executed properly. Ready to run integration tests."
	message = briefing
	message += "<br/>Could successfully create all test user channels and topic channels needed for incoming integration tests."
	return (status, briefing, message, None)
