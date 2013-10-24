from requests import Request, Session
from requests.exceptions import Timeout, SSLError
import json, base64
from names_persistence_utils import obtainActualName

#util_dependencies
from ssl_adapter import SSLAdapter


TEST_USER_EMAIL = 'some@email.com'
TEST_USER_PASSWORD = 'a-password' #Those are not actually used for authentication


def prepare_and_send_request(request_method, request_url, payload=None, authorization=None):

	headers = {
		'Accept' : 'application/json',
		'Accept-Encoding' : 'gzip,deflate,sdch',
		'Accept-Language' : 'en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4',
		'Cache-Control' : 'no-cache',
		'Connection' : 'keep-alive',
	}

	if ( authorization != None ):
		headers['Authorization'] = "Basic " + base64.b64encode("%s:%s" % (authorization, TEST_USER_PASSWORD))

	if ( payload == None ):
		req = Request(request_method, request_url, headers=headers)
		r = req.prepare()
	else:
		headers['Content-Type'] = 'application/json'		
		req = Request(request_method, request_url, data=json.dumps(payload), headers=headers)
		r = req.prepare()

	s = Session()
	s.mount('https://', SSLAdapter('TLSv1'))

	try:
		resp = s.send(r, verify=False, timeout=200)
	except Timeout, SSLError:
		return prepare_and_send_request(request_method, request_url, payload, authorization)
	return (resp.ok, resp)

#HTTP_API endpoint: /:channel/metadata/:node
def user_channel_exists(session, domain_url, api_location, username):

	username = obtainActualName(session, username)

	(status, response) = prepare_and_send_request('GET', '%s%s@%s/metadata/posts' % (api_location, username, domain_url))

	try:
		response = json.loads(response.content)
		return status
	except ValueError:
		return False

#HTTP_API endpoint: /account
def create_user_channel(session, domain_url, api_location, username):

	username = obtainActualName(session, username)
	
	data = {
		'username' : username,
		'password' : TEST_USER_PASSWORD,
		'email' : TEST_USER_EMAIL
	}
	(status, response) = prepare_and_send_request('POST', '%saccount' % (api_location), payload=data)
	return status

#HTTP_API endpoint: /account
def delete_user_channel(session, domain_url, api_location, username):

	username = obtainActualName(session, username)

	(status, response) = prepare_and_send_request('DELETE', '%saccount' % (api_location), authorization=username)
	return status

#HTTP_API endpoint: /:channel/metadata/:node
def topic_channel_exists(session, domain_url, api_location, channel_name):

	channel_name = obtainActualName(session, channel_name)
	
	(status, response) = prepare_and_send_request('GET', '%s%s@topics.%s/metadata/posts' % (api_location, channel_name, domain_url))

	try:
		response = json.loads(response.content)
		return status
	except ValueError:
		return False

#HTTP_API endpoint: /:channel
def create_topic_channel(session, domain_url, api_location, username, channel_name):

	username = obtainActualName(session, username)
	channel_name = obtainActualName(session, channel_name)

	(status, response) = prepare_and_send_request('POST', '%s%s@topics.%s' % (api_location, channel_name, domain_url), authorization=username)
	return status

#HTTP_API endpoint: /:channel
def delete_topic_channel(session, domain_url, api_location, username, channel_name):

	username = obtainActualName(session, username)
	channel_name = obtainActualName(session, channel_name)

	(status, response) = prepare_and_send_request('DELETE', '%s%s@topics.%s' % (api_location, channel_name, domain_url), authorization=username)
	return status

#HTTP_API endpoint /:channel/metadata/:node
def is_open_user_channel(domain_url, api_location, username):

	username = obtainActualName(session, username)

	(status, response) = prepare_and_send_request('GET', '%s%s@%s/metadata/posts' % (api_location, username, domain_url))

	if status == True:

		try:
			response = json.loads(response.content)
			return 'access_model' in response and response['access_model'] == 'open'
		except ValueError:
			pass

	return False

#HTTP_API endpoint /:channel/metadata/:node
def open_this_user_channel(session, domain_url, api_location, username):

	username = obtainActualName(session, username)

	data = {
		'access_model' : 'open'
	}
	return prepare_and_send_request('POST', '%s%s@%s/metadata/posts' % (api_location, username, domain_url),
			payload=data, authorization=username)

#HTTP_API endpoint /:channel/metadata/:node
def is_authorized_user_channel(domain_url, api_location, username):

	username = obtainActualName(session, username)

	(status, response) = prepare_and_send_request('GET', '%s%s@%s/metadata/posts' % (api_location, username, domain_url))

	if status == True:

		try:
			response = json.loads(response.content)
			return 'access_model' in response and response['access_model'] == 'authorize'
		except ValueError:
			pass

	return False

