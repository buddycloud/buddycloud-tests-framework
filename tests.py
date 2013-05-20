import random, time
from xmpp_server_tests import xmppServerServiceRecordLookup, xmppServerAddressRecordLookup, xmppServerConnection
from buddycloud_server_tests import buddycloudServerDisco
from api_server_tests import apiLookup, apiHTTPSConnection
from push_server_tests import pushServerDisco

def testExample(domain_url):
	# This is a temporary test example, does nothing but wait.
	waittime = random.randint(0,10)
	time.sleep(waittime)
	briefing = "Waited "+str(waittime)
	status = 0
	message = "This is a test example designed to wait "+str(waittime)+" and then succeed."
	return (status, briefing, message)

def testFailExample(domain_url):
	# This is a temporary test example, does nothing but wait.
	waittime = random.randint(0,10)
	time.sleep(waittime)
	briefing = "Failed to wait "+str(waittime)
	status = 1
	message = "This is a test example designed to wait "+str(waittime)+" and then fail."
	return (status, briefing, message)

#Test entries: tests to be performed in order by the inspector, each have a name and a function
test_entries = []
test_entries.append({'name' : 'xmpp_server_srv_lookup', 'test' : xmppServerServiceRecordLookup, 'continue_if_fail' : False })
test_entries.append({'name' : 'xmpp_server_a_lookup', 'test' : xmppServerAddressRecordLookup, 'continue_if_fail' : False })
test_entries.append({'name' : 'xmpp_server_connection', 'test' : xmppServerConnection, 'continue_if_fail' : False })
test_entries.append({'name' : 'buddycloud_server_disco', 'test' : buddycloudServerDisco, 'continue_if_fail' : False })
test_entries.append({'name' : 'api_lookup', 'test' : apiLookup, 'continue_if_fail' : False })
test_entries.append({'name' : 'api_https_connection', 'test' : apiHTTPSConnection, 'continue_if_fail' : True }) 
test_entries.append({'name' : 'push_server_disco', 'test' : pushServerDisco, 'continue_if_fail' : True })
test_entries.append({'name' : 'test_ex_1', 'test' : testFailExample, 'continue_if_fail' : True })
test_entries.append({'name' : 'test_ex_2', 'test' : testExample, 'continue_if_fail' : False })

test_names = {
'xmpp_server_srv_lookup' : 0,
'xmpp_server_a_lookup' : 1,
'xmpp_server_connection' : 2,
'buddycloud_server_disco' : 3,
'api_lookup' : 4,
'api_https_connection' : 5,
'push_server_disco' : 6,
'test_ex_1' : 7,
'test_ex_2' : 8
}
