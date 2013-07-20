from requests import Request, Session

#util_dependencies
from ssl_adapter import SSLAdapter

#installation_suite_dependencies
from api_server_lookup import testFunction as apiLookup


def testFunction(domain_url):

	status, briefing, message, answers = apiLookup(domain_url)
	if ( status != 0 ):
		status = 2
		briefing = "This test was skipped because previous test <strong>api_server_lookup</strong> has failed.<br/>"
		new_message = briefing
		new_message += "Reason:<br/>"
		new_message += "<br/>" + message
		return (status, briefing, new_message, None)

	if ( len(answers) == 0 ):

		briefing = "No API server TXT record found!"
		status = 1
		message = "We could not find your API server TXT record!"
		message += "You must setup your DNS to point to the API server endpoint using a TXT record similat to the one below: "
		message += "<br/><br/>_buddycloud-api._tcp.EXAMPLE.COM.          IN TXT \"v=1.0\" \"host=buddycloud.EXAMPLE.COM\" \"protocol=https\" \"path=/api\" \"port=443\""
		return (status, briefing, message, None)
	
	found = ""

	for answer in answers:

		connection_failed = False

		try:

			req = Request('HEAD', answer['protocol'] + "://" + answer['domain'] + answer['path'] + ":" + str(answer['port']))
			r = req.prepare()

			s = Session()

			if ( answer['protocol'] == 'https' ):
				
				s.mount('https://', SSLAdapter('TLSv1'))
			else:

				briefing = "Protocol specified in TXT record for API server at "+answer['domain']+answer['path']+":"+str(answer['port'])+" is not HTTPS!"
				status = 1
				message = briefing + "We have detected that your TXT record specifies a protocol other than HTTPS."
				message += "<br/> Please ensure your API server will run with HTTPS enabled."
				return (status, briefing, message, None)

			if ( (s.send(r, verify=False)).ok ):
		
				if ( found != "" ):
					found += " | "

				found += answer['domain']+answer['path']+":"+answer['port']

			else:

				raise Exception("Could not reach server at "+answer['domain']+answer['path']+":"+str(answer['port'])+".")

		except Exception, e:

			briefing = "Connection failed to API server at "+answer['domain']+answer['path']+":"+str(answer['port']+"!")
			status = 1
			message = "The problem we found was: "+str(e)
			message = "<br/>Please ensure your API server is running (with HTTPS)!"
			message = briefing + message
			return (status, briefing, message, None)

	if len(answers) == 1:
		found = "Connection successful to API server: " + found
	else:
		found = "Connection successful to API servers: " + found

	briefing = found
	status = 0
	message = "We could locate and connect to your API server! Congratulations!"
	message += briefing
	return (status, briefing, message, None)
