import dns.resolver, string
from dns.resolver import NoAnswer, NXDOMAIN
from sleekxmpp import ClientXMPP

#util_dependencies
from dns_utils import getAuthoritativeNameserver

#installation_suite_depedencies
from xmpp_server_srv_lookup import testFunction as xmppServerServiceRecordLookup
from xmpp_client_srv_lookup import testFunction as xmppClientServiceRecordLookup


def classifyDomainByRecord(domain):

		resolver = dns.resolver.Resolver()
		resolver.lifetime = 5
		try:
#			resolver.nameservers = [ getAuthoritativeNameserver(domain) ]
			addresses = resolver.query(domain, dns.rdatatype.CNAME)
			return { 'type' : 'CNAME',
				 'domain' : domain, 
				 'addresses' : addresses
			}
		
		except dns.resolver.NXDOMAIN:
			pass
		except dns.resolver.NoAnswer:
			pass
		except Exception as e:
			return { 'type' : 'PROBLEM',
				 'name' : 'CNAME record',
				 'value' : str(e)
			}

		try:
			addresses = resolver.query(domain, dns.rdatatype.A)
			return { 'type' : 'A',
				 'domain' : domain,
				 'addresses' : addresses
			}

		except (NXDOMAIN, NoAnswer):
			return { 'type' : 'NONEXISTENT',
				 'domain' : domain,
				 'addresses' : []
			}
		except Exception as e:
			return { 'type' : 'PROBLEM',
				 'name' : 'A record',
				 'value' : str(e)
			}

def suggestPossibleARecords(domain_url, domainsPointedBySRV):

	message = "<br/>It seems that your buddycloud server is called:<br/>"
	message += "<strong>" + string.join(domainsPointedBySRV, "</strong> or <strong>")  + "</strong>.<br/>"

	for possible_server in domainsPointedBySRV:

		message += "<br/>Assuming your buddycloud server is: <strong>" + possible_server + "</strong>"

		buddycloud_server_address = None
		try:
			buddycloud_server_address = str(dns.resolver.query(possible_server)[0])
			message += "<br/>Your A record should be <strong>EXACTLY</strong> this:<br/>"

		except:

			message += "<br/>Your A record should be something like this:<br/>"
			buddycloud_server_address = "{IP address}<br/>"
			buddycloud_server_address += "</strong><em>where</em> <strong>{IP address}</strong>"
			buddycloud_server_address += " <em>is the address of the buddycloud server.</em>"
			try:
				domain_url_address = str(dns.resolver.query(domain_url)[0]).split(".")
				guess = string.join(domain_url_address[0:2] + ["??","??"], ".")
				guess = "<br/><strong>{IP address}</strong><em> could be: " + guess + "</em>"
				buddycloud_server_address += guess + "<strong>"
			except:
				pass
		finally:
			A_record = possible_server + "\tIN\tA\t" + buddycloud_server_address
			message += "<br/><strong>" + A_record  + "</strong><br/>"

	return message

def doSkip(skipped_tests):
	status = 2
	briefing = "This test was skipped because previous test"

	test_names = string.join(skipped_tests.keys(), "</strong> and <strong>")

	if ( len(skipped_tests) > 1 ):
		briefing += "s"

	briefing += " <strong>%s</strong> " % test_names

	if ( len(skipped_tests) > 1 ):
		briefing += "have failed.<br/>"
	else:
		briefing += "has failed.<br/>"

	new_message = briefing
	new_message += "<br/>Reason:<br/><br/>"

	for test in skipped_tests:

		new_message += "<strong>%s</strong> log:<br/>" % test
		new_message += skipped_tests[test] + "<br/><br/>"

	return (status, briefing, new_message, None)

def testFunction(domain_url):

	answers = []
	skipped = {}

	status, briefing, message, server_srvs = xmppServerServiceRecordLookup(domain_url)
	if ( status != 0 ):
		skipped["xmpp_server_srv_lookup"] = message
	else:
		answers += server_srvs

#	status, briefing, message, client_srvs = xmppClientServiceRecordLookup(domain_url)
#	if ( status != 0 ):
#		skipped["xmpp_client_srv_lookup"] = message
#	else:
#		answers += client_srvs

