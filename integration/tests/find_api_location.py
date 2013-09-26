#util_dependencies
from domain_name_lookup import testFunction as domainNameLookup

#installation_suite_dependencies
from api_server_lookup import testFunction as apiLookup
from api_server_connection import testFunction as apiConnection

def findAPILocation(domain_url):

	(status, briefing, message, output) = domainNameLookup(domain_url)
	if ( status != 0 ):
		return (status, briefing, message, None)

	status, briefing, message, data = apiLookup(domain_url)
	if ( status != 0 ):
		status = 2
		briefing = "This test was skipped because previous test <strong>api_server_lookup</strong> has failed.<br/>"
		new_message = briefing
		new_message += "Reason:<br/>"
		new_message += "<br/>" + message
		return (status, briefing, new_message, None)

	status, briefing, message, output = apiConnection(domain_url)
	if ( status != 0 ):
		status = 2
		briefing = "This test was skipped because previous test <strong>api_server_connection</strong> has failed.<br/>"
		new_message = briefing
		new_message = "Reason:<br/>"
		new_message += "<br/>" + message
		return (status, briefing, new_message, None)

	api_location = "%(protocol)s://%(domain)s%(path)s/" % data
	
	status = 0
	briefing = "HTTP API location for buddycloud domain at %s found: %s" % (domain_url, api_location)
	message = briefing
	return (status, briefing, message, api_location)
