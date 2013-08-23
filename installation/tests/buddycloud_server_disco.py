import logging, string, sleekxmpp
from xml.etree.ElementTree import tostring as strxml
from flask import Markup


descriptions = {
	'XMPP_CONNECTION_PROBLEM' : "A problem happened while our " + 
	"Protocol Tester attempted to stablish a XMPP connection!<br/>" +
	"Beware it is NOT a problem with your XMPP server at %s.",
	'QUERY_SEND_PROBLEM' : "A problem happened while our " +
	"XMPP client attempted to send a query to XMPP server at %s!<br/>" +
	"Beware it may not be a problem with your XMPP server at %s.",
	'SERVER_ERROR' : "Your XMPP server at %s returned an error as " +
	" response to our query.",
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

	for identity in response.xml.findall("{%s}query/{%s}identity" % ((DISCO_INFO_NS,)*2)):

		identity_category = identity.attrib['category']
		identity_type = identity.attrib['type']

		print 'cat', identity_category
		print 'type', identity_type

		if ( identity_category == 'pubsub' and identity_type == 'channels' ):
			return "BUDDYCLOUD_ENABLED"

	return "NOT_BUDDYCLOUD_ENABLED"

def xmppServerDiscoItems(to_this, xmpp):

	DISCO_ITEMS_NS = 'http://jabber.org/protocol/disco#items'

	iq = xmpp.make_iq_get(queryxmlns=DISCO_ITEMS_NS, 
			      ito=to_this, ifrom=xmpp.boundjid)

	try:
		response = iq.send(block=True, timeout=5)
	except:
		xmpp.disconnect()
		return "QUERY_SEND_PROBLEM"

	if ( len(response.xml.findall("iq[@type='result']")) != 0 ):
		return "SERVER_ERROR"

	for item in response.xml.findall("{%s}query/{%s}item" % ((DISCO_ITEMS_NS,)*2)):
	
		print 'jid', item.attrib['jid']

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

	classified_as = checkBuddycloudCompatibility(domain_url)

	briefing = descriptions[classified_as] % domain_url
	message = briefing

	if ( classified_as == "BUDDYCLOUD_ENABLED" ):
		status = 0
	elif ( classified_as == "SERVER_ERROR"
	    or classified_as == "NOT_BUDDYCLOUD_ENABLED" ):
		status = 1
	else:
		status = 2

	return (status, briefing, message, None)

if __name__ == "__main__":
	
	logging.basicConfig()
	logging.getLogger('sleekxmpp').setLevel(logging.DEBUG)

	try:
		import sys
		domain_url = sys.argv[1]
	except:
		domain_url = "buddycloud.org"

	print domain_url

	(status, briefing, message, output) = testFunction(domain_url)

	print "status: %d" % status
	print "briefing:\n%s" % briefing
	print "message:\n%s" % message
