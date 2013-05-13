import dns.resolver
from sleekxmpp import ClientXMPP

def xmppServerServiceRecordLookup(domain_url, redirectTestOutput=False):

	answers = []
	query_for_SRV_record = None

	try:

		query_for_SRV_record = dns.resolver.query("_xmpp-server._tcp."+domain_url, dns.rdatatype.SRV)

	except dns.resolver.NXDOMAIN:
	
		if redirectTestOutput:
			return []
		
		briefing = "No XMPP server SRV record found at domain "+domain_url+"!"
		status = 1
		message = "We were unable to find your XMPP server. Check at http://buddycloud.org/wiki/Install#DNS on how to setup the DNS for your domain."
		return (status, briefing, message)

	except Exception, e:
	
		if redirectTestOutput:
			return []
		
		briefing = "A problem happened while searching for a XMPP server SRV record!"
		status = 2
		message = "Something odd happened while we were looking a XMPP server SRV record up at your domain at "+domain_url+": "+str(e)+". "
		message += "<br/>It could be a bug in our Inspector. Let us know at <email> if you think so." 
		return (status, briefing, message)

	for answer in query_for_SRV_record:

		domain = answer.target.to_text()[:-1]
		port = str(answer.port)

		answers.append({
			'domain' : domain,
			'port' : port,
			'priority' : answer.priority,
			'weight' : answer.weight
		})

	if redirectTestOutput:
		return answers

	if len(answers) != 0:
		
		found = "XMPP server SRV records found: "
		
		for answer in answers:
			found += answer['domain'] + " at port " + str(answer['port'])+" | "
		
		briefing = found
		status = 0
		message = "You have said that the following addresses will handle all XMPP messages for this domain.<br/>"
		message += briefing
		return (status, briefing, message)

	else:
		
		if redirectTestOutput:
			return []
		
		briefing = "No XMPP server SRV record found at domain "+domain_url+"!"
		status = 1
		message = "We were unable to find your XMPP server. Check at http://buddycloud.org/wiki/Install#DNS on how to setup the DNS for your domain."
		return (status, briefing, message)

def xmppServerAddressRecordLookup(domain_url, redirectTestOutput=False):

	answers = xmppServerServiceRecordLookup(domain_url, True)

	if len(answers) != 0:
		found = "XMPP server A records found: "

		if redirectTestOutput:
			addresses = []
		
		for answer in answers:

			# Check if SRV doesn't point to a CNAME record
			try:
				query_for_A_record = dns.resolver.query(answer['domain'], dns.rdatatype.CNAME)

				if redirectTestOutput:
					return addresses
			
				briefing = "XMPP server SRV record is pointing to a CNAME record!"
				status = 1
				message = "We found that your XMPP server SRV record is pointing to a CNAME record. <br/>The XMPP server SRV record (_xmpp-server._tcp."+domain_url+") must point to a valid A record instead. <br/>Check at http://buddycloud.org/wiki/Install#DNS on how to setup the DNS for your domain."
				return (status, briefing, message)

			except dns.resolver.NXDOMAIN:
				pass
			except dns.resolver.NoAnswer:
				pass

			# Check if SRV points to a valid A record
			try:
			
				query_for_A_record = dns.resolver.query(answer['domain'], dns.rdatatype.A)

			except dns.resolver.NXDOMAIN:
				
				if redirectTestOutput:
					return addresses

				briefing = "No XMPP server A record found!"
				status = 1
				message = "There is no A record being pointed by your XMPP SRV record. <br/>  Check at http://buddycloud.org/wiki/Install#DNS on how to setup the DNS for your domain."
				return (status, briefing, message)

			except Exception, e:
				
				if redirectTestOutput:
					return addresses
				
				briefing = "A problem happened while searching for the XMPP server A record!"
				status = 2
				message = "Something odd happened while we were looking a XMPP server SRV record up at your domain at "+domain_url+": "+str(e)+". "
				message += "<br/>It could be a bug in our Inspector. Let us know at <email> if you think so." 
				return (status, briefing)
			
			for record in query_for_A_record:

				address = str(record)
			
				if redirectTestOutput:
					addresses.append({'address':address, 'domain' : answer['domain']})

				else:
					found += answer['domain'] + " at " + address + " | "

		if redirectTestOutput:
			return addresses


		briefing = found
		status = 0
		message = "You are pointing your XMPP server SRV record to the following valid A records: <br/>"
		message += briefing
		return (status, briefing, message)
	else:

		if redirectTestOutput:
			return []
		
		briefing = "No XMPP server SRV record found at domain "+domain_url+"!"
		status = 1
		message = "We were unable to find your XMPP server. Check at http://buddycloud.org/wiki/Install#DNS on how to setup the DNS for your domain."
		return (status, briefing, message)

def xmppServerConnection(domain_url):

	answers = xmppServerAddressRecordLookup(domain_url, True)

	if len(answers) != 0:

		found = ""
		for answer in answers:

			address = answer['address']

			xmpp_client = ClientXMPP("inspect@buddycloud", "ei3tseq")
			if ( xmpp_client.connect((address, 5222), reattempt=False, use_ssl=False, use_tls=False) ):

				found += answer['domain'] + " at " + address + " | "

			else:

				briefing = "Could not connect with XMPP server "+answer['domain']+" at "+address
				status = 1
				message = "We could not open a connection to your XMPP server "+answer['domain']+" at "+address+" using a XMPP client."
				message += "<br/>Please make sure it is up and running on port 5222 and try again."
				return (status, briefing, message)

		found = "Connection succesfull to XMPP servers: "+found
		briefing = found
		status = 0
		message = "We were able to find your XMPP server! Congratulations. We found the following XMPP servers: "
		message += "<br/>"+found
		return (status, briefing, message)
	else:
		
		briefing = "No XMPP server SRV record found at domain "+domain_url+"!"
		status = 1
		message = "We were unable to find your XMPP server. Check at http://buddycloud.org/wiki/Install#DNS on how to setup the DNS for your domain."
		return (status, briefing, message)
