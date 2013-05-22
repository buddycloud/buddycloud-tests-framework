import socket

from api_server_lookup import apiLookup

def apiHTTPSConnection(domain_url):

	found = "Connection was successful to API server at: "

	status, briefing, message, answers = apiLookup(domain_url)
	if ( status != 0 ):
		return (status, briefing, message, None)

	if ( len(answers) == 0 ):

		briefing = "No API server TXT record found!"
		status = 1
		message = "We could not find your API server TXT record!"
		message += "You must setup your DNS to point to the API server endpoint using a TXT record similat to the one below: "
		message += "<br/><br/>_buddycloud-api._tcp.EXAMPLE.COM.          IN TXT \"v=1.0\" \"host=buddycloud.EXAMPLE.COM\" \"protocol=https\" \"path=/api\" \"port=443\""
		return (status, briefing, message, None)

	for answer in answers:

		try:
			socket.create_connection((answer['domain'],answer['port']), timeout=8)
			found += answer['domain']+":"+answer['port']+" | "

		except socket.timeout:

			briefing = "Timeout exceeded! Connection failed to API server at "+answer['domain']+":"+str(answer['port'])
			status = 1
			message = "<br/>Ensure your API server is running (with HTTPS)"
			message = briefing + message
			return (status, briefing, message, None)

		except socket.gaierror:

			briefing = "Can't locate address. Connection failed to API server at "+answer['domain']+":"+str(answer['port'])
			status = 1
			message = "<br/>Ensure your API server is running (with HTTPS)"
			message = briefing + message
			return (status, briefing, message, None)

	briefing = found
	status = 0
	message = "We could locate and connect to your API server! Congratulations!"
	message += briefing
	return (status, briefing, message, None)
