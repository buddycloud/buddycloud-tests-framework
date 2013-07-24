import dns.resolver, string
from sleekxmpp import ClientXMPP

#util_dependencies
from domain_name_lookup import testFunction as domainNameLookup
from dns_utils import getAuthoritativeNameserver

def testFunction(domain_url):

	(status, briefing, message, output) = domainNameLookup(domain_url)
	if ( status != 0 ):
		return (status, briefing, message, None)

	answers = []
	query_for_SRV_record = None

	try:

		resolver = dns.resolver.Resolver()
		resolver.nameservers = [ getAuthoritativeNameserver(domain_url) ]
		query_for_SRV_record = resolver.query("_xmpp-server._tcp."+domain_url, dns.rdatatype.SRV)

	except dns.resolver.NXDOMAIN:

		status = 1
		briefing = "No XMPP server SRV record found at domain "+domain_url+"!"
		message = "We were unable to find your XMPP server."
		message += "<br/>Assuming the server running buddycloud will be named: <strong><em>buddycloud."
		message += domain_url + "</em></strong>," 
		message += "<br/>here you are a SRV record that should work:<br/>"
		message += "<strong>_xmpp-server._tcp." + domain_url + "\tSRV\t5\t0\t5269\t<em>buddycloud."
		message += domain_url + ".</em></strong><br/>"
		message += "<br/>Check at <a href='http://buddycloud.org/wiki/Install#buddycloud_DNS'"
		message += "target='_blank'>http://buddycloud.org/wiki/Install#buddycloud_DNS</a>"
		message += " for more information on how to setup the DNS for your domain."
		return (status, briefing, message, None)

	except Exception, e:

		status = 2
		briefing = "A problem happened while searching for the XMPP server SRV record:"
		briefing += " _xmpp-server._tcp." + domain_url + "!"
		message = "Something odd happened while we were searching for the XMPP server SRV record:"
		message += " _xmpp-server._tcp." + domain_url + "!"
		message += "<br/>This is the exception we got: {"+str(e)+"}"
		message += "<br/>It is probably a temporary issue with domain " + domain_url + "."
		message += "<br/>But it could also be a bug in our Inspector."
		message += " Let us know at <email> if you think so." 
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
		SRV_record = "_xmpp-server._tcp." + domain_url + " IN SRV "
		SRV_record += answers[i]['port'] + " " + str(answers[i]['domain'])
		SRV_records.append(SRV_record)

	status = 0
	briefing = "XMPP server SRV records found: <strong>" + string.join(SRV_records, " | ") + "</strong>"
	message = "Congratulations! You have set up your SRV records correctly."
	message += "<br/>These were the XMPP server SRV records we found:<br/>"
	message += "<strong><br/>" + string.join(SRV_records, "<br/>") + "<br/></strong>"
	message += "<br/>Now, we expect that at least of of them is pointing to an A record"
	message += " that will ultimately guide us to your buddycloud server."
	return (status, briefing, message, answers)
