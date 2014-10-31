import dns
import dns.name
import dns.query
import dns.resolver


def getAuthoritativeNameserver(hostname):
    try:
        answers = dns.resolver.query(hostname, 
                                     dns.rdatatype.SOA)
        if len(answers) == 0:
            return None
        ns = answers[0].mname.to_text()
        answers = dns.resolver.query(ns);
        if len(answers) == 0:
            return None
        return answers[0].to_text()
    except:
        return None