#HTTP_API endpoint /:channel/metadata/:node
def close_this_user_channel(session, domain_url, api_location, username):

	username = obtainActualName(session, username)

	data = {
		'access_model' : 'authorize'
	}
	return prepare_and_send_request('POST', '%s%s@%s/metadata/posts' % (api_location, username, domain_url),
			payload=data, authorization=username)

#HTTP_API endpoint: /subscribed
def subscribe_to_user_channel(session, domain_url, api_location, username, channel_name, subscription):

	username = obtainActualName(session, username)
	channel_name = obtainActualName(session, channel_name)

	data = {
		'%s@%s/posts' % (channel_name, domain_url) : subscription
	}
	(status, response) = prepare_and_send_request('POST', '%ssubscribed' % (api_location), payload=data, authorization=username)
	return status

#HTTP_API endpoint: /:channel/subscribers/:node/approve
def approve_user_channel_subscription_request(session, domain_url, api_location, username, subscriber_jids):

	username = obtainActualName(session, username)
	subscriber_jids = map(lambda x: obtainActualName(session, x), subscriber_jids)

	data = [ {'subscription' : 'subscribed', 'jid' : jid + "@" + domain_url} for jid in subscriber_jids ]
	return prepare_and_send_request('POST', '%s%s@%s/subscribers/posts/approve' % (api_location, username, domain_url),
			payload=data, authorization=username)

#HTTP_API endpoint: /subscribed
def has_subscriber_role_in_user_channel(session, domain_url, api_location, username, channel_name, subscription):

	username = obtainActualName(session, username)
	channel_name = obtainActualName(session, channel_name)

	(status, response) = prepare_and_send_request('GET', '%ssubscribed' % (api_location), authorization=username)

	if status == True:

		try:
			response = json.loads(response.content)
			channel_node = '%s@%s/posts' % (channel_name, domain_url)
			return channel_node in response and response[channel_node] == subscription
		except ValueError:
			pass

	return False

#HTTP_API endpoint /:channel/subscribers/:node 
def change_user_channel_subscriber_role(session, domain_url, api_location, username, subscriber_username, subscription):

	username = obtainActualName(session, username)
	subscriber_username = obtainActualName(session, subscriber_username)

	data = {
		subscriber_username + "@" + domain_url : subscription
	}
	return prepare_and_send_request('POST', '%s%s@%s/subscribers/posts' % (api_location, username, domain_url),
			payload=data, authorization=username)

#HTTP_API endpoint: /subscribed
def subscribe_to_topic_channel(session, domain_url, api_location, username, channel_name, subscription):

	username = obtainActualName(session, username)
	channel_name = obtainActualName(session, channel_name)

	data = {
		'%s@topics.%s/posts' % (channel_name, domain_url) : subscription
	}
	(status, response) = prepare_and_send_request('POST', '%ssubscribed' % (api_location), payload=data, authorization=username)
	return status

#HTTP_API endpoint: /:channel/subscribers/:node/approve
def approve_topic_channel_subscription_request(session, domain_url, api_location, channel_name, owner_username, subscriber_jids):

	channel_name = obtainActualName(session, channel_name)
	owner_username = obtainActualName(session, owner_username)
	subscriber_jids = map(lambda x: obtainActualName(session, x), subscriber_jids)

	data = [ {'subscription' : 'subscribed', 'jid' : jid + "@" + domain_url} for jid in subscriber_jids ]
	return prepare_and_send_request('POST', '%s%s@topics.%s/subscribers/posts/approve' % (api_location, channel_name, domain_url),
			payload=data, authorization=owner_username)

#HTTP_API endpoint: /subscribed
def has_subscriber_role_in_topic_channel(session, domain_url, api_location, username, channel_name, subscription):

	username = obtainActualName(session, username)
	channel_name = obtainActualName(session, channel_name)

	(status, response) = prepare_and_send_request('GET', '%ssubscribed' % (api_location), authorization=username)

	if status == True:

		try:
			response = json.loads(response.content)
			channel_node = '%s@topics.%s/posts' % (channel_name, domain_url)
			return channel_node in response and response[channel_node] == subscription
		except ValueError:
			pass

	return False

#HTTP_API endpoint /:channel/subscribers/:node 
def change_topic_channel_subscriber_role(session, domain_url, api_location, owner_username, username, channel_name, subscription):

	owner_username = obtainActualName(session, owner_username)
	username = obtainActualName(session, username)
	channel_name = obtainActualName(session, channel_name)

	data = {
		username + "@" + domain_url : subscription
	}
	return prepare_and_send_request('POST', '%s%s@topics.%s/subscribers/posts' % (api_location, channel_name, domain_url),
			payload=data, authorization=owner_username)
