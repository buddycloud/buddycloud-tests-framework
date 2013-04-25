import dns.resolver
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError

def buddycloudServerDisco(domain_url):

	answers = []
	query_for_SRV_record = None
	try:
		query_for_SRV_record = dns.resolver.query("_xmpp-server._tcp."+domain_url, dns.rdatatype.SRV)
	except dns.resolver.NXDOMAIN:
		out = "No XMPP server SRV record found!"
		status = 1
		return (status, out)
	except:
		out = "A problem happened while searching for a XMPP server SRV record!"
		status = 1
		return (status, out)

	for answer in query_for_SRV_record:
		domain = answer.target.to_text()[:-1]
		port = str(answer.port)

		answers.append({
			'domain' : domain,
			'port' : port,
			'priority' : answer.priority,
			'weight' : answer.weight
		})

	if len(answers) != 0:
		found = ""
		for answer in answers:

			# Check if SRV doesn't point to a CNAME record
			try:
				query_for_A_record = dns.resolver.query(answer['domain'], dns.rdatatype.CNAME)
				out = "XMPP server SRV record is pointing to a CNAME record!"
				status = 1
				return (status, out)
			except dns.resolver.NXDOMAIN:
				pass
			except dns.resolver.NoAnswer:
				pass

			# Check if SRV points to a valid A record
			try:
				query_for_A_record = dns.resolver.query(answer['domain'], dns.rdatatype.A)
			except dns.resolver.NXDOMAIN:
				out = "No XMPP server A record found!"
				status = 1
				return (status, out)
			except Exception, e:
				out = "A problem happened while searching for the XMPP server A record: "+str(e)
				status = 1
				return (status, ok)

			# Check if there actually is a XMPP server listening on address pointed by A record
			for record in query_for_A_record:
				address = str(record)

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

									if ( identity_category == 'pubsub' and identity_type == 'channels' ):
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
						out = "We have found your buddycloud server on your XMPP server at "+server_jid
						status = 0
						return (status, out)
					else:
						out = "We could not find your buddycloud server on your XMPP server"
						status = 1
						return (status, out)

				else:
					out = "Could not connect with XMPP server "+answer['domain']+" at "+address
					status = 1
					return (status, out)

		found = "Connection succesfull to XMPP server(s): "+found
		out = found
		status = 0
	else:
		out = "Could not find any XMPP server SRV records!"
		status = 1
	return (status, out)
