import dns.resolver


def testFunction(domain_url):

	try:
		address = str(dns.resolver.query(domain_url)[0])
		status = 0
		briefing = "Could locate domain " + domain_url + " at " + address + "!"
		message = briefing
		return (status, briefing, message, None)

	except dns.resolver.NXDOMAIN:
	
		briefing = "Could not locate " + domain_url + "!"
		status = 1
		message = "We were unable to find your domain " + domain_url + "."
		return (status, briefing, message, None)

	except Exception, e:
	
		briefing = "A problem happened while attempting to locate your domain " + domain_url + "!"
		status = 2
		message = "Something odd happened while we were looking for your domain "+domain_url+": "+str(e)+"."
		message += "<br/>It could be a bug in our Inspector. Let us know at <email> if you think so." 
		return (status, briefing, message, None)

