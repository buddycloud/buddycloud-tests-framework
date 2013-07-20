import dns.resolver

#util_dependencies
from domain_name_lookup import testFunction as domainNameLookup


def testFunction(domain_url):

	(status, briefing, message, output) = domainNameLookup(domain_url)
	if ( status != 0 ):
		return (status, briefing, message, None)

	answers = []
	lookup_api_query = None

	try:
		lookup_api_query = dns.resolver.query("_buddycloud-api._tcp."+domain_url, dns.rdatatype.TXT)

	except dns.resolver.NXDOMAIN:

		briefing = "No API server TXT record found at domain " + domain_url + "!"
		status = 1
		message = "We could not find your API server TXT record!"
		message += "<br/>You must setup your DNS to point to the API server endpoint using a TXT record similat to the one below: "
		message += "<br/><br/>_buddycloud-api._tcp.EXAMPLE.COM.          IN TXT \"v=1.0\" \"host=buddycloud.EXAMPLE.COM\" \"protocol=https\" \"path=/api\" \"port=443\""
		return (status, briefing, message, None)

	except Exception, e:

		briefing = "A problem happened while searching for API server TXT record!"
		status = 2
		message = "Something odd happened while we were looking a API server TXT record up at your domain at "+domain_url+": "+str(e)+". "
		message += "<br/>It could be a bug in our Inspector. Let us know at <email> if you think so."
		return (status, briefing, message, None)

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

			briefing = problem
			status = 1
			message = "We could find your API server TXT record! The problem is it is missing some important information."
			message += "<br/>Please check if your API server TXT record has a format similar to this example below:"
			message += "<br/><br/>_buddycloud-api._tcp.EXAMPLE.COM.          IN TXT \"v=1.0\" \"host=buddycloud.EXAMPLE.COM\" \"protocol=https\" \"path=/api\" \"port=443\""
			return (status, briefing, message, None)

		domain = answer[answer.find("host=")+5 : answer.find("\"", answer.find("host="))]
		port = answer[answer.find("port=")+5 : answer.find("\"", answer.find("port="))]
		path = answer[answer.find("path=")+5 : answer.find("\"", answer.find("path="))]
		protocol = answer[answer.find("protocol=")+9 : answer.find("\"", answer.find("protocol="))]

		answers.append({
			'domain' : domain,
			'port' : port,
			'protocol' : protocol,
			'path' : path
		})


	found = answers[0]['domain'] + answers[0]['path'] + ", port: " + str(answers[0]['port'])

	for i in range(1, len(answers)):
		found = answers[i]['domain'] + answers[i]['path'] + ", port: " + str(answers[i]['port'])

	if len(answers) == 1:
		found = "API server record found: " + found
	else:
		found = "API server records found: " + found

	briefing = found
	status = 0
	message = "We could succesfully find your API server TXT record on your domain!"
	message += briefing
	return (status, briefing, message, answers)
