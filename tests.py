import random, time

def lookupAPI(domain_url):
	# Look at SRV record of the given domain if the service _buddycloud-api can be found!
	out = "executed lookupAPI test"
	err = "none"
	return "OUT: "+str(out)+", ERR: "+str(err)


def testExample(domain_url):
	# This is a temporary test example, does nothing but wait.
	waittime = random.randint(0,10)
	time.sleep(waittime)
	return "OUT: waited"+str(waittime)


#Test entries: tests to be performed by the inspector, each have a name and a function
test_entries = {}
test_entries['lookupAPI'] = lookupAPI
test_entries['testExample1'] = testExample 
test_entries['testExample2'] = testExample 
test_entries['testExample3'] = testExample 
test_entries['testExample4'] = testExample 
test_entries['testExample5'] = testExample 
test_entries['testExample6'] = testExample 
test_entries['testExample7'] = testExample 
test_entries['testExample8'] = testExample 
test_entries['testExample9'] = testExample 
test_entries['testExample10'] = testExample
