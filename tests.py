import random, time, dns.resolver

#List all test funcion definitions here, they all must receive a <domain_url> parameter.
#The return value is a tuple (exit_status, output).


def lookupAPI(domain_url):
	# Look at SRV record of the given domain if the service _buddycloud-api can be found!
	answers = []
	for answer in dns.resolver.query("_buddycloud-api._tcp."+domain_url, dns.rdatatype.SRV, raise_on_no_answer=False):
		answers.append({
			'domain' : answer.target.to_text()[:-1],
			'port' : answer.port,
			'priority' : answer.priority,
			'weight' : answer.weight
		})

	found = "API server(s) found: "
	if len(answers) != 0:
		for answer in answers:
			print "Answer found:", answer
			found += answer['domain'] + " at " + str(answer['port'])
		out = found
		status = 0
	else:
		out = "Could not find any API servers!"
		status = 1

	return (status, out)


def testExample(domain_url):
	# This is a temporary test example, does nothing but wait.
	waittime = random.randint(0,10)
	time.sleep(waittime)
	out = "Waited "+str(waittime)
	status = 0
	return (status, out)


#Then for each function,
#add a new entry into the test_entries map below
#with a unique name identifier as key
#and have the respective function as value.


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
