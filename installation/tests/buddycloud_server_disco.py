import string, sleekxmpp, dns.resolver, config, re

#util_dependencies
from template_utils import bold, italic, code, breakline, parse,\
render, build_output
from domain_name_lookup import testFunction as domainNameLookup
from dns_utils import getAuthoritativeNameserver


def _build_checker(checks):
    def checker(TXT_record):
        veredict = True
        for check in checks:
            veredict = ( veredict and
            check[2](check[0].search(TXT_record)) == check[1] )
        return veredict
    return checker
record_well_formedness_tests = []

def has_version():

    checks = []
    is_none = lambda match: match == None

    find_version = re.compile("(v=[0-9]+(\.{1}[0-9]+){0,1}){1}"), False, is_none
    checks.append(find_version)

    return _build_checker(checks)
record_well_formedness_tests.append((has_version(),
    bold("version") + " attribute missing!"))

def has_server():

    checks = []
    is_none = lambda match: match == None

    find_server = re.compile("(server=[^\"\']+){1}"), False, is_none
    checks.append(find_server)

    return _build_checker(checks)
record_well_formedness_tests.append((has_server(),
    bold("server") + " attribute missing!"))

def has_exactly_two_specs():

    checks = []
    is_none = lambda match: match == None

    find_at_least_two = ( re.compile("^\"( *[^\"\' ]+=[^\"\' ]+ *){2}\"$"),
        False, is_none )
    checks.append(find_at_least_two)
    find_at_most_two = ( re.compile("^\"( *[^\"\' ]+=[^\"\' ]+ *){3}\"$"),
        True, is_none )
    checks.append(find_at_most_two)

    return _build_checker(checks)
record_well_formedness_tests.insert(0, (has_exactly_two_specs(),
"""
A well-formed <code>TXT record</code> has exactly the following 2 attributes specified:
<dl class='dl-horizontal'>
    <dt>v (version)</dt>
    <dd>the version attribute; accepts <code>floating point</code></dd>
    <dt>server</dt>
    <dd>the server attribute; accepts <code>string</code></dd>
</dl>

Each of them being specified according to the following format: (<code>attribute=value</code>)
<br/>
<br/>
There must be only whitespaces in between each attribute definition and one pair of double quotes surrounding all attribute definitions.
<br/>
<br/>
For example:
<br/>
<div class='highlight test_log'><pre><code>"v=1.0 server=server01.verona.lit."</code></pre></div>"""))


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
    message_template += code("TXT record lookup") + ", which is different: "
    message_template += bold("{{channel_server2}}") + "!" + breakline()
    message_template += "The channel server addresses found through "
    message_template += code("Service Discovery") + " and " + code("TXT record lookup") + " must match!"
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def record_error_template():

    briefing_template = "We could find the Buddycloud server " + code("TXT record")
    briefing_template += " for " + bold("{{domain_url}}")
    briefing_template += " but it is problematic!"
    message_template = briefing_template + breakline()
    message_template += breakline() + "This is your record:" + breakline()
    message_template += code_block("{{&record}}")
    message_template += "{{&error}}" + breakline()
    message_template += "Please fix this in your DNS settings." + breakline()
    message_template += "Refer to this " + link("document",
        "http://buddycloud.github.io/buddycloud-xep/#DNS-discovery") + " for more info."
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
    message_template += "{{#txt_record}}We also found your channel server through "
    message_template += code("TXT record lookup") + "." + breakline() + "{{/txt_record}}{{/discovery}}"
    message_template += "{{^discovery}}{{#txt_record}}Using " + code("TXT record lookup")
    message_template += ", we found your channel server at "
    message_template += bold("{{channel_server}}") + "!" + breakline() + "Bu"
    message_template += "t we could not find it through "
    message_template += code("Service Discovery") + ".{{/txt_record}}{{/discovery}}"
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

def record_error(view):
    return build_output(view, 1, record_error_template, None)

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
                            TXT_name = "_bcloud-server._tcp." + domain_url
                            answer = resolver.query(TXT_name, dns.rdatatype.TXT)
                        except Exception:
                            pass
                        else:
                            view["txt_record"] = True
                            txt_answer = answer[0].to_text()

                            for test in record_well_formedness_tests:
                                if ( not test[0](txt_answer) ):
                                    view["error"] = code("TXT record") + " is malformed! " + test[1]
                                    return record_error(view)

                            answer_jid =  txt_answer[txt_answer.find("server=")+7:txt_answer.find(" ", txt_answer.find("server=")+7)]

                            if ( item_jid != answer_jid ):
                                view["channel_server2"] = answer_jid
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
        TXT_name = "_bcloud-server._tcp." + domain_url
        answer = resolver.query(TXT_name, dns.rdatatype.TXT)
    except Exception:
        return disco_situation() 
    else:
        view["txt_record"] = True
        txt_answer = answer[0].to_text()

        for test in record_well_formedness_tests:
            if ( not test[0](txt_answer) ):
                view["error"] = code("TXT record") + " is malformed! " + test[1]
                return record_error(view)

        answer_jid =  txt_answer[txt_answer.find("server=")+7:txt_answer.find(" ", txt_answer.find("server=")+7)]

        view["channel_server"] = answer_jid
        return is_buddycloud_enabled(view)
