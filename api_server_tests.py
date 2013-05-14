import dns.resolver, socket

def apiLookup(domain_url, redirectTestOutput=False):
	
	answers = []
	lookup_api_query = None

	try:
		lookup_api_query = dns.resolver.query("_buddycloud-api._tcp."+domain_url, dns.rdatatype.TXT)

	except dns.resolver.NXDOMAIN:

		if redirectTestOutput:
			return []

		briefing = "No API server TXT record found!"
		status = 1
		message = "We could not find your API server TXT record!"
		message += "You must setup your DNS to point to the API server endpoint using a TXT record similat to the one below: "
		message += "<br/><br/>_buddycloud-api._tcp.EXAMPLE.COM.          IN TXT \"v=1.0\" \"host=buddycloud.EXAMPLE.COM\" \"protocol=https\" \"path=/api\" \"port=443\""
		return (status, briefing, message)

	except Exception, e:

		if redirectTestOutput:
			return []

		briefing = "A problem happened while searching for API server TXT record!"
		status = 2
		message = "Something odd happened while we were looking a API server TXT record up at your domain at "+domain_url+": "+str(e)+". "
		message += "<br/>It could be a bug in our Inspector. Let us know at <email> if you think so."
		return (status, briefing, message)

	for answer in lookup_api_query:

		answer = str(answer)

		problem = None

		if ( answer.find("host=") == -1 ):
			problem = "API server TXT record found but it contains no API server host infomation!"
		elif ( answer.find("port=") == -1 ):
			problem = "API server TXT record found but it contains no API server port information!"
		elif ( answer.find("path=") == -1 ):
			problem = "API server TXT record found but it contains no API server path information!"
		elif ( answer.find("protocol=") == -1 ):
			problem = "API server TXT record found but it contains no API server protocol information!"

		if ( problem != None ):

			if redirectTestOutput:
				return []

			
			briefing = problem
			status = 1
			message = "We could find your API server TXT record! The problem is it is missing some important information."
			message += "<br/>Please check if your API server TXT record has a format similar to this example below:"
			message += "<br/><br/>_buddycloud-api._tcp.EXAMPLE.COM.          IN TXT \"v=1.0\" \"host=buddycloud.EXAMPLE.COM\" \"protocol=https\" \"path=/api\" \"port=443\""
			return (status, briefing, message)

		domain = answer[answer.find("host=")+5 : answer.find("\"", answer.find("host="))]
		port = answer[answer.find("port=")+5 : answer.find("\"", answer.find("port="))]
		path = answer[answer.find("path=")+5 : answer.find("\"", answer.find("path="))]
		protocol = answer[answer.find("protocol=")+9 : answer.find("\"", answer.find("protocol="))]

		answers.append({
			'domain' : domain + path,
			'port' : port,
			'protocol' : protocol
		})

	found = "API server records found: "

	if redirectTestOutput:
		return answers

	for answer in answers:
		found += answer['domain'] + " at " + str(answer['port'])+" | "

	briefing = found
	status = 0
	message = "We could succesfully find your API server TXT record on your domain!"
	message += briefing
	return (status, briefing, message)

def apiHTTPSConnection(domain_url):

	found = "Connection was successful to API server at: "

	answers = apiLookup(domain_url, True)
	
	if ( len(answers) == 0 ):

		briefing = "No API server TXT record found!"
		status = 1
		message = "We could not find your API server TXT record!"
		message += "You must setup your DNS to point to the API server endpoint using a TXT record similat to the one below: "
		message += "<br/><br/>_buddycloud-api._tcp.EXAMPLE.COM.          IN TXT \"v=1.0\" \"host=buddycloud.EXAMPLE.COM\" \"protocol=https\" \"path=/api\" \"port=443\""
		return (status, briefing, message)

	for answer in answers:

		try:
			socket.create_connection((answer['domain'],answer['port']), timeout=8)
			found += answer['domain']+":"+answer['port']+" | "

		except socket.timeout:

			briefing = "Timeout exceeded! Connection failed to API server at "+answer['domain']+":"+str(answer['port'])
			status = 1
			message = "<br/>Ensure your API server is running (with HTTPS)"
			message = briefing + message
			return (status, briefing, message)

		except socket.gaierror:

			briefing = "Can't locate address. Connection failed to API server at "+answer['domain']+":"+str(answer['port'])
			status = 1
			message = "<br/>Ensure your API server is running (with HTTPS)"
			message = briefing + message
			return (status, briefing, message)

	briefing = found
	status = 0
	message = "We could locate and connect to your API server! Congratulations!"
	message += briefing
	return (status, briefing, message)

if __name__ == "__main__":

	domain_url = "buddycloud.org"
	print apiLookup(domain_url)
	print apiHTTPSConnection(domain_url)
