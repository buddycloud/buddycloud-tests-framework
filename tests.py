import random, time
from xmpp_server_tests import xmppServerSRVLookup, xmppServerAddressRecordLookup, xmppServerConnectionTest
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
test_entries.append({'name' : 'xmpp_server_srv_lookup', 'test' : xmppServerSRVLookup, 'continue_if_fail' : False })
test_entries.append({'name' : 'xmpp_server_a_lookup', 'test' : xmppServerAddressRecordLookup, 'continue_if_fail' : False })
test_entries.append({'name' : 'xmpp_server_connection', 'test' : xmppServerConnectionTest, 'continue_if_fail' : False })
test_entries.append({'name' : 'test_example1', 'test' : testExample, 'continue_if_fail' : True })
test_entries.append({'name' : 'test_example2', 'test' : testFailExample, 'continue_if_fail' : True })
test_entries.append({'name' : 'lookup_api', 'test' : lookupAPI, 'continue_if_fail' : False })
#test_entries.append({'name' : 'test_example3', 'test' : testExample, 'continue_if_fail' : True })
#test_entries.append({'name' : 'test_example4', 'test' : testExample, 'continue_if_fail' : True })
#test_entries.append({'name' : 'test_example5', 'test' : testFailExample, 'continue_if_fail' : True })
#test_entries.append({'name' : 'test_example6', 'test' : testExample, 'continue_if_fail' : True })
#test_entries.append({'name' : 'test_example7', 'test' : testExample, 'continue_if_fail' : True })
#test_entries.append({'name' : 'test_example8', 'test' : testFailExample, 'continue_if_fail' : True })
#test_entries.append({'name' : 'test_example9', 'test' : testExample, 'continue_if_fail' : True })
#test_entries.append({'name' : 'test_example10', 'test' : testExample, 'continue_if_fail' : True })
#test_entries.append({'name' : 'test_example11', 'test' : testExample, 'continue_if_fail' : True })
#test_entries.append({'name' : 'test_example12', 'test' : testFailExample, 'continue_if_fail' : True })

test_names = {
'xmpp_server_srv_lookup' : 0,
'xmpp_server_a_lookup' : 1,
'xmpp_server_connection' : 2,
'test_example1' : 3,
'test_example2' : 4,
'lookup_api' : 5
}
#'test_example3' : 6,
#'test_example4' : 7,
#'test_example5' : 8,
#'test_example6' : 9,
#'test_example7' : 10,
#'test_example8' : 11,
#'test_example9' : 12,
#'test_example10' : 13,
#'test_example11' : 14,
#'test_example12' : 15,
#}
