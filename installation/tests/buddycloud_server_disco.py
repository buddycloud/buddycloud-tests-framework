import string, sleekxmpp, dns.resolver

#util_dependencies
from template_utils import bold, italic, code, breakline, parse,\
render, build_output
from domain_name_lookup import testFunction as domainNameLookup
from dns_utils import getAuthoritativeNameserver

import config

def xmpp_connection_problem_template():

    briefing_template = "Could not establish a client XMPP connection."
    message_template = briefing_template + breakline() + "Beware it is NOT a"
    message_template += " problem with domain " + bold("{{domain_url}}")+ "."
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def xmpp_disco_query_send_error_template():

    briefing_template = "Could not send "+code("{{disco_type}}")+" query to "
    briefing_template += "{{^xmpp_server}}" + bold("{{domain_url}}")
    briefing_template += "{{/xmpp_server}}"
    briefing_template += "{{#xmpp_server}}" + bold("{{xmpp_server}}")
    briefing_template += "{{/xmpp_server}}."
    message_template = briefing_template
    message_template += "{{#error}}" + breakline()
    message_template += "Error response: " + code("{{&error}}") +"{{/error}}"
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def xmpp_server_error_template():

    briefing_template = "The {{disco_type}} query got an error response from"
    briefing_template += "{{^xmpp_server}}" + bold("{{domain_url}}")
    briefing_template += "{{/xmpp_server}}"
    briefing_template += "{{#xmpp_server}}" + bold("{{xmpp_server}}")
    briefing_template += "{{/xmpp_server}}."
    message_template = briefing_template
    message_template += "{{#error}}" + breakline()
    message_template += "Error response: " + code("{{&error}}") +"{{/error}}"
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def not_buddycloud_enabled_template():

    briefing_template = bold("{{domain_url}}") + " is not "
    briefing_template += italic("buddycloud enabled") + "."
    message_template = "Congratulations! " + briefing_template
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def warning_template():

    briefing_template = bold("Precondition problem:") + " "
    briefing_template += code("{{warning}}")
    message_template = "This test did not even run. " + briefing_template
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def buddycloud_enabled_conflict_template():

    briefing_template = bold("{{domain_url}}") + " is "
    briefing_template += italic("buddycloud enabled") + ","
    briefing_template += " but we detected a conflict problem."
    message_template = briefing_template + breakline()
    message_template += "Using " + code("Service Discovery")
    message_template += ", we found your channel server at "
    message_template += bold("{{channel_server}}") + "!" + breakline()
    message_template += "But we also found a channel server through "
    message_template += code("PTR record lookup") + ", which is different: "
    message_template += bold("{{channel_server2}}") + "!" + breakline()
    message_template += "The channel server addresses found through "
    message_template += code("Service Discovery") + " and " + code("PTR record lookup") + " must match!"
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def is_buddycloud_enabled_template():

    briefing_template = bold("{{domain_url}}") + " is "
    briefing_template += italic("buddycloud enabled") + "."
    message_template = "Congratulations! " + briefing_template + breakline()
    message_template += "{{#discovery}}Using " + code("Service Discovery")
    message_template += ", we found your channel server at "
    message_template += bold("{{channel_server}}") + "!" + breakline()
    message_template += "{{#ptr_record}}We also found your channel server through "
    message_template += code("PTR record lookup") + ".{{/ptr_record}}{{/discovery}}"
    message_template += "{{#ptr_record}}Using " + code("PTR record lookup")
    message_template += ", we found your channel server at "
    message_template += bold("{{channel_server}}") + "!" + breakline() + "Bu"
    message_template += "t we could not find it through "
    message_template += code("Service Discovery") + ".{{/ptr_record}}"
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def xmpp_connection_problem(view):
    return build_output(view, 2, xmpp_connection_problem_template, None)

def xmpp_disco_query_send_error(view):
    return build_output(view, 1, xmpp_disco_query_send_error_template, None)

def xmpp_server_error(view):
    return build_output(view, 1, xmpp_server_error_template, None)

def not_buddycloud_enabled(view):
    return build_output(view, 1, not_buddycloud_enabled_template, None)

def warning(view):
    return build_output(view, 2, warning_template, None)

def buddycloud_enabled_with_conflict(view):
    return build_output(view, 1, buddycloud_enabled_conflict_template, None)

