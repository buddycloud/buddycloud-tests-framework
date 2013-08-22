import sys
sys.path.append("suite_utils")

import logging, string
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError
from xml.etree.ElementTree import tostring as strxml
from flask import Markup

#installation_suite_dependencies
from xmpp_server_a_lookup import testFunction as xmppServerAddressRecordLookup


disco_items = {}


def checkBuddycloudCompatibility(domain_url, xmpp_server_address):

	global disco_items

	xmpp_client = ClientXMPP("inspect@buddycloud.org", "ei3tseq")
	xmpp_client.register_plugin('xep_0030')

	conn_address = xmpp_server_address, 5222

	conn_established = xmpp_client.connect(conn_address,
			reattempt=False, use_ssl=False, use_tls=False)

	if (not conn_established):
		return { 'type' : 'UNREACHABLE',
			 'description' : "Could not establish connection to " +
		"xmpp server [%s]!"
		}

	xmpp_client.process(block=False)

	disco_items_ns = "http://jabber.org/protocol/disco#items"
	iq = xmpp_client.make_iq_get(queryxmlns=disco_items_ns,
			ito=domain_url, ifrom=xmpp_client.boundjid)

	try:
		xmpp_client.send(iq, timeout=5, now=True)
		response = iq.result
	except:
		return { 'type' : 'PROBLEM1',
			 'description' : "Could not send query " +
		"[disco#items] to xmpp server [%s]!"
		}
	finally:
		xmpp_client.disconnect(wait=False)

	if ( response.xml.attrib['type'] == 'error' ):
		return { 'type' : 'PROBLEM2',
			 'description' : "XMPP server [%s] returned " +
		"error as response to query [disco#items]!"
		}
	else:
		disco_items[xmpp_server_address] = response.xml
		return { 'type' : 'REACHABLE',
			 'description' : "XMPP server [%s] returned " +
			 "something as response to query [disco#items]:"
		}

def testFunction(domain_url):

	status, briefing, message, answers = xmppServerAddressRecordLookup(domain_url)
	if ( status != 0 ):
		status = 2
		briefing = "This test was skipped because previous test"
		briefing += " <strong>xmpp_server_a_lookup</strong> has failed.<br/>"
		new_message = briefing
		new_message += "Reason:<br/>"
		new_message += "<br/>" + message
		return (status, briefing, new_message, None)

	classified = {}
	descriptions = {}

	for answer in answers:

		answer_classified = checkBuddycloudCompatibility(domain_url, answer['address'])

		if ( not answer_classified['type'] in classified ):
			classified[answer_classified['type']] = []
		classified[answer_classified['type']].append(answer['address'])
		descriptions[answer_classified['type']] = answer_classified['description']


	if ( len(classified.get('UNREACHABLE', [])) != 0 or len(classified.get('PROBLEM1', [])) != 0 or len(classified.get('PROBLEM2', [])) != 0 ):

		status = 1
		briefing = "Problems occurred."

		message = "Full description of problems that occurred: <br/><br/>"

		def message_builder(message, situation):
			for address in classified.get(situation, []):
				message += (descriptions[situation] + "<br/>") % address
			return message

		message = message_builder(message, 'UNREACHABLE')
		message = message_builder(message, 'PROBLEM1')
		message = message_builder(message, 'PROBLEM2')

		if ( len(classified.get('REACHABLE', [])) != 0 ):

			message += "<br/>But these had outputs: <br/><br/>"
		
			def message_builder2(message, situation):
				for address in classified.get(situation, []):
					message += (descriptions[situation] + "<br/><strong>%s</strong>") % (address, Markup.escape(strxml(disco_items[address])))
				return message

			message = message_builder2(message, 'REACHABLE')
		
		return (status, briefing, message, None)	

	elif ( len(classified.get('REACHABLE', [])) != 0 ):

		status = 0
		briefing = "All xmpp servers had outputs: <strong>%s</strong>" % string.join(classified['REACHABLE'], " | ")

		message = "All xmpp servers had outputs. See: <br/>"
		def message_builder2(message, situation):
			for address in classified.get(situation, []):
				message += (descriptions[situation] + "<br/><strong>%s</strong>") % (address, Markup.escape(strxml(disco_items[address])))
			return message

		message = message_builder2(message, 'REACHABLE')

		return (status, briefing, message, None)

	return (2, "oddly none were classified, this should never happen, ill fix this", "", None)

