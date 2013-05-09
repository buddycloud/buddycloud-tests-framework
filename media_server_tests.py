import dns.resolver
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError
from xmpp_server_tests import xmppServerAddressRecordLookup

def mediaServerDisco(domain_url):

	answers = xmppServerAddressRecordLookup(domain_url, True)

	for answer in answers:
	
		address = answer['address']

		xmpp_client = ClientXMPP("inspect@buddycloud.org", "ei3tseq")
		xmpp_client.register_plugin('xep_0030')
		if ( xmpp_client.connect((address, 5222), reattempt=True, use_ssl=False, use_tls=False) ):
			xmpp_client.process(block=False)

			server_discovered = False
			server_jid = None
			
			try:
				items = xmpp_client['xep_0030'].get_items(jid='buddycloud.org', ifrom='inspect@buddycloud.org', block=True, timeout=40)
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

							print "ic", identity_category, "it", identity_type

							if ( item_jid == "mediaserver.buddycloud.org" and identity_category == 'component' and identity_type == 'generic' ):

								server_discovered = True
								server_jid = item_jid
								break

					except IqError:
						continue
					except:
						out = "Could not query for more information on item with jid "+item_jid+" of XMPP server "+answer['domain']+" at "+address
						status = 1
						return (status, out)

			except:
				out = "Could not query for items of XMPP server "+answer['domain']+" at "+address
				status = 1
				return (status, out)
			finally:
				xmpp_client.disconnect()

			if server_discovered:
				out = "We have found your media server on your XMPP server at "+server_jid
				status = 0
				return (status, out)
			else:
				out = "We could not find your media server on your XMPP server"
				status = 1
				return (status, out)

		else:
			out = "Could not connect with XMPP server "+answer['domain']+" at "+address
			status = 1
			return (status, out)
