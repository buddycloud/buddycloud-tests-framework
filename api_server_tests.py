import dns.resolver

def lookupAPI(domain_url):
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
		for answer in answers:
			found += answer['domain'] + " at " + str(answer['port'])+" | "
		out = found
		status = 0
	else:
		out = "Could not find any API server records!"
		status = 1
	return (status, out)
