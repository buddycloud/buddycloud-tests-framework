from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError

import logging, sys
sys.path.append("suite_utils")

#installation_suite_dependencies
from xmpp_server_a_lookup import testFunction as xmppServerAddressRecordLookup

def discoInfo(items):

	print "THIS FUNCTION ACTUALLY GOT CALLED"

	query_namespace = "{http://jabber.org/protocol/disco#items}"

	for item in items.xml.findall("%squery/%sitem" % (query_namespace, query_namespace)):
						
		if server_discovered:
			break

		item_jid = item.attrib['jid']
				
		try:

			info = xmpp_client['xep_0030'].get_info(jid=item_jid, ifrom='inspect@buddycloud.org', block=False, timeout=None)
			query_namespace = "{http://jabber.org/protocol/disco#info}"
		
			for identity in info.xml.findall("%squery/%sidentity" % (query_namespace, query_namespace)):

				identity_category = identity.attrib['category']
				identity_type = identity.attrib['type']

				if ( identity_category == 'pubsub' and identity_type == 'channels' ):

					server_discovered = True
					server_jid = item_jid
					break

		except IqError:
			continue
		except:
			continue

def testFunction(domain_url):

	status, briefing, message, answers = xmppServerAddressRecordLookup(domain_url)
	if ( status != 0 ):
		status = 2
		briefing = "This test was skipped because previous test <strong>xmpp_server_a_lookup</strong> has failed.<br/>"
		new_message = briefing
		new_message += "Reason:<br/>"
		new_message += "<br/>" + message
		return (status, briefing, new_message, None)

	xmpp_client = None

	for answer in answers:
	
		if xmpp_client != None:
			xmpp_client.disconnect()

		xmpp_client = ClientXMPP("inspect@buddycloud.org", "ei3tseq")
		xmpp_client.register_plugin('xep_0030')
	
		#connecting to (address, int(answer['port'])) below apparently won't work -- must be always 5222
		if ( xmpp_client.connect((answer['address'], 5222), reattempt=False, use_ssl=False, use_tls=False) ):
			xmpp_client.process(block=False)

			server_discovered = False
			server_jid = None
			
			try:
				xmpp_client['xep_0030'].get_items(jid=domain_url, ifrom='inspect@buddycloud.org', local=False, block=False, timeout=None)

			except Exception, e:
				
				briefing = "Could not disco#items on your XMPP server "+answer['domain']+" at "+address+": "+str(e)
				status = 1
				message = "We could not find the identity of your buddycloud channel server while performing a discovery operation on your XMPP server. "
				message += "<br/>Please ensure that disco#items and disco#info are properly working."
				return (status, briefing, message, None)

			finally:
				
				xmpp_client.disconnect()

		else:

			briefing = "Could not connect with XMPP server "+answer['domain']+" at "+address
			status = 1
			message = "We could not open a connection to your XMPP server "+answer['domain']+" at "+address+" using a XMPP client."
			message += "<br/>Please make sure it is up and running the correct port and try again."
			return (status, briefing, message, None)

if __name__ == "__main__":

	logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
	testFunction("buddycloud.org")
	#testFunction("opensheffield.net")
