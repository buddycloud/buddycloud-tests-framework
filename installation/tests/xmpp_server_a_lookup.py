import dns.resolver, string
from sleekxmpp import ClientXMPP

#installation_suite_depedencies
from xmpp_server_srv_lookup import testFunction as xmppServerServiceRecordLookup


def testFunction(domain_url):

	status, briefing, message, answers = xmppServerServiceRecordLookup(domain_url)
	if ( status != 0 ):
		status = 2
		briefing = "This test was skipped because previous test <strong>xmpp_server_srv_lookup</strong> has failed.<br/>"
		new_message = briefing
		new_message += "Reason:<br/>"
		new_message += "<br/>" + message
		return (status, briefing, new_message, None)


	records = ""

	addresses = []

	for answer in answers:

		# Check if SRV doesn't point to a CNAME record
		try:
			address = str(dns.resolver.query(answer['domain'], dns.rdatatype.CNAME)[0])

			briefing = "XMPP server SRV record is pointing to a CNAME record! Should be to an A record instead."
			briefing += "<br/><strong>" + answer['domain'] + ". IN CNAME " + address + "</strong>"
			status = 1
			message = "We found a CNAME record pointing to your XMPP SRV record. You must not have these in your DNS."
			message += "<br/>Instead, you should have an A record being pointed by your XMPP SRV record."
			message += "<br/>It seems like your buddycloud server is called: <strong>" + answer['domain'] + "</strong>."

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
			message += "<br/><strong>" + answer['domain'] + "\tIN\tA\t" + buddycloud_server_address + "</strong><br/>"
			message += "<br/>Check at <a href='http://buddycloud.org/wiki/Install#buddycloud_DNS' target='_blank'>http://buddycloud.org/wiki/Install#buddycloud_DNS</a>"
			message += " for more information on how to setup the DNS for your domain."
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
			message += "<br/>It seems like your buddycloud server is called: <strong>" + answer['domain'] + "</strong>."

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
			message += "<br/><strong>" + answer['domain'] + "\tIN\tA\t" + buddycloud_server_address + "</strong><br/>"
			message += "<br/>Check at <a href='http://buddycloud.org/wiki/Install#buddycloud_DNS' target='_blank'>http://buddycloud.org/wiki/Install#buddycloud_DNS</a>"
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

		if records == "":
			records += "<strong>"

		for i in range(0, len(addresses)):

			if records != "<strong>":
				records += " | "

			records += addresses[i]['domain'] + " IN A " + addresses[i]['address']


	records += "</strong>"
	briefing = ""
	if len(addresses) == 1:
		briefing = "XMPP server A record found: " + records
	else:
		briefing = "XMPP server A records found: " + records

	status = 0
	message = "You are pointing your XMPP server SRV records to the following valid A records: <br/>"
	message += records
	return (status, briefing, message, addresses)
