import dns.resolver, sys
from flask import Markup

def testFunction(domain_url):

	try:
		address = str(dns.resolver.query(domain_url)[0])
		status = 0
		briefing = "Could locate domain " + domain_url + " at " + address + "!"
		message = briefing
		return (status, briefing, message, None)

	except dns.resolver.NXDOMAIN:
	
		status = 1
		briefing = "Could not locate " + domain_url + "!"
		message = "We were unable to find your domain " + domain_url + "."
		return (status, briefing, message, None)

	except Exception, e:
	
		status = 2
		briefing = "A problem happened while attempting to locate your domain " + domain_url + "!"
		message = "Something odd happened while we were trying to locate your domain " + domain_url + "!"
		e_type, e_value, e_trace = sys.exc_info()
		e_type = Markup.escape(str(type(e))).__str__()
#		message += "<br/>This is the exception we got: {"+str(e)+"}"
		message += "<br/>This is the exception we got: {type:%s, value:%s}" % (e_type, e_value)
		message += "<br/>It is probably a temporary issue with domain " + domain_url + "."
		message += "<br/>But it could also be a bug in our Inspector. Let us know at <a href='https://github.com/buddycloud/buddycloud-tests-framework/issues'>our issue tracker</a> if you think so." 
		return (status, briefing, message, None)
