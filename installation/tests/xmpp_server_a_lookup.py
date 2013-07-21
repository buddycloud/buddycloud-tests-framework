import dns.resolver, string
from sleekxmpp import ClientXMPP

#installation_suite_depedencies
from xmpp_server_srv_lookup import testFunction as xmppServerServiceRecordLookup


def classifyDomainByRecord(domain):

		try:
			addresses = dns.resolver.query(domain, dns.rdatatype.CNAME)
			return { 'type' : 'CNAME',
				 'name' : domain, 
				 'value' : addresses
			}
		
		except dns.resolver.NXDOMAIN:
			pass
		except dns.resolver.NoAnswer:
			pass
		except Exception, e:
			return { 'type' : 'PROBLEM',
				 'name' : 'CNAME record',
				 'value' : str(e)
			}

		try:
			addresses = dns.resolver.query(domain, dns.rdatatype.A)
			return { 'type' : 'A',
				 'name' : domain,
				 'value' : addresses
			}

		except dns.resolver.NXDOMAIN:
			return { 'type' : 'NONEXISTENT',
				 'name' : domain,
				 'value' : []
			}
		except dns.resolver.NoAnswer, e:
			return { 'type' : 'NONEXISTENT',
				 'name' : domain,
				 'value' : []
			}
		except Exception, e:
			return { 'type' : 'PROBLEM',
				 'name' : 'A record',
				 'value' : str(e)
			}

def suggestPossibleARecords(domain_url, domainsPointedBySRV):

	message += "<br/>It seems that your buddycloud server is called: <strong>" + string.join(domainsPointedBySRV, " or ")  + "</strong>.<br/>"

	possible_servers_found = 0

	for possible_server in domainsPointedBySRV:

		message += "<br/>Assuming it is: " + possible_server

		buddycloud_server_address = None
		try:
			buddycloud_server_address = str(dns.resolver.query(possible_server)[0])
			possible_servers_found += 1
		except:
			pass

		message += "<br/>Your A record should be something like this: </br>"
		message += "<br/><strong>" + possible_server + "\tIN\tA\t" + buddycloud_server_address + "</strong><br/>"

	if possible_servers_found == 0:

		try:
			domain_url_address = str(dns.resolver.query(domain_url)[0]).split(".")
			buddycloud_server_address = string.join(domain_url_address[0:2] + ["??","??"], ".")
			buddycloud_server_address += " {maybe " + string.join(domain_url_address, ".") + " or even a completely different address}"
		except:
			buddycloud_server_address = "{the address of your buddycloud server}"

		message += "<br/>Your A record should be something like this: </br>"
		message += "<br/><strong>" + possible_server + "\tIN\tA\t" + buddycloud_server_address + "</strong><br/>"

	return message

def testFunction(domain_url):

	status, briefing, message, answers = xmppServerServiceRecordLookup(domain_url)
	if ( status != 0 ):
		status = 2
		briefing = "This test was skipped because previous test <strong>xmpp_server_srv_lookup</strong> has failed.<br/>"
		new_message = briefing
		new_message += "Reason:<br/>"
		new_message += "<br/>" + message
		return (status, briefing, new_message, None)


	classified = { 'A' : [], 'CNAME' : [] }
	domainsPointedBySRV = {}

	for answer in answers:

		domainsPointedBySRV[answer['domain']] = True

		answer_classified = classifyDomainByRecord(answer['domain'])
		
		if ( answer_classified['type'] == 'NONEXISTENT' ):
			continue

		elif ( answer_classified['type'] == 'PROBLEM' ):

			status = 2
			briefing = "A problem happened while searching for the " + answer_classified['name'] + ": " + answer['domain'] + "!"
			message = "Something odd happened while we were searching for the " + answer_classified['name'] + ": " + answer['domain'] + "!"
			message += "<br/>This is the exception we got: {"+str(e)+"}"
			message += "<br/>It is probably a temporary issue with domain " + domain_url + "."
			message += "<br/>But it could also be a bug in our Inspector. Let us know at <email> if you think so." 
			return (status, briefing, message, None)

		classified[answer_classified['type']].append(answer_classified)

	domainsPointedBySRV = domainsPointedBySRV.keys()

	if ( len(classified['A']) == 0 ):

		status = 1
		briefing = "No XMPP server A record found!"
		message = "There is no A record being pointed by your XMPP SRV record."
		message += suggestPossibleARecords(domain_url, domainsPointedBySRV)
		message += "<br/>Check at <a href='http://buddycloud.org/wiki/Install#buddycloud_DNS' target='_blank'>http://buddycloud.org/wiki/Install#buddycloud_DNS</a>"
		message += " for more information on how to setup the DNS for your domain."
		return (status, briefing, message, None)


	if ( len(classified['CNAME']) != 0 ):

		CNAME_records = []

		for categorized in classified['CNAME']:
			answers = categorized['value']
			for answer in answers:
				CNAME_records.append("buddycloud." + categorized['name'] + " IN CNAME " + str(answer))

		status = 1
		briefing = "There is a XMPP server SRV record pointing to a CNAME record! Should be to an A record instead."
		message = "We found a CNAME record pointing to your XMPP SRV record. You must not have these in your DNS.<br/>"
		message += "<strong><br/>" + string.join(CNAME_records, "<br/>") + "<br/></strong>"		
		message += "<br/>Instead, you should have A records being pointed by your XMPP SRV record."
		message += suggestPossibleARecords(domain_url, domainsPointedBySRV)
		message += "<br/>Check at <a href='http://buddycloud.org/wiki/Install#buddycloud_DNS' target='_blank'>http://buddycloud.org/wiki/Install#buddycloud_DNS</a>"
		message += " for more information on how to setup the DNS for your domain."
		return (status, briefing, message, None)


	if ( len(classified['A']) != 0 ):
		
		addresses = []
		A_records = []
		
		for categorized in classified['A']:
			answers = categorized['value']
			for answer in answers:
				A_records.append(categorized['name'] + " IN A " + str(answer))
				addresses.append({'domain' : categorized['name'], 'address' : str(answer)})

		status = 0
		briefing = "XMPP server A records found: "
		briefing += "<strong>" + string.join(A_records, " | ") + "</strong>"
		message = "You are pointing your XMPP server SRV records to the following valid A records: <br/>"
		message += "<strong><br/>" + string.join(A_records, "<br/>") + "<br/></strong>"
		return (status, briefing, message, addresses)
