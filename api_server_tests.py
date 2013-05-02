import dns.resolver, socket

def apiLookup(domain_url, redirectTestOutput=False):
	# Look at SRV record of the given domain if the service _buddycloud-api can be found!
	answers = []
	lookup_api_query = None
	try:
		lookup_api_query = dns.resolver.query("_buddycloud-api._tcp."+domain_url, dns.rdatatype.SRV)
	except dns.resolver.NXDOMAIN:
		out = "No API server record found!"
		status = 1
		return (status, out)
	except:
		out = "A problem happened while searching for API server record!"
		status = 1
		return (status, out)

	for answer in lookup_api_query:
		domain = answer.target.to_text()[:-1]
		port = str(answer.port)

		answers.append({
			'domain' : domain,
			'port' : port,
			'priority' : answer.priority,
			'weight' : answer.weight
		})

	if len(answers) != 0:
		found = "API server record(s) found: "

		if ( redirectTestOutput ):
			return answers

		for answer in answers:
			found += answer['domain'] + " at " + str(answer['port'])+" | "

		out = found
		status = 0
	else:
		out = "Could not find any API server records!"
		status = 1
	return (status, out)

def apiConnection(domain_url):

	found = "API server connection was successful at: "

	answers = apiLookup(domain_url, True)
	for answer in answers:

		try:
			socket.create_connection((answer['domain'],answer['port']), timeout=5)
			found += answer['domain']+":"+answer['port']+" | "
		except socket.timeout:
			out = "API server connection failed at "+answer['domain']+":"+str(answer['port'])
			status = 1
			return (status, out)

	out = found
	status = 0
	return (status, out)