if __name__ == "__main__":
	
	logging.basicConfig(level="DEBUG", format='%(levelname)-8s %(message)s')

	try:
		domain_url = sys.argv[1]
	except:
		domain_url = "buddycloud.org"

	(status, briefing, message, output) = testFunction(domain_url)

	print "status: %d" % status
	print "briefing:\n%s" % briefing
	print "message:\n%s" % message

#		xmpp_client = ClientXMPP("inspect@buddycloud.org", "ei3tseq")
#		xmpp_client.register_plugin('xep_0030')

#		if ( xmpp_client.connect((address, 5222), reattempt=False, use_ssl=False, use_tls=False) ):
#			xmpp_client.process(block=False)

#			server_discovered = False
#			server_jid = None

#			try:
#				items = xmpp_client['xep_0030'].get_items(jid=domain_url, ifrom='inspect@buddycloud.org', local=False, block=True, timeout=40)

#				query_namespace = "{http://jabber.org/protocol/disco#items}"	

#				for item in items.xml.findall("%squery/%sitem" % (query_namespace, query_namespace)):

#					if server_discovered:
#						break

#					item_jid = item.attrib['jid']

#					try:

#						info = xmpp_client['xep_0030'].get_info(jid=item_jid, ifrom='inspect@buddycloud.org', block=True, timeout=40)
#						query_namespace = "{http://jabber.org/protocol/disco#info}"

#						for identity in info.xml.findall("%squery/%sidentity" % (query_namespace, query_namespace)):

#							identity_category = identity.attrib['category']
#							identity_type = identity.attrib['type']

#							if ( identity_category == 'pubsub' and identity_type == 'channels' ):

#								server_discovered = True
#								server_jid = item_jid
#								break

#					except IqError:
#						continue
#					except:
#						continue

#			except Exception, e:

#				briefing = "Could not disco#items on your XMPP server "+answer['domain']+" at "+address+": "+str(e)
#				status = 1
#				message = "We could not find the identity of your buddycloud channel server while performing a discovery operation on your XMPP server. "
#				message += "<br/>Please ensure that disco#items and disco#info are properly working."
#				return (status, briefing, message, None)

#			finally:

#				xmpp_client.disconnect()

#			if server_discovered:

#				briefing = "We have found your buddycloud server on your XMPP server at "+server_jid+"!"
#				status = 0
#				message = "We found your buddycloud server on your XMPP server at "+server_jid+"!"
#				message += "<br/>You've properly configured it to advertise its type so that it can be used by other entities."
#				message += "<br/>Congratulations!"
#				return (status, briefing, message, None)
#			else:

#				briefing = "We were unable to discover you buddycloud server."
#				status = 1
#				message = "We could not find the identity of your buddycloud channel server while performing a discovery operation on your XMPP server. "
#				message += "<br/>Please ensure that you have it running with the command '/etc/init.d/buddycloud-server status'."
#				message += "<br/>Also check if disco#items and disco#info are properly working on your XMPP server and make sure your buddycloud server component has a proper identity."
#				message += "<br/>Check https://buddycloud.org/wiki/XMPP_XEP#buddycloud_Server_Discovery for more information."
#				return (status, briefing, message, None)

#		else:

#			briefing = "Could not connect with XMPP server "+answer['domain']+" at "+address
#			status = 1
#			message = "We could not open a connection to your XMPP server "+answer['domain']+" at "+address+" using a XMPP client."
#			message += "<br/>Please make sure it is up and running on port 5222 and try again."
#			return (status, briefing, message, None)
