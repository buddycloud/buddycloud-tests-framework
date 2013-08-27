import sys
sys.path.append("suite_utils")

from requests import Request, Session

#util_dependencies
from ssl_adapter import SSLAdapter

#installation_suite_dependencies
from api_server_lookup import testFunction as apiLookup


def testFunction(domain_url):

	status, briefing, message, api_TXT_record = apiLookup(domain_url)
	if ( status != 0 ):
		status = 2
		briefing = "This test was skipped because previous test "
		briefing += "<strong>api_server_lookup</strong> has failed.<br/>"
		new_message = briefing
		new_message += "Reason:<br/>"
		new_message += "<br/>" + message
		return (status, briefing, new_message, None)

	try:

		req = Request('HEAD', "%(protocol)s://%(domain)s:%(port)s%(path)s" %api_TXT_record)
		r = req.prepare()

		s = Session()
		s.mount('https://', SSLAdapter('TLSv1'))

		if ( (s.send(r, verify=False)).ok ):
		
			status = 0
			briefing = "Connection successful to API server at "
			briefing += "<strong>%(domain)s:%(port)s%(path)s</strong>" %api_TXT_record
			message = briefing
			return (status, briefing, message, None)

		else:

			status = 1
			briefing = "Could not connect to API server at "
			briefing += "<strong>%(domain)s:%(port)s%(path)s</strong>." % api_TXT_record
			message = briefing
			return (status, briefing, message, None)

	except Exception, e:

		status = 2
		briefing = "Something odd happened while trying to connect to API server at "
		briefing += "<strong>%(domain)s:%(port)s%(path)s</strong>!" % api_TXT_record
		message = briefing
		message += "<br/>This is the exception we got: {%s}" % str(e)
		message += "<br/>It is probably a temporary issue with domain " + domain_url + "."
		message += "<br/>But it could also be a bug in our Inspector."
		message += " Let us know at <email> if you think so." 
		return (status, briefing, message, None)
