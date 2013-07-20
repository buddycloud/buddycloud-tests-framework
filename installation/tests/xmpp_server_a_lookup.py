import dns.resolver, string
from sleekxmpp import ClientXMPP

#installation_suite_depedencies
from xmpp_server_srv_lookup import testFunction as xmppServerServiceRecordLookup


def testFunction(domain_url):

	status, briefing, message, answers = xmppServerServiceRecordLookup(domain_url)
	if ( status != 0 ):
		return (status, briefing, message, None)


	records = "XMPP server A records found: "

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
			message += "<br/>It seems like your buddycloud server is called: " + answer['domain'] + "."

			buddycloud_server_address = None
			try:
				buddycloud_server_address = str(dns.resolver.query(answer['domain'])[0])
			except:
				pass

			if buddycloud_server_address == None:

				try:
					domain_url_address = str(dns.resolver.query(domain_url)[0]).split(".")
					buddycloud_server_address = string.join(domain_url_address[0:2] + ["??","??"], ".")
					buddycloud_server_address += " {maybe " + string.join(domain_url_address, ".") + " or even a completely different address}"
				except:
					buddycloud_server_address = "{the address of your buddycloud server}"

			message += "<br/>Your A record should be something like this: </br>"
			message += "</br><strong>" + answer['domain'] + "\tIN\tA\t" + buddycloud_server_address + "</strong><br/>"
			message += "<br/>Check at <a href='http://buddycloud.org/wiki/Install#DNS' target='_blank'>http://buddycloud.org/wiki/Install#DNS</a>"
			message += " for more information on how to setup the DNS for your domain."
			return (status, briefing, message, None)

		except Exception, e:
				
			briefing = "A problem happened while searching for the XMPP server A record!"
			status = 2
			message = "Something odd happened while we were looking a XMPP server SRV record up at your domain at "+domain_url+": "+str(e)+". "
			message += "<br/>It could be a bug in our Inspector. Let us know at <email> if you think so." 
			return (status, briefing, message, None)
			
		for record in query_for_A_record:

			try:

				address = str(record)
				addresses.append({'address':address, 'domain' : answer['domain']})

			except Exception, e:
				continue

		if len(addresses) == 0:
	
			briefing = "XMPP server A record found at domain "+domain_url+" but it doesn't contain all the relevant information!"
			status = 1
			message = "We were unable to find your XMPP server, even though we could find your XMPP A record."
			message += "<br/>Check at <a href='http://buddycloud.org/wiki/Install#DNS' target='_blank'>http://buddycloud.org/wiki/Install#DNS</a>"
			message += " on how to setup the DNS for your domain."
			return (status, briefing, message, None)

		else:

			records = "<strong>" + addresses[0]['domain'] + ", ip: " + addresses[0]['address']

			for i in range(1, len(addresses)):

				records += " | " + addresses[i]['domain'] + ", ip: " + addresses[i]['address']

			records += "</strong>"

	briefing = ""
	if len(addresses) == 1:
		briefing = "XMPP server A record found: " + records
	else:
		briefing = "XMPP server A records found: " + records

	status = 0
	message = "You are pointing your XMPP server SRV record to the following valid A records: <br/>"
	message += records
	return (status, briefing, message, addresses)

def getTestReference():
	return InstallationTest("xmpp_server_a_lookup", xmppServerAddressRecordLookup)
