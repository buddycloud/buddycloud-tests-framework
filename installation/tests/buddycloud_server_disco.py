import string, sleekxmpp, dns.resolver
from dns.resolver import NXDOMAIN, NoAnswer, Timeout

#util_dependencies
from template_utils import bold, italic, code, breakline, parse,\
render, build_output
from domain_name_lookup import testFunction as domainNameLookup
from dns_utils import getAuthoritativeNameserver

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
    briefing_template += " " + code("{{warning}}")
    message_template = "This test did not even run. " + briefing_template
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def multiple_problems_template():

    briefing_template = "No xmpp server found is "
    briefing_template += italic("buddycloud enabled") + "."
    message_template = briefing_template + breakline()
    message_template += "Several problems with XMPP servers found: "
    message_template += breakline() + breakline()
    message_template += "{{#xmpp_servers}}" + bold("{{name}}:")
    message_template += breakline() + "{{&error}}"
    message_template += breakline() + breakline()
    message_template += "{{/xmpp_servers}}"
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def is_buddycloud_enabled_template():

    briefing_template = bold("{{domain_url}}") + " is " italic("buddycloud " \
    + "enabled") + "."
    message_template = "Congratulations! " + briefing_template + breakline() \
    + "{{#discovery}}Using " + code("Service Discovery") + ", we found your "\
    + "channel server at " + bold("{{channel_server}}") + "!" + breakline()  \
    + "{{#ptr_record}}We also found your channel server " +code("PTR record")\
    + ".{{/ptr_record}}{{/discovery}}{{#ptr_record}}Using " + code("PTR rec" \
    + "ord") + ", we found your channel server at " + bold("{{channel_serve" \
    + "r}}") + "!" + breakline() + "But we could not find it through "       \
    + code("Service Discovery") + ".{{/ptr_record}}"
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

def multiple_problems(view):
    return build_output(view, view["status"], multiple_problems_template, None)

def is_buddycloud_enabled(view):
    return build_output(view, 0, is_buddycloud_enabled_template, None)

def make_output_builder(view, builder):
    final_view = view.copy()
    return lambda: builder(final_view)

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

    situation = {}

    for answer in answers:

        conn_address = answer["domain"], answer["port"]
        view["xmpp_server"] = conn_address[0]

        if ( not xmpp.connect(conn_address, reattempt=False, use_ssl=False, use_tls=False) ):
             situation[conn_address] = make_output_builder(view,
                 xmpp_connection_problem)
             continue

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
                situation[conn_address] = make_output_builder(view,
                    xmpp_disco_query_send_error)
                continue

            if ( len(response.xml.findall("iq[@type='error']")) != 0 ):
                view["error"] = response.xml.findall("iq[@type='error']")[0]
                situation[conn_address] = make_output_builder(view,
                    xmpp_server_error)
                continue

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
                    if ( str(e) != "" ):
                        view["error"] = str(e)
                    situation[conn_address] = make_output_builder(view,
                        xmpp_disco_query_send_error)
                    continue

                if ( len(response.xml.findall("iq[@type='error']")) != 0 ):
                    view["error"] = response.xml.findall("iq[@type='error']")[0]
                    situation[conn_address] = make_output_builder(view,
                        xmpp_server_error)
                    continue

                ids = response.xml.findall(
                    "{%s}query/{%s}identity" % ((DISCO_INFO_NS,)*2))
                for identity in ids:
                    identity_category = identity.attrib['category']
                    identity_type = identity.attrib['type']

                    view["discovery"] = True
                    view["channel_server"] = item_jid
                    if ( identity_category == 'pubsub'
                        and identity_type == 'channels' ):

                        try:
                            resolver = dns.resolver.Resolver()
                            nameserver = getAuthoritativeNameserver(domain_url)
                            resolver.nameservers = [nameserver]
                            resolver.lifetime = 5
                            PTR_name = "_buddycloud-server._tcp." + domain_url
                            answer = resolver.query(PTR_name, dns.rdatatype.PTR)
                        except Exception:
                            pass
                        else:
                            #TODO check if PTR record and DISCO are pointing
                            # to the same place -- they must!
                            view["ptr_record"] = True
                        return is_buddycloud_enabled(view)

            if not conn_address in situation:
                situation[conn_address] = make_output_builder(view,
                    not_buddycloud_enabled)

        finally:
            xmpp.disconnect()

    try:
        resolver = dns.resolver.Resolver()
        nameserver = getAuthoritativeNameserver(domain_url)
        resolver.nameservers = [nameserver]
        resolver.lifetime = 5
        PTR_name = "_buddycloud-server._tcp." + domain_url
        answer = resolver.query(PTR_name, dns.rdatatype.PTR)
    except (NXDOMAIN, NoAnswer, Timeout):
        pass
    except Exception:
        pass
    else:
        view["ptr_record"] = True
        #view["channel_server"] = answer
        return is_buddycloud_enabled(view)

    if ( len(situation) == 1 ):
       return situation[situation.keys()[0]]() 

    view["xmpp_servers"] = []

    status = 2
    for xmpp_server in situation:
        output = situation[xmpp_server]()
        if ( output[0] == 1 ):
            status = 1
        view["xmpp_servers"].append({
            "name" : "%s through port %s" %(xmpp_server),
            "error" : output[2]
        })

    view["status"] = status

    return multiple_problems(view)