def is_buddycloud_enabled(view):
    return build_output(view, 0, is_buddycloud_enabled_template, None)

def make_output_builder(view, builder):
    final_view = view.copy()
    return lambda: builder(final_view)

def create_xmpp_client():
    client = sleekxmpp.ClientXMPP("inspect@buddycloud.org", "ei3tseq",
        sasl_mech='PLAIN')
    client.register_plugin('xep_0030')
    client['feature_mechanisms'].unencrypted_plain = True
    return client

def testFunction(domain_url):

    view = {"domain_url":domain_url}

    if ( domainNameLookup(domain_url)[0] != 0 ):
        view["warning"] = "%s not found!" % (domain_url)
        return warning(view)

    xmpp = create_xmpp_client()
    conn_address = 'crater.buddycloud.org', 5222

    disco_situation = None

    if ( not xmpp.connect(conn_address) ):
        disco_situation = make_output_builder(view, xmpp_connection_problem)

    else:
        xmpp.process(block=False)

        try:
            DISCO_ITEMS_NS = 'http://jabber.org/protocol/disco#items'
            iq = xmpp.make_iq_get(queryxmlns=DISCO_ITEMS_NS,
                ito=domain_url, ifrom=xmpp.boundjid)

            class DiscoItemsFailedException(Exception):
                pass

            try:
                view["disco_type"] = "disco#items"
                response = iq.send(block=True, timeout=config.IQ_TIMEOUT)
            except Exception as e:
                if ( str(e) != "" ):
                    view["error"] = str(e)
                disco_situation = make_output_builder(view,
                    xmpp_disco_query_send_error)
                raise DiscoItemsFailedException()

            if ( len(response.xml.findall("iq[@type='error']")) != 0 ):
                view["error"] = response.xml.findall("iq[@type='error']")[0]
                disco_situation = make_output_builder(view,
                    xmpp_server_error)
                raise DiscoItemsFailedException()

            its = response.xml.findall(
                "{%s}query/{%s}item" % ((DISCO_ITEMS_NS,)*2))
            for item in its:
                item_jid = item.attrib['jid']

                DISCO_INFO_NS = 'http://jabber.org/protocol/disco#info'
                iq = xmpp.make_iq_get(queryxmlns=DISCO_INFO_NS,
                    ito=item_jid, ifrom=xmpp.boundjid)

                try:
                    view["disco_type"] = "disco#info"
                    view["xmpp_server"] = item_jid
                    response = iq.send(block=True, timeout=config.IQ_TIMEOUT)
                except Exception as e:
                    if ( str(e) != "" ):
                        view["error"] = str(e)
                    disco_situation = make_output_builder(view,
                        xmpp_disco_query_send_error)
                    continue

                if ( len(response.xml.findall("iq[@type='error']")) != 0 ):
                    view["error"] = response.xml.findall("iq[@type='error']")[0]
                    disco_situation = make_output_builder(view,
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
#                            nameserver = getAuthoritativeNameserver(domain_url)
#                            resolver.nameservers = [nameserver]
#                            resolver.lifetime = config.DNS_TIMEOUT
                            PTR_name = "_buddycloud-server._tcp." + domain_url
                            answer = resolver.query(PTR_name, dns.rdatatype.PTR)
                        except Exception:
                            pass
                        else:
                            view["ptr_record"] = True
                            ptr_answer = answer[0].target.to_text()[:-1]
                            if ( item_jid != ptr_answer ):
                                view["channel_server2"] = ptr_answer
                                return buddycloud_enabled_with_conflict(view)

                        return is_buddycloud_enabled(view)

            if disco_situation == None:
                disco_situation = make_output_builder(view,
                    not_buddycloud_enabled)

        except DiscoItemsFailedException:
            pass
        finally:
            xmpp.disconnect()

    try:
        resolver = dns.resolver.Resolver()
#        nameserver = getAuthoritativeNameserver(domain_url)
#        resolver.nameservers = [nameserver]
#        resolver.lifetime = config.DNS_TIMEOUT
        PTR_name = "_buddycloud-server._tcp." + domain_url
        answer = resolver.query(PTR_name, dns.rdatatype.PTR)
    except Exception:
        return disco_situation() 
    else:
        view["ptr_record"] = True
        ptr_answer = answer[0].target.to_text()[:-1]
        view["channel_server"] = ptr_answer
        return is_buddycloud_enabled(view)
