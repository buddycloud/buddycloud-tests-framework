import dns.resolver
from sleekxmpp import ClientXMPP

from xmpp_server_srv_lookup import xmppServerServiceRecordLookup


def xmppServerAddressRecordLookup(domain_url):

	status, briefing, message, answers = xmppServerServiceRecordLookup(domain_url)
	if ( status != 0 ):
		return (status, briefing, message, None)


	found = "XMPP server A records found: "

	addresses = []

	for answer in answers:

		# Check if SRV doesn't point to a CNAME record
		try:
			query_for_A_record = dns.resolver.query(answer['domain'], dns.rdatatype.CNAME)

			briefing = "XMPP server SRV record is pointing to a CNAME record!"
			status = 1
			message = "We found that your XMPP server SRV record is pointing to a CNAME record."
			message += "<br/>The XMPP server SRV record (_xmpp-server._tcp."+domain_url+") must point to a valid A record instead."
			message += "<br/>Check at http://buddycloud.org/wiki/Install#DNS on how to setup the DNS for your domain."
			return (status, briefing, message, None)

		except dns.resolver.NXDOMAIN:
			pass
		except dns.resolver.NoAnswer:
			pass

		# Check if SRV points to a valid A record
		try:
			
			query_for_A_record = dns.resolver.query(answer['domain'], dns.rdatatype.A)

		except dns.resolver.NXDOMAIN:
				
			briefing = "No XMPP server A record found!"
			status = 1
			message = "There is no A record being pointed by your XMPP SRV record."
			message += "<br/>  Check at http://buddycloud.org/wiki/Install#DNS on how to setup the DNS for your domain."
			return (status, briefing, message, None)

		except Exception, e:
				
			briefing = "A problem happened while searching for the XMPP server A record!"
			status = 2
			message = "Something odd happened while we were looking a XMPP server SRV record up at your domain at "+domain_url+": "+str(e)+". "
			message += "<br/>It could be a bug in our Inspector. Let us know at <email> if you think so." 
			return (status, briefing, message, None)
			
		for record in query_for_A_record:

			address = str(record)
			addresses.append({'address':address, 'domain' : answer['domain']})
			found += answer['domain'] + " at " + address + " | "


	briefing = found
	status = 0
	message = "You are pointing your XMPP server SRV record to the following valid A records: <br/>"
	message += briefing
	return (status, briefing, message, addresses)
