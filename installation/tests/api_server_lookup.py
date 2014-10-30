import dns.resolver, string, re

#util_dependencies
from template_utils import bold, italic, code, code_block, breakline, link,\
parse, render, build_output
from domain_name_lookup import testFunction as domainNameLookup
from dns_utils import getAuthoritativeNameserver


def warning_template():

    briefing_template = bold("Precondition problem:") + " "
    briefing_template += code("{{warning}}")
    message_template = "This test did not even run. " + briefing_template
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def no_record_template():

    briefing_template = "Could not find the API server " + code("TXT record")
    briefing_template += " for " + bold("{{domain_url}}") + "!"
    message_template = briefing_template + breakline()
    message_template += "Please add one in your DNS settings." + breakline()
    message_template += "Refer to the " + link("install instructions",
        "http://buddycloud.com/install#buddycloud_dns_") + " for more info."
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def record_error_template():

    briefing_template = "We could find the API server " + code("TXT record")
    briefing_template += " for " + bold("{{domain_url}}")
    briefing_template += " but it is problematic!"
    message_template = briefing_template + breakline()
    message_template += breakline() + "This is your record:" + breakline()
    message_template += code_block("{{&record}}")
    message_template += "{{&error}}" + breakline()
    message_template += "Please fix this in your DNS settings." + breakline()
    message_template += "Refer to the " + link("install instructions",
        "http://buddycloud.com/install#buddycloud_dns_") + " for more info."
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def record_correct_template():

    briefing_template = "We could find the API server " + code("TXT record")
    briefing_template += " for " + bold("{{domain_url}}") + "!"
    message_template = "Congratulations! " + briefing_template + breakline()
    message_template += breakline() + "This is your record:" + breakline()
    message_template += code_block("{{&record}}")
    briefing_template = parse(briefing_template)
    message_template = parse(message_template)
    return briefing_template, message_template

def warning(view):
    return build_output(view, 2, warning_template, None)

def no_record(view):
    return build_output(view, 1, no_record_template, None)

def record_error(view):
    return build_output(view, 1, record_error_template, None)

def record_correct(view, output):
    return build_output(view, 0, record_correct_template, output)

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

def has_host():

    checks = []
    is_none = lambda match: match == None

    find_host = re.compile("(host=[^\"\']+){1}"), False, is_none
    checks.append(find_host)

    return _build_checker(checks)
record_well_formedness_tests.append((has_host(),
    bold("host") + " attribute missing!"))

def has_protocol():

    checks = []
    is_none = lambda match: match == None

    find_protocol = re.compile("(protocol=[^\"\']+){1}"), False, is_none
    checks.append(find_protocol)

    return _build_checker(checks)
record_well_formedness_tests.append((has_protocol(),
    bold("protocol") + " attribute missing!"))

def has_path():

    checks = []
    is_none = lambda match: match == None

    find_path = re.compile("(path=[^\"\']*){1}"), False, is_none
    checks.append(find_path)

    return _build_checker(checks)
record_well_formedness_tests.append((has_path(),
    bold("path") + " attribute missing!"))

def has_port():

    checks = []
    is_none = lambda match: match == None

    find_port = re.compile("(port=[0-9]+){1}"), False, is_none
    checks.append(find_port)

    return _build_checker(checks)
record_well_formedness_tests.append((has_port(),
    bold("port") + " attribute missing!"))

def has_exactly_five_specs():

    checks = []
    is_none = lambda match: match == None

    find_at_least_five = ( re.compile("^\"( *[^\"\' ]+=[^\"\' ]+ *){5}\"$"),
        False, is_none )
    checks.append(find_at_least_five)
    find_at_most_five = ( re.compile("^\"( *[^\"\' ]+=[^\"\' ]+ *){6}\"$"),
        True, is_none )
    checks.append(find_at_most_five)

    return _build_checker(checks)
record_well_formedness_tests.insert(0, (has_exactly_five_specs(),
"""
A well-formed <code>TXT record</code> has exactly the following 5 attributes specified:
<dl class='dl-horizontal'>
    <dt>v (version)</dt>
    <dd>the version attribute; accepts <code>floating point</code></dd>
    <dt>host</dt>
    <dd>the host attribute; accepts <code>string</code></dd>
    <dt>protocol</dt>
    <dd>the protocol attribute; accepts <code>string</code></dd>
    <dt>path</dt>
    <dd>the path attribute; accepts <code>string</code></dd>
    <dt>port</dt>
    <dd>the port attribute; accepts <code>integer</code></dd>
</dl>

Each of them being specified according to the following format: (<code>attribute=value</code>)
<br/>
<br/>
There must be only whitespaces in between each attribute definition and one pair of double quotes surrounding all attribute definitions.
<br/>
<br/>
For example:
<br/>
<div class='highlight test_log'><pre><code>"v=1.0 host=demo.buddycloud.org protocol=https path=/api port=443"</code></pre></div>"""))

def testFunction(domain_url):

    view = {"domain_url":domain_url}

    if ( domainNameLookup(domain_url)[0] != 0 ):
        view["warning"] = "%s not found!" % (domain_url)
        return warning(view)

    try:
        resolver = dns.resolver.Resolver()
        nameserver = getAuthoritativeNameserver(domain_url)
        if ( nameserver ):
            resolver.nameservers = [ nameserver ]
        answer = resolver.query("_buddycloud-api._tcp."+domain_url,
            dns.rdatatype.TXT)
    except Exception as e:
        return no_record(view)

    else:

        txt_answer = answer[0].to_text()
        view["record"] = txt_answer

        for test in record_well_formedness_tests:
            if ( not test[0](txt_answer) ):
                view["error"] = code("TXT record") + " is malformed! " + test[1]
                return record_error(view)

        domain =  txt_answer[txt_answer.find("host=")+5:
            txt_answer.find(" ", txt_answer.find("host=")+5)]
        port = txt_answer[txt_answer.find("port=")+5:
            txt_answer.find(" ", txt_answer.find("port=")+5)]
        path = txt_answer[txt_answer.find("path=")+5:
            txt_answer.find(" ", txt_answer.find("path=")+5)]
        protocol = txt_answer[txt_answer.find("protocol=")+9:
            txt_answer.find(" ", txt_answer.find("protocol=")+9)]

        if ( protocol.lower() != "https" ):
            view["error"] = code("TXT record") + "\'s " + bold("protocol") + "\
                attribute must have value set to " + code("https") + "!"
            return record_error(view)

        output = {
            'protocol' : protocol,
            'domain' : domain,
            'port' : port,
            'path' : path
        }
        return record_correct(view, output)
