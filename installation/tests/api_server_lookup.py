import dns.resolver, string
from dns.resolver import NoAnswer, NXDOMAIN
from sleekxmpp import ClientXMPP

#util_dependencies
from domain_name_lookup import testFunction as domainNameLookup
from dns_utils import getAuthoritativeNameserver


def classifyTXTRecord(TXT_record):

	if ( TXT_record.find("host=") == -1 ):
		return {
			'type' : 'INFO_MISSING',
			'description' : 'HOST information missing.',
			'record' : TXT_record
		}
	elif (  TXT_record.find("port=") == -1 ):
		return {
			'type' : 'INFO_MISSING',
			'description' : 'PORT information missing.',
			'record' : TXT_record
		}
	elif (  TXT_record.find("path=") == -1 ):
		return {
			'type' : 'INFO_MISSING',
			'description' : 'PATH information missing.',
			'record' : TXT_record
		}
	elif (  TXT_record.find("protocol=") == -1 ):
		return {
			'type' : 'INFO_MISSING',
			'description' : 'PROTOCOL information missing.',
			'record' : TXT_record
		}

	domain =  TXT_record[TXT_record.find("host=")+5 :  TXT_record.find("\"",  TXT_record.find("host="))]
	port = TXT_record[TXT_record.find("port=")+5 : TXT_record.find("\"", TXT_record.find("port="))]
	path = TXT_record[TXT_record.find("path=")+5 : TXT_record.find("\"", TXT_record.find("path="))]
	protocol = TXT_record[TXT_record.find("protocol=")+9 : TXT_record.find("\"", TXT_record.find("protocol="))]

	if protocol != "https":
		return {
			'type' : 'NOT_HTTPS',
			'description' : 'PROTOCOL must be HTTPS.',
			'record' : TXT_record
		}

	if ( domain == "" or port == "" or path == "" or protocol == "" ):
		return {
			'type' : 'MALFORMED',
			'description' : 'Malformed TXT record.',
			'record' : TXT_record
		}

	return {
		'type' : 'CORRECT',
		'domain' : domain,
		'port' : port,
		'path' : path,
		'protocol' : protocol,
		'record' : TXT_record
	}

def noTXTRecord(domain_url):

	status = 1
	briefing = "No API server TXT record found at domain <strong>"+domain_url+"</strong>!"
	message = "We were unable to find your API server TXT record."
	message += "<br/>Assuming the server running buddycloud will be named: <strong><em>buddycloud."
	message += domain_url + "</em></strong>," 
	message += "<br/>here you are a TXT record that should work:<br/>"
	message += "<strong>_buddycloud-api._tcp." + domain_url + "\tIN TXT \"host=buddycloud."
	message += domain_url + "\" \"protocol=https\" \"path=/api\" \"port=433\"</strong><br/>"
	message += "<br/>Check at <a href='http://buddycloud.org/wiki/Install#buddycloud_DNS'"
	message += "target='_blank'>http://buddycloud.org/wiki/Install#buddycloud_DNS</a>"
	message += " for more information on how to setup the DNS for your domain."
	return (status, briefing, message, None)

def testFunction(domain_url):

	(status, briefing, message, output) = domainNameLookup(domain_url)
	if ( status != 0 ):
		return (status, briefing, message, None)

	answers = []
	query_for_TXT_record = None

	try:

		resolver = dns.resolver.Resolver()
		resolver.nameservers = [ getAuthoritativeNameserver(domain_url) ]
		resolver.lifetime = 5
		query_for_TXT_record = resolver.query("_buddycloud-api._tcp."+domain_url, dns.rdatatype.TXT)

	except (NXDOMAIN, NoAnswer):

		return noTXTRecord(domain_url)

	except Exception as e:

		if ( str(e) == "" or str(e) == ("%s. does not exist." % domain_url) ):
			return noTXTRecord(domain_url)

		status = 2
		briefing = "A problem happened while searching for the API server TXT record:"
		briefing += " <strong>_buddycloud-api._tcp." + domain_url + "</strong>!"
		message = "Something odd happened while we were searching for the API server TXT record:"
		message += " <strong>_buddycloud-api._tcp." + domain_url + "</strong>!"
		message += "<br/>This is the exception we got: {"+str(e)+"}"
		message += "<br/>It is probably a temporary issue with domain " + domain_url + "."
		message += "<br/>But it could also be a bug in our Inspector."
		message += " Let us know at <email> if you think so." 
		return (status, briefing, message, None)

	classified_records = {}

	for answer in query_for_TXT_record:

		classified = classifyTXTRecord(str(answer))

		if not classified['type'] in classified_records:
			classified_records[classified['type']] = []
		classified_records[classified['type']].append(classified)

	if len(classified_records.get('CORRECT', [])) == 0:

		status = 1
		briefing = "No API server TXT record found at "
		briefing += "domain <strong>%s</strong>!<br/>" % domain_url
		message = briefing

		if ( len(classified_records.get('INFO_MISSING', [])) != 0
		  or len(classified_records.get('MALFORMED', [])) != 0
		  or len(classified_records.get('NOT_HTTPS', [])) != 0 ):

			message += "We detected you set up the following API server"
			message += " TXT records, though.<br/>"
			message += "They have problems: <br/><br/>"

		for record in classified_records.get('INFO_MISSING', []):

			message += ("<strong>%s</strong><br/><em>%s</em><br/><br/>"
					% (record['description'], record['record']))

		for record in classified_records.get('MALFORMED', []):

			message += ("<strong>%s</strong><br/><em>%s</em><br/><br/>"
					% (record['description'], record['record']))

		for record in classified_records.get('NOT_HTTPS', []):

			message += ("<strong>%s</strong><br/><em>%s</em><br/><br/>"
					% (record['description'], record['record']))

		if ( len(classified_records.get('NOT_HTTPS', [])) != 0 ):

			message += "Please ensure your API server will run with HTTPS enabled."

		return (status, briefing, message, None)

	elif len(classified_records.get('CORRECT', [])) > 1:

		status = 2
		briefing = "We found multiple correct API server TXT records!"
		message = briefing + "<br/>"
		message += "But really, you should have just one.<br/>"
		message += "These are the records we found: <br/>"

	else:

		status = 0
		briefing = "API server TXT record found: "
		briefing += "<strong>%s</strong>" % classified_records['CORRECT'][0]['record']
		message = "Congratulations! You have set up your API server "
		message += "TXT record correctly.<br/>"

	for record in classified_records.get('CORRECT', []):

		message += ("<strong>%s://%s:%s%s</strong><br/><em>%s</em><br/><br/>"
				% (record['protocol'],
				   record['domain'],
				   record['port'],
				   record['path'],
				   record['record']))

	r = classified_records['CORRECT'][0]

	return (status, briefing, message, {
			'protocol' : r['protocol'],
			'domain' : r['domain'],
			'port' : r['port'],
			'path' : r['path']
		})
