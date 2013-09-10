import string, sleekxmpp

#util_dependencies
from domain_name_lookup import testFunction as domainNameLookup


#installation_suite_dependencies
from buddycloud_server_srv_lookup import testFunction as buddycloudChannelSRVLookup
from xmpp_server_srv_lookup import testFunction as xmppServerServiceRecordLookup
from xmpp_server_connection import testFunction as xmppServerConnection

descriptions = {
	'XMPP_CONNECTION_PROBLEM' : "A problem happened while we " +
	"attempted to stablish a XMPP connection!<br/> Beware it is NOT a problem with the server at %s.",
	'QUERY_SEND_PROBLEM' : "A problem happened while our XMPP client attempted to send a query " +
	"to XMPP server at %s!<br/> Beware it may not be a problem with your XMPP server.",
	'SERVER_ERROR' : "Your XMPP server at %s returned an error as response to our query.",
	'BUDDYCLOUD_ENABLED' : "Congratulations! %s is buddycloud enabled!",
	'NOT_BUDDYCLOUD_ENABLED' : "Domain %s is NOT buddycloud enabled."
}

def componentDiscoInfo(to_this, xmpp):

	DISCO_INFO_NS = 'http://jabber.org/protocol/disco#info'

	iq = xmpp.make_iq_get(queryxmlns=DISCO_INFO_NS, 
			      ito=to_this, ifrom=xmpp.boundjid)	

	try:
		response = iq.send(block=True, timeout=5)
	except:
		return "QUERY_SEND_PROBLEM"

	if ( len(response.xml.findall("iq[@type='error']")) != 0 ):
		return "SERVER_ERROR"

	for identity in response.xml.findall("{%s}query/{%s}identity" % ((DISCO_INFO_NS,)*2)):

		identity_category = identity.attrib['category']
		identity_type = identity.attrib['type']

		if ( identity_category == 'pubsub' and identity_type == 'channels' ):
			return "BUDDYCLOUD_ENABLED"

	return "NOT_BUDDYCLOUD_ENABLED"

def xmppServerDiscoItems(to_this, xmpp):

	DISCO_ITEMS_NS = 'http://jabber.org/protocol/disco#items'

	iq = xmpp.make_iq_get(queryxmlns=DISCO_ITEMS_NS, 
			      ito=to_this, ifrom=xmpp.boundjid)

	try:
		response = iq.send(block=True, timeout=5)
	except Exception as e:
		xmpp.disconnect()
		
		if ( str(e) != "" ):
			descriptions['QUERY_SEND_PROBLEM'] += "<br/>Reason: %s..." % str(e)
		return "QUERY_SEND_PROBLEM"

	if ( len(response.xml.findall("iq[@type='error']")) != 0 ):
		return "SERVER_ERROR"

	for item in response.xml.findall("{%s}query/{%s}item" % ((DISCO_ITEMS_NS,)*2)):
	
		situation = componentDiscoInfo(item.attrib['jid'], xmpp)
		if ( situation == "BUDDYCLOUD_ENABLED" ):
			return situation

	return "NOT_BUDDYCLOUD_ENABLED"

def checkBuddycloudCompatibility(domain_url):

	xmpp = sleekxmpp.ClientXMPP("inspect@buddycloud.org", "ei3tseq")

	conn_address = 'crater.buddycloud.org', 5222

	if ( not xmpp.connect(conn_address, reattempt=False, use_ssl=False, use_tls=False) ):
		return "XMPP_CONNECTION_PROBLEM"

	xmpp.process(block=False)

	try:
		return xmppServerDiscoItems(domain_url, xmpp)
	finally:
		xmpp.disconnect()

def testFunction(domain_url):

	(status, briefing, message, output) = domainNameLookup(domain_url)
	if ( status != 0 ):
		return (status, briefing, message, None)

	classified_as = checkBuddycloudCompatibility(domain_url)

	description =  descriptions[classified_as] % ("<strong>"+domain_url+"</strong>")
	briefing = description.split("<br/>")[0]
	message = description

	if ( classified_as == "BUDDYCLOUD_ENABLED" ):
		status = 0
	elif ( classified_as == "SERVER_ERROR"
	    or classified_as == "NOT_BUDDYCLOUD_ENABLED" ):
		status = 1

		(sts, brf, mes, out) = buddycloudChannelSRVLookup(domain_url)
		if ( sts != 0 ):

			message += "<br/>You need to set up a SRV record "
			
			(sts2, brf2, mes2, xmpp_server_names) = xmppServerServiceRecordLookup(domain_url)
			if ( sts2 != 0 ):

				message += "similar to the following:"
				message += "<br/><br/><em>(assuming your XMPP server is called"
				message += " <strong>bc.%s</strong>)</em><br/>" % domain_url
				message += "<strong>_xmpp-server._tcp.channels." + domain_url + "."
				message += "\tSRV\t5\t0\t5269\tbc.%s.</strong>" % domain_url

			else:
				message += "exactly like the following:"
				
				if ( len(xmpp_server_names) > 1 ):
					message += " (only one of them)"

				message += "<br/><br/>"

				for xmpp_server in xmpp_server_names:

					xmpp_server = xmpp_server['domain']
					message += "<strong>_xmpp-server._tcp.channels.%s." %domain_url
					message += "\tSRV\t5\t0\t5269\t%s.<br/><br/></strong>" %xmpp_server

		else:

			message += "<br/>Please ensure your buddycloud channel server is running "
			message += "at <strong>%s</strong> and if that's not the case, run:<br/>" % domain_url
			message += "<br/><strong>sudo /etc/init.d/buddycloud-server"
			message += " start</strong><br/><br/>...to start your buddycloud channel server.<br/>"
			message += "See more information at <a href='https://buddycloud.org/wiki/Install"
			message += "#buddycloud_Channel_Server' target='_blank'>"
			message += "https://buddycloud.org/wiki/Install#buddycloud_Channel_Server</a>."
	else:
		status = 2

		(sts, brf, mes, out) = xmppServerConnection(domain_url)
		if ( sts != 0 ):

			status = 1
			message = briefing + "<br/>"
			message += "Reason: <br/>"
			message += mes
			return (status, briefing, message, None)

	return (status, briefing, message, None)

#if __name__ == "__main__":
#	
#	logging.basicConfig()
#	logging.getLogger('sleekxmpp').setLevel(logging.DEBUG)
#
#	try:
#		import sys
#		domain_url = sys.argv[1]
#	except:
#		domain_url = "buddycloud.org"
#
#	print domain_url
#
#	(status, briefing, message, output) = testFunction(domain_url)
#
#	print "status: %d" % status
#	print "briefing:\n%s" % briefing
#	print "message:\n%s" % message
