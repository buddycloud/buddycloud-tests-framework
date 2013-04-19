import random, time, dns.resolver

#List all test funcion definitions here, they all must receive a multiprocessing.Queue <result> and a String <domain_url> parameter.
#The return value is a tuple (exit_status, output). Also, right before returning, a result.put_nowait((<exit_status>, <output>)) operation must be performed.


def lookupAPI(domain_url):
#def lookupAPI(result, domain_url):
	# Look at SRV record of the given domain if the service _buddycloud-api can be found!
	answers = []
	lookup_api_query = None
	try:
		lookup_api_query = dns.resolver.query("_buddycloud-api._tcp."+domain_url, dns.rdatatype.SRV, raise_on_no_answer=False)
	except dns.resolver.NXDOMAIN:
		out = "Could not find any API servers!"
		status = 1
#		result.put_nowait((status, out))
		return (status, out)

	for answer in lookup_api_query:
		answers.append({
			'domain' : answer.target.to_text()[:-1],
			'port' : answer.port,
			'priority' : answer.priority,
			'weight' : answer.weight
		})

	if len(answers) != 0:
		found = "API server(s) found: "
		for answer in answers:
			print "Answer found:", answer
			found += answer['domain'] + " at " + str(answer['port']+" | ")
		out = found
		status = 0
	else:
		out = "Could not find any API servers!"
		status = 1
#	result.put_nowait((status, out))
	return (status, out)


#def testExample(result, domain_url):
def testExample(domain_url):
	# This is a temporary test example, does nothing but wait.
	waittime = random.randint(0,10)
	time.sleep(waittime)
	out = "Waited "+str(waittime)
	status = 0
#	result.put_nowait((status, out))
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
