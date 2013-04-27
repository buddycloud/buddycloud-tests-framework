import random, time
from xmpp_server_tests import xmppServerServiceRecordLookup, xmppServerAddressRecordLookup, xmppServerConnection
from buddycloud_server_tests import buddycloudServerDisco
from api_server_tests import lookupAPI

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
test_entries.append({'name' : 'lookup_api', 'test' : lookupAPI, 'continue_if_fail' : False })
test_entries.append({'name' : 'test_example1', 'test' : testExample, 'continue_if_fail' : True })
test_entries.append({'name' : 'test_example2', 'test' : testFailExample, 'continue_if_fail' : True })
test_entries.append({'name' : 'test_example3', 'test' : testFailExample, 'continue_if_fail' : False })

test_names = {
'xmpp_server_srv_lookup' : 0,
'xmpp_server_a_lookup' : 1,
'xmpp_server_connection' : 2,
'buddycloud_server_disco' : 3,
'lookup_api' : 4,
'test_example1' : 5,
'test_example2' : 6,
'test_example3' : 7
}
