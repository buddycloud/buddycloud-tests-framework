#import sys
#sys.path.append("suite_utils")

import logging, string, sleekxmpp
from xml.etree.ElementTree import tostring as strxml
from flask import Markup

#installation_suite_dependencies
from xmpp_server_a_lookup import testFunction as xmppServerAddressRecordLookup


classified_domains = {}
disco_items_results = {}
status_descriptions = {
	'UNREACHABLE' : "Could not establish connection to XMPP server [%s]!",
	'UNQUERIABLE' : "Could not send query [disco#items] to XMPP server [%s]!",
	'SERVER_ERROR' : "XMPP server [%s] returned an error as response to query [disco#items]: ",
	'BUDDYCLOUD_ENABLED' : "XMPP server [%s] returned something as response to query [disco#items]: "
}

def message_builder(message, situation):

	global classified_domains
	
	for address in classified_domains.get(situation, []):
		message += (status_descriptions[situation] + "<br/>") % address
	return message

def message_builder2(message, situation):

	global classified_domains
	
	for address in classified_domains.get(situation, []):
		message += (status_descriptions[situation] + "<br/><strong>%s</strong>") % (address, Markup.escape(strxml(disco_items_results[address])))
	return message

def classifyXMPPServerAs(xmpp_server_address, status):

	global classified_domains

	if (not status in classified_domains):
		classified_domains[status] = []
	classified_domains[status].append(xmpp_server_address)


def checkBuddycloudCompatibility(domain_url, xmpp_server_address):

	DISCO_ITEM_NS = 'http://jabber.org/protocol/disco#items'

	xmpp = sleekxmpp.ClientXMPP("inspect@buddycloud.org", "ei3tseq")

	conn_address = xmpp_server_address, 5222

	if ( not xmpp.connect(conn_address, reattempt=False, use_ssl=False, use_tls=False) ):
		classifyXMPPServerAs(xmpp_server_address, 'UNREACHABLE')
		return

	xmpp.process(block=False)

	iq = xmpp.make_iq_get(queryxmlns=DISCO_ITEM_NS, 
			      ito=domain_url, ifrom=xmpp.boundjid)

	try:
		response = iq.send(block=True, timeout=5)
	except:
		classifyXMPPServerAs(xmpp_server_address, 'UNQUERIABLE')
	finally:
		xmpp.disconnect()

	if ( len(response.xml.findall("iq[@type='result']")) != 0 ):
		classifyXMPPServerAs(xmpp_server_address, 'SERVER_ERROR')
	else:
		classifyXMPPServerAs(xmpp_server_address, 'BUDDYCLOUD_ENABLED')

	disco_items_results[xmpp_server_address] = response.xml

def testFunction(domain_url):

	status, briefing, message, answers = xmppServerAddressRecordLookup("buddycloud.org")
	if ( status != 0 ):
		status = 2
		briefing = "This test was skipped because previous test"
		briefing += " <strong>xmpp_server_a_lookup</strong> has failed.<br/>"
		new_message = briefing
		new_message += "Reason:<br/>"
		new_message += "<br/>" + message
		return (status, briefing, new_message, None)

	for answer in answers:

		checkBuddycloudCompatibility(domain_url, answer['domain'])


	global classified_domains

	if ( len(classified_domains.get('UNREACHABLE', [])) != 0 or len(classified_domains.get('SERVER_ERROR', [])) != 0 or len(classified_domains.get('UNQUERIABLE', [])) != 0 ):

		status = 1
		briefing = "Problems occurred."

		message = "Full description of problems that occurred: <br/><br/>"
		message = message_builder(message, 'UNREACHABLE')
		message = message_builder(message, 'UNQUERIABLE')
		message = message_builder2(message, 'SERVER_ERROR')

		if ( len(classified_domains.get('BUDDYCLOUD_ENABLED', [])) != 0 ):

			message += "<br/>But these had outputs: <br/><br/>"
			message = message_builder2(message, 'BUDDYCLOUD_ENABLED')
		
		return (status, briefing, message, None)	

	else:
#	elif ( len(classified_domains.get('BUDDYCLOUD_ENABLED', [])) != 0 ):

		status = 0
		briefing = "All xmpp servers had outputs: <strong>%s</strong>" % string.join(classified_domains['BUDDYCLOUD_ENABLED'], " | ")

		message = "All xmpp servers had outputs. See: <br/>"
		message = message_builder2(message, 'BUDDYCLOUD_ENABLED')

		return (status, briefing, message, None)

#if __name__ == "__main__":
#	
#	logging.basicConfig()
#	logging.getLogger('sleekxmpp').setLevel(logging.DEBUG)
#
#	try:
#		domain_url = sys.argv[1]
#	except:
#		domain_url = "buddycloud.org"
#
#	(status, briefing, message, output) = testFunction(domain_url)
#
#	print "status: %d" % status
#	print "briefing:\n%s" % briefing
#	print "message:\n%s" % message
