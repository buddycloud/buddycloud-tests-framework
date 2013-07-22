import string
from sleekxmpp import ClientXMPP

#installation_suite_dependencies
from xmpp_server_a_lookup import testFunction as xmppServerAddressRecordLookup


def testFunction(domain_url):

	status, briefing, message, answers = xmppServerAddressRecordLookup(domain_url)
	if ( status != 0 ):
		status = 2
		briefing = "This test was skipped because previous test "
		briefing += "<strong>xmpp_server_a_lookup</strong> has failed.<br/>"
		new_message = briefing
		new_message += "Reason:<br/>"
		new_message += "<br/>" + message
		return (status, briefing, new_message, None)

	reachable = []
	unreachable = []

	for answer in answers:
		
		address = answer['address']

		xmpp_client = ClientXMPP("inspect@buddycloud", "ei3tseq")
		if ( xmpp_client.connect((address, 5222), reattempt=False, use_ssl=False, use_tls=False) ):

			reachable.append({'domain' : answer['domain'], 'address' : address})
		else:

			unreachable.append({'domain' : answer['domain'], 'address' : address})

	if len(reachable) == 0:

		status = 1
		briefing = "Could not connect to all XMPP servers specified: "
		briefing += "<strong>" + string.join(unreachable, " | ") + "</strong>"
		message = "We could not connect to all XMPP servers you told us to look after!<br/>"
		message += "<strong><br/>" + string.join(unreachable, "<br/>") + "<br/></strong>"
		message += "<br/>Please make sure your XMPP server with the buddycloud component"
		message += " is up and running on port 5222 and try again."
		return (status, briefing, message, None)

	else:

		status = 0
		briefing = "Could connect to your XMPP servers: "
		briefing += "<strong>" + string.join(reachable, " | ") + "</strong>"
		message = "We were able to connect to the following XMPP servers.<br/>"
		message += "<strong><br/>" + string.join(reachable, "<br/>") + "<br/></strong>"

		if len(unreachable) != 0:

			message += "<br/>But beware - we could NOT connect to the following XMPP servers"
			message += " you told us to look after:<br/>"
			message += "<strong><br/>" + string.join(unreachable, "<br/>") + "<br/></strong>"
			message += "<br/>Be warned it might result in problems, if any of those "
			message += "are meant to host a buddycloud component."
			message += " <br/>To be safe, be sure these are also up and running"
			message += " on port 5222 and try again."
		else:
			message += "<br/>Congratulations!! All XMPP servers specified are up and running properly."

		return (status, briefing, message, None)
