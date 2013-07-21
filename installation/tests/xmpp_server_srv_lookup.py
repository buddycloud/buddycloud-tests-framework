import dns.resolver, string
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

		status = 1
		briefing = "No XMPP server SRV record found at domain "+domain_url+"!"
		message = "We were unable to find your XMPP server."
		message += "<br/>Assuming the server running buddycloud will be named: <strong><em>buddycloud." + domain_url + "</em></strong>," 
		message += "<br/>here you are a SRV record that should work:<br/>"
		message += "<strong>_xmpp-server._tcp." + domain_url + "\tSRV\t5\t0\t5269\t<em>buddycloud." + domain_url + ".</em></strong><br/>"
		message += "<br/>Check at <a href='http://buddycloud.org/wiki/Install#buddycloud_DNS' target='_blank'>http://buddycloud.org/wiki/Install#buddycloud_DNS</a>"
		message += " for more information on how to setup the DNS for your domain."
		return (status, briefing, message, None)

	except Exception, e:

		status = 2
		briefing = "A problem happened while searching for the XMPP server SRV record: _xmpp-server._tcp." + domain_url + "!"
		message = "Something odd happened while we were searching for the XMPP server SRV record: _xmpp-server._tcp." + domain_url + "!"
		message += "<br/>This is the exception we got: {"+str(e)+"}"
		message += "<br/>It is probably a temporary issue with domain " + domain_url + "."
		message += "<br/>But it could also be a bug in our Inspector. Let us know at <email> if you think so." 
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

	SRV_records = []
	for i in range(len(answers)):
		SRV_records.append("_xmpp-server._tcp." + domain_url + " IN SRV " + answers[i]['port'] + " " + str(answers[i]['domain']))

	status = 0
	briefing = "XMPP server SRV records found: <strong>" + string.join(SRV_records, " | ") + "</strong>"
	message = "You have said that the following addresses will handle all XMPP messages for this domain.<br/>"
	message += "<br/>These were the XMPP server SRV records we found:<br/>"
	message += "<strong><br/>" + string.join(SRV_records, "<br/>") + "<br/></strong>"
	return (status, briefing, message, answers)
