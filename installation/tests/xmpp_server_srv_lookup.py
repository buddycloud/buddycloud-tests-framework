import dns.resolver
from sleekxmpp import ClientXMPP

#util_dependencies
from domain_name_lookup import testFunction as domainNameLookup


def testFunction(domain_url):

	(status, briefing, message, output) = domainNameLookup(domain_url)
	if ( status != 0 ):
		return (status, briefing, message, None)

	answers = []
	query_for_SRV_record = None

	try:

		query_for_SRV_record = dns.resolver.query("_xmpp-server._tcp."+domain_url, dns.rdatatype.SRV)

	except dns.resolver.NXDOMAIN:
	
		briefing = "No XMPP server SRV record found at domain "+domain_url+"!"
		status = 1
		message = "We were unable to find your XMPP server."
		message += "<br/>Assuming the server running buddycloud will be named: buddycloud." + domain_url + "," 
		message += "<br/>here you are an SRV record that should work:<br/>"
		message += "<strong>_xmpp-server._tcp." + domain_url + "\tSRV\t5\t0\t5269\tbuddycloud." + domain_url + ".</strong><br/>"
		message += "<br/>Check at <a href='http://buddycloud.org/wiki/Install#DNS' target='_blank'>http://buddycloud.org/wiki/Install#DNS</a>"
		message += "for more information on how to setup the DNS for your domain."
		return (status, briefing, message, None)

	except Exception, e:
	
		briefing = "A problem happened while searching for a XMPP server SRV record!"
		status = 2
		message = "Something odd happened while we were looking a XMPP server SRV record up at your domain at "+domain_url+": "+str(e)+". "
		message += "<br/>It could be a bug in our Inspector. Let us know at <email> if you think so." 
		return (status, briefing, message, None)

	for answer in query_for_SRV_record:

		try:

			domain = answer.target.to_text()[:-1]
			port = str(answer.port)

			answers.append({
				'domain' : domain,
				'port' : port,
				'priority' : answer.priority,
				'weight' : answer.weight
			})

		except Exception, e:
			continue

	if len(answers) == 0:
		
		briefing = "XMPP server SRV record found at domain "+domain_url+" but it doesn't contain all the relevant information!"
		status = 1
		message = "We were unable to find your XMPP server, even though we could find your XMPP SRV record."
		message += "<br/>Check at <a href='http://buddycloud.org/wiki/Install#DNS' target='_blank'>http://buddycloud.org/wiki/Install#DNS</a>"
		message += " on how to setup the DNS for your domain."
		return (status, briefing, message, None)

	else:

		records = "<strong>" + answers[0]['domain'] + ", port: " + str(answers[0]['port'])

		for i in range(1, len(answers)):
			records += " | " + answers[i]['domain'] + ", port: " + str(answers[i]['port'])

		records += "</strong>"

		if len(answers) == 1:
			found = "XMPP server SRV record found: " + records
		else:
			found = "XMPP server SRV records found: " + records

		briefing = found
		status = 0
		message = "You have said that the following addresses will handle all XMPP messages for this domain.<br/>"
		message += records
		return (status, briefing, message, answers)

