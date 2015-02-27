import string, sleekxmpp

#util_dependencies
from domain_name_lookup import testFunction as domainNameLookup


descriptions = {
	'XMPP_CONNECTION_PROBLEM' : "A problem happened while we " +
	"attempted to stablish a XMPP connection!<br/> Beware it is NOT a problem with the server at %s.",
	'QUERY_SEND_PROBLEM' : "A problem happened while our XMPP client attempted to send a query " +
	"to XMPP server at %s!<br/> Beware it may not be a problem with your XMPP server.",
	'SERVER_ERROR' : "Your XMPP server at %s returned an error as response to our query.",
	'MEDIASERVER_UP' : "Congratulations! We could locate your Media Server XMPP Component for domain %s!",
	'NOT_MEDIASERVER_UP' : "We could not find your Media Server XMPP Component for domain %s."
}

def componentDiscoInfo(to_this, xmpp):

	DISCO_INFO_NS = 'http://jabber.org/protocol/disco#info'

	iq = xmpp.make_iq_get(queryxmlns=DISCO_INFO_NS, 
			      ito=to_this, ifrom=xmpp.boundjid)	

	try:
		response = iq.send(block=True, timeout=config.IQ_TIMEOUT)
	except:
		return "QUERY_SEND_PROBLEM"

	if ( len(response.xml.findall("iq[@type='error']")) != 0 ):
		return "SERVER_ERROR"

	for identity in response.xml.findall("{%s}query/{%s}identity" % ((DISCO_INFO_NS,)*2)):

		identity_category = identity.attrib['category']
		identity_type = identity.attrib['type']
		identity_name = identity.attrib.get('name', '')

		if ( identity_category == 'component' and identity_type == 'generic' and identity_name == 'Media Server' ):
			return "MEDIASERVER_UP"

	return "NOT_MEDIASERVER_UP"

def xmppServerDiscoItems(to_this, xmpp):

	DISCO_ITEMS_NS = 'http://jabber.org/protocol/disco#items'

	iq = xmpp.make_iq_get(queryxmlns=DISCO_ITEMS_NS, 
			      ito=to_this, ifrom=xmpp.boundjid)

	try:
		response = iq.send(block=True, timeout=config.IQ_TIMEOUT)
	except Exception as e:
		xmpp.disconnect()
		
		if ( str(e) != "" ):
			descriptions['QUERY_SEND_PROBLEM'] += "<br/>Reason: %s..." % str(e)
		return "QUERY_SEND_PROBLEM"

	if ( len(response.xml.findall("iq[@type='error']")) != 0 ):
		return "SERVER_ERROR"

	for item in response.xml.findall("{%s}query/{%s}item" % ((DISCO_ITEMS_NS,)*2)):
	
		situation = componentDiscoInfo(item.attrib['jid'], xmpp)
		if ( situation == "MEDIASERVER_UP" ):
			return situation

	return "NOT_MEDIASERVER_UP"

def checkMediaServerPresence(domain_url):

	xmpp = sleekxmpp.ClientXMPP("inspect@buddycloud.org", "ei3tseq",
            sasl_mech='PLAIN')
        xmpp.register_plugin('xep_0030')
        xmpp['feature_mechanisms'].unencrypted_plain = True

	conn_address = 'crater.buddycloud.org', 5222

	if ( not xmpp.connect(conn_address) ):
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

	classified_as = checkMediaServerPresence(domain_url)

	description =  descriptions[classified_as] % ("<strong>"+domain_url+"</strong>")
	briefing = description.split("<br/>")[0]
	message = description

	if ( classified_as == "MEDIASERVER_UP" ):
		status = 0
	elif ( classified_as == "SERVER_ERROR"
	    or classified_as == "NOT_MEDIASERVER_UP" ):
		status = 1
	else:
		status = 2

	return (status, briefing, message, None)
