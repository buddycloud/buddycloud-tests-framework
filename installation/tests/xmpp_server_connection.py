from sleekxmpp import ClientXMPP

#installation_suite_dependencies
from xmpp_server_a_lookup import testFunction as xmppServerAddressRecordLookup


def testFunction(domain_url):

	status, briefing, message, answers = xmppServerAddressRecordLookup(domain_url)
	if ( status != 0 ):
		return (status, briefing, message, None)

	found = ""
	for answer in answers:
		
		address = answer['address']

		xmpp_client = ClientXMPP("inspect@buddycloud", "ei3tseq")
		if ( xmpp_client.connect((address, 5222), reattempt=False, use_ssl=False, use_tls=False) ):

			if found != "":
				found += " | "
			found += answer['domain'] + ", ip: " + address
		else:

			briefing = "Could not connect with XMPP server "+answer['domain']+" at "+address
			status = 1
			message = "We could not open a connection to your XMPP server "+answer['domain']+" at "+address+" using a XMPP client."
			message += "<br/>Please make sure it is up and running on port 5222 and try again."
			return (status, briefing, message, None)

	if len(answers) == 1:
		found = "Connection successful to XMPP server: " + found
	else:
		found = "Connection successful to XMPP servers: " + found

	briefing = found
	status = 0
	message = "We were able to find your XMPP server! Congratulations. We found the following XMPP servers: "
	message += "<br/>"+found
	return (status, briefing, message, None)
