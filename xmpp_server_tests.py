import dns.resolver
from sleekxmpp import ClientXMPP

def xmppServerServiceRecordLookup(domain_url, redirectTestOutput=False):

	answers = []
	query_for_SRV_record = None
	try:
		query_for_SRV_record = dns.resolver.query("_xmpp-server._tcp."+domain_url, dns.rdatatype.SRV)
	except dns.resolver.NXDOMAIN:
		out = "No XMPP server SRV record found!"
		status = 1
		return (status, out)
	except:
		out = "A problem happened while searching for a XMPP server SRV record!"
		status = 1
		return (status, out)

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
		found = "XMPP server SRV record(s) found: "
		for answer in answers:
			found += answer['domain'] + " at " + str(answer['port'])+" | "
		out = found
		status = 0
		return (status, out)
	else:
		out = "Could not find any XMPP server SRV records!"
		status = 1
	return (status, out)

def xmppServerAddressRecordLookup(domain_url, redirectTestOutput=False):

	answers = xmppServerServiceRecordLookup(domain_url, True)

	if len(answers) != 0:
		found = "XMPP server A record(s) found: "

		if redirectTestOutput:
			addresses = []
		
		for answer in answers:

			# Check if SRV doesn't point to a CNAME record
			try:
				query_for_A_record = dns.resolver.query(answer['domain'], dns.rdatatype.CNAME)
				out = "XMPP server SRV record is pointing to a CNAME record!"
				status = 1
				return (status, out)
			except dns.resolver.NXDOMAIN:
				pass
			except dns.resolver.NoAnswer:
				pass

			# Check if SRV points to a valid A record
			try:
				query_for_A_record = dns.resolver.query(answer['domain'], dns.rdatatype.A)
			except dns.resolver.NXDOMAIN:
				out = "No XMPP server A record found!"
				status = 1
				return (status, out)
			except:
				out = "A problem happened while searching for the XMPP server A record!"
				status = 1
				return (status, ok)
			
			for record in query_for_A_record:
				address = str(record)
			
				if redirectTestOutput:
					addresses.append({'address':address, 'domain' : answer['domain']})
				else:
					found += answer['domain'] + " at " + address + " | "

		if redirectTestOutput:
			return addresses

		out = found
		status = 0
	else:
		out = "Could not find any XMPP server SRV records!"
		status = 1
	return (status, out)

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
				out = "Could not connect with XMPP server "+answer['domain']+" at "+address
				status = 1
				return (status, out)

		found = "Connection succesfull to XMPP server(s): "+found
		out = found
		status = 0
	else:
		out = "Could not find any XMPP server SRV records!"
		status = 1
	return (status, out)
