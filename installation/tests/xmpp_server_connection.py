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
		
		xmpp_client = ClientXMPP("inspect@buddycloud", "ei3tseq")
		if ( xmpp_client.connect((answer['address'], int(answer['port'])),
			reattempt=False, use_ssl=False, use_tls=False) ):

			reachable.append("%(domain)s = %(address)s:%(port)s" %answer)
		else:

			unreachable.append("%(domain)s = %(address)s:%(port)s" %answer)

	if len(reachable) == 0:

		status = 1
		briefing = "Could not connect to all XMPP servers specified: "
		briefing += "<strong>" + string.join(unreachable, " | ") + "</strong>"
		message = "We could not connect to all XMPP servers specified!<br/>"
		message += "<strong><br/>" + string.join(unreachable, "<br/>") + "<br/></strong>"
		message += "<br/>Please make sure your XMPP server the buddycloud XMPP component"
		message += " is up and running on the correct port and try again.<br/>"
		message += "If that's not the case, please execute the command: <br/><br/><strong>"
		message += "sudo /etc/init.d/prosody restart</strong><br/><br/>"
		message += "See <a href='https://buddycloud.org/wiki/Install#Prosody_Setup' target='_blank'>"
		message += "https://buddycloud.org/wiki/Install#Prosody_Setup</a> for more information."
		return (status, briefing, message, None)

	else:

		status = 0
		briefing = "Could connect to your XMPP servers: "
		briefing += "<strong>" + string.join(reachable, " | ") + "</strong>"
		message = "We were able to connect to the following XMPP servers.<br/>"
		message += "<strong><br/>" + string.join(reachable, "<br/>") + "<br/></strong>"

		if len(unreachable) != 0:

			message += "<br/>But beware - we could NOT connect to the following XMPP servers:<br/>"
			message += "<strong><br/>" + string.join(unreachable, "<br/>") + "<br/></strong>"
			message += "<br/>Be warned it might result in problems, if any of those "
			message += "are meant to host the buddycloud component."
			message += " <br/>To be safe, be sure these are also up and running"
			message += " on the correct port and try again."
		else:
			message += "<br/>Congratulations!! All XMPP servers specified are up and running properly."
			message += "<br/>Now, we expect that one of them has the buddycloud XMPP component."

		return (status, briefing, message, None)