#	if ( len(skipped.keys()) == 2 ):
	if ( len(skipped.keys()) == 1 ):
		return doSkip(skipped)


	classified = { 'A' : [], 'CNAME' : [] }
	domainsPointedBySRV = {}

	for answer in answers:

		domainsPointedBySRV[answer['domain']] = True

		answer_classified = classifyDomainByRecord(answer['domain'])
		
		if ( answer_classified['type'] == 'NONEXISTENT' ):
			continue

		elif ( answer_classified['type'] == 'PROBLEM' ):

			status = 2
			briefing = "A problem happened while searching for the " + answer_classified['name'] + ": "
			briefing += answer['domain'] + "!"
			message = "Something odd happened while we were searching for the "
			message += answer_classified['name'] + ": " + answer['domain'] + "!"
			message += "<br/>This is the exception we got: {"+str(e)+"}"
			message += "<br/>It is probably a temporary issue with domain " + domain_url + "."
			message += "<br/>But it could also be a bug in our Inspector."
			message += " Let us know at <a href='https://github.com/buddycloud/buddycloud-tests-framework/issues'>our issue tracker</a> if you think so." 
			return (status, briefing, message, None)

		answer_classified['port'] = answer['port']

		classified[answer_classified['type']].append(answer_classified)

	domainsPointedBySRV = domainsPointedBySRV.keys()

	if ( len(classified['A']) == 0 ):

		status = 1
		briefing = "No XMPP server A record found!"
		message = "There is no A record being pointed by your XMPP SRV record."
		message += suggestPossibleARecords(domain_url, domainsPointedBySRV)
		message += "<br/>Check at <a href='http://buddycloud.org/wiki/Install#buddycloud_DNS'"
		message += " target='_blank'>http://buddycloud.org/wiki/Install#buddycloud_DNS</a>"
		message += " for more information on how to setup the DNS for your domain."
		return (status, briefing, message, None)


	if ( len(classified['CNAME']) != 0 ):

		CNAME_records = []

		for categorized in classified['CNAME']:
			answers = categorized['addresses']
			for answer in answers:
				CNAME_record = "buddycloud." + categorized['domain'] + " IN CNAME " + str(answer)
				CNAME_records.append(CNAME_record)

		status = 1
		briefing = "There is a XMPP server SRV record pointing to a <strong>CNAME record</strong>!"
		briefing += "<br/>Should be to an <strong>A record</strong> instead."
		message = "We found a CNAME record pointing to your XMPP SRV record."
		message += "<br/>You MUST NOT have these in your DNS.<br/>"
		message += "<strong><br/>" + string.join(CNAME_records, "<br/>") + "<br/></strong>"		
		message += "<br/>Instead, you should have A records being pointed by your XMPP SRV record."
		message += suggestPossibleARecords(domain_url, domainsPointedBySRV)
		message += "<br/>Check at <a href='http://buddycloud.org/wiki/Install#buddycloud_DNS'"
		message += " target='_blank'>http://buddycloud.org/wiki/Install#buddycloud_DNS</a>"
		message += " for more information on how to setup the DNS for your domain."
		return (status, briefing, message, None)


	if ( len(classified['A']) != 0 ):
		
		addresses = []
		A_records = []
		
		for categorized in classified['A']:
			answers = categorized['addresses']
			for answer in answers:

				A_record = categorized['domain'] + " IN A " + str(answer)
				if not A_record in A_records:
					A_records.append(A_record)

				addresses.append({
					'domain' : categorized['domain'],
					'address' : str(answer),
					'port' : categorized['port']
				})

		status = 0
		briefing = "XMPP server A records found: "
		briefing += "<strong>" + string.join(A_records, " | ") + "</strong>"
		message = "Congratulations! You've set up your A records appropriately."
		message += "<br/>You are pointing your XMPP server SRV records to the following valid A records: <br/>"
		message += "<strong><br/>" + string.join(A_records, "<br/>") + "<br/></strong>"
		message += "<br/>Now, we expect that at least one of them is leading us to your buddycloud server."
		return (status, briefing, message, addresses)
