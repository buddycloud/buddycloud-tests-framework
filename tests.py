import random, time
from xmpp_server_tests import xmppServerServiceRecordLookup, xmppServerAddressRecordLookup, xmppServerConnection
from buddycloud_server_tests import buddycloudServerDisco
from api_server_tests import apiLookup, apiConnection

def testExample(domain_url):
	# This is a temporary test example, does nothing but wait.
	waittime = random.randint(0,10)
	time.sleep(waittime)
	out = "Waited "+str(waittime)
	status = 0
	return (status, out)

def testFailExample(domain_url):
	# This is a temporary test example, does nothing but wait.
	waittime = random.randint(0,10)
	time.sleep(waittime)
	out = "Failed to wait "+str(waittime)
	status = 1
	return (status, out)

#Test entries: tests to be performed in order by the inspector, each have a name and a function
test_entries = []
test_entries.append({'name' : 'xmpp_server_srv_lookup', 'test' : xmppServerServiceRecordLookup, 'continue_if_fail' : False })
test_entries.append({'name' : 'xmpp_server_a_lookup', 'test' : xmppServerAddressRecordLookup, 'continue_if_fail' : False })
test_entries.append({'name' : 'xmpp_server_connection', 'test' : xmppServerConnection, 'continue_if_fail' : False })
test_entries.append({'name' : 'buddycloud_server_disco', 'test' : buddycloudServerDisco, 'continue_if_fail' : False })
test_entries.append({'name' : 'api_lookup', 'test' : apiLookup, 'continue_if_fail' : False })
test_entries.append({'name' : 'api_connection', 'test' : apiConnection, 'continue_if_fail' : False })
test_entries.append({'name' : 'test_example2', 'test' : testFailExample, 'continue_if_fail' : True })
test_entries.append({'name' : 'test_example3', 'test' : testFailExample, 'continue_if_fail' : True })
test_entries.append({'name' : 'test_example4', 'test' : testExample, 'continue_if_fail' : True })
test_entries.append({'name' : 'test_example5', 'test' : testExample, 'continue_if_fail' : True })
test_entries.append({'name' : 'test_example6', 'test' : testFailExample, 'continue_if_fail' : True })
test_entries.append({'name' : 'test_example7', 'test' : testExample, 'continue_if_fail' : True })
test_entries.append({'name' : 'test_example8', 'test' : testFailExample, 'continue_if_fail' : True })
test_entries.append({'name' : 'test_example9', 'test' : testExample, 'continue_if_fail' : True })

test_names = {
'xmpp_server_srv_lookup' : 0,
'xmpp_server_a_lookup' : 1,
'xmpp_server_connection' : 2,
'buddycloud_server_disco' : 3,
'api_lookup' : 4,
'api_connection' : 5,
'test_example2' : 6,
'test_example3' : 7,
'test_example4' : 8,
'test_example5' : 9,
'test_example6' : 10,
'test_example7' : 11,
'test_example8' : 12,
'test_example9' : 13
}
