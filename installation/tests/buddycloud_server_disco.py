import string, sleekxmpp

#util_dependencies
from template_utils import bold, italic, code, breakline, parse,\
render, build_output
from domain_name_lookup import testFunction as domainNameLookup

#installation_suite_dependencies
from xmpp_server_srv_lookup import testFunction as xmppServerServiceRecordLookup

def xmpp_connection_problem_template():

    briefing_template = "Could not establish a XMPP connection"
    briefing_template += " to " + bold("{{xmpp_server}}") + "."
    message_template = briefing_template + breakline()
    message_template += "Beware it is NOT a problem with domain "
    message_template += bold("{{domain_url}}") + " nor the XMPP server"
    message_template += " at " + bold("{{xmpp_server}}") + "."
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def xmpp_disco_query_send_error_template():

    briefing_template = "Could not send " + code("{{disco_type}}") + " query"
    briefing_template += " to " + bold("{{xmpp_server}}") + "."
    message_template = briefing_template + breakline()
    message_template += "Beware it may not be a problem with domain "
    message_template += bold("{{domain_url}}") + " or the XMPP server"
    message_template += " at " + bold("{{xmpp_server}}") + "."
    message_template += breakline() + "{{#error}}Problem: {{error}}{{/error}}"
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def xmpp_server_error_template():

    briefing_template = "The {{disco_type}} query got an error response"
    briefing_template += " from " + bold("{{xmpp_server}}") + "."
    message_template = briefing_template + breakline()
    message_template += "The XMPP server at " + bold("{{xmpp_server}}")
    message_template += " returned the following error: " + code("{{&error}}")
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def not_buddycloud_enabled_template():

    briefing_template = bold("{{domain_url}}")
    briefing_template += " is not " + italic("buddycloud enabled") + "."
    message_template = "Congratulations! " + briefing_template
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def warning_template():

    briefing_template = bold("Precondition problem:")
    briefing_template += " " + code("{{warning}}") + "."
    message_template = "This test did not even run. " + briefing_template
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def is_buddycloud_enabled_template():

    briefing_template = bold("{{domain_url}}")
    briefing_template += " is " + italic("buddycloud enabled") + "."
    message_template = "Congratulations! " + briefing_template
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def xmpp_connection_problem(view):
    return build_output(view, 1, xmpp_connection_problem_template, None)

def xmpp_disco_query_send_error(view):
    return build_output(view, 1, xmpp_disco_query_send_error_template, None)

def xmpp_server_error(view):
    return build_output(view, 1, xmpp_server_error_template, None)

def not_buddycloud_enabled(view):
    return build_output(view, 1, not_buddycloud_enabled_template, None)

def warning(view):
    return build_output(view, 2, warning_template, None)

def is_buddycloud_enabled(view):
    return build_output(view, 0, is_buddycloud_enabled_template, None)

def testFunction(domain_url):

    view = {"domain_url":domain_url}

    if ( domainNameLookup(domain_url)[0] != 0 ):
        view["warning"] = "%s not found!" % (domain_url)
        return warning(view)

    (status, b, m, answers) = xmppServerServiceRecordLookup(domain_url)
    if ( status != 0 ):
        wiew["warning"] = "XMPP Server of domain %s not found!" % (domain_url)
        return warning(view)

    xmpp = sleekxmpp.ClientXMPP("inspect@buddycloud.org", "ei3tseq")
    conn_address = answers[0]["domain"], answers[0]["port"]
    view["xmpp_server"] = conn_address[0]

    if ( not xmpp.connect(conn_address, reattempt=False, use_ssl=False, use_tls=False) ):
        return xmpp_connection_problem(view)

    xmpp.process(block=False)

    try:
	DISCO_ITEMS_NS = 'http://jabber.org/protocol/disco#items'
        iq = xmpp.make_iq_get(queryxmlns=DISCO_ITEMS_NS,
            ito=domain_url, ifrom=xmpp.boundjid)

        try:
            view["disco_type"] = "disco#items"
            response = iq.send(block=True, timeout=5)
        except Exception as e:
            if ( str(e) != "" ):
                view["error"] = str(e)
            return xmpp_disco_query_send_error(view)

        if ( len(response.xml.findall("iq[@type='error']")) != 0 ):
            view["error"] = response.xml.findall("iq[@type='error']")[0]
            return xmpp_server_error(view)

        its = response.xml.findall(
            "{%s}query/{%s}item" % ((DISCO_ITEMS_NS,)*2))
        for item in its:
            item_jid = item.attrib['jid']

            DISCO_INFO_NS = 'http://jabber.org/protocol/disco#info'
            iq = xmpp.make_iq_get(queryxmlns=DISCO_INFO_NS,
                ito=item_jid, ifrom=xmpp.boundjid)

            try:
                view["disco_type"] = "disco#info"
                response = iq.send(block=True, timeout=5)
            except Exception as e:
                return xmpp_disco_query_send_error(view)

            if ( len(response.xml.findall("iq[@type='error']")) != 0 ):
                view["error"] = response.xml.findall("iq[@type='error']")[0]
                return xmpp_server_error(view)

            ids = response.xml.findall(
                "{%s}query/{%s}identity" % ((DISCO_INFO_NS,)*2))
            for identity in ids:
                identity_category = identity.attrib['category']
                identity_type = identity.attrib['type']

                if ( identity_category == 'pubsub'
                    and identity_type == 'channels' ):
                    return is_buddycloud_enabled(view)

        return not_buddycloud_enabled(view)

    finally:
        xmpp.disconnect()
