from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError

#installation_suite_dependencies
from xmpp_server_a_lookup import testFunction as xmppServerAddressRecordLookup


def testFunction(domain_url):

	status, briefing, message, answers = xmppServerAddressRecordLookup(domain_url)
	if ( status != 0 ):
		return (status, briefing, message, None)

	for answer in answers:
	
		address = answer['address']

		xmpp_client = ClientXMPP("inspect@buddycloud.org", "ei3tseq")
		xmpp_client.register_plugin('xep_0030')
		
		if ( xmpp_client.connect((address, 5222), reattempt=True, use_ssl=False, use_tls=False) ):
			xmpp_client.process(block=False)

			server_discovered = False
			server_jid = None
			
			try:
				items = xmpp_client['xep_0030'].get_items(jid='buddycloud.org', ifrom='inspect@buddycloud.org', local=False, block=True, timeout=40)
			
				query_namespace = "{http://jabber.org/protocol/disco#items}"	

				for item in items.xml.findall("%squery/%sitem" % (query_namespace, query_namespace)):
						
					if server_discovered:
						break

					item_jid = item.attrib['jid']
				
					try:

						info = xmpp_client['xep_0030'].get_info(jid=item_jid, ifrom='inspect@buddycloud.org', block=True, timeout=40)
						query_namespace = "{http://jabber.org/protocol/disco#info}"
							
						for identity in info.xml.findall("%squery/%sidentity" % (query_namespace, query_namespace)):

							identity_category = identity.attrib['category']
							identity_type = identity.attrib['type']

							if ( identity_category == 'Pusher' and identity_type == 'Notification' ):

								server_discovered = True
								server_jid = item_jid
								break

					except IqError:
						continue
					except:
						continue

			except Exception, e:
				briefing = "Could not disco#items on your XMPP server "+answer['domain']+" at "+address+": "+str(e)
				status = 1
				message = "We could not find the identity of your push notification server while performing a discovery operation on your XMPP server. "
				message += "<br/>Please ensure that disco#items and disco#info are properly working."
				return (status, briefing, message, None)
			finally:
				xmpp_client.disconnect()

			if server_discovered:

				briefing = "We have found your push notification server on your XMPP server at "+server_jid+"!"
				status = 0
				message = "We found your push notification server on your XMPP server at "+server_jid+"!"
				message += "<br/>You've properly configured it to advertise its type so that it can be used by other entities."
				message += "<br/>Congratulations!"
				return (status, briefing, message, None)
			else:

				briefing = "We were unable to discover your push notification server."
				status = 1
				message = "We could not find the identity of your push notification server while performing a discovery operation on your XMPP server. "
				message += "<br/>Check if disco#items and disco#info are properly working on your XMPP server and make sure your buddycloud server component has a proper identity."
				message += "<br/>Check https://buddycloud.org/wiki/XMPP_XEP#buddycloud_Server_Discovery for more information."
				return (status, briefing, message, None)

		else:

			briefing = "Could not connect with XMPP server "+answer['domain']+" at "+address
			status = 1
			message = "We could not open a connection to your XMPP server "+answer['domain']+" at "+address+" using a XMPP client."
			message += "<br/>Please make sure it is up and running on port 5222 and try again."
			return (status, briefing, message, None)
