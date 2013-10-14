import string
from api_utils import user_channel_exists, create_user_channel, delete_user_channel
from find_api_location import findAPILocation


def testFunction(domain_url):

	CLASSIFIED = { 'CREATED' : [], 'UNEXPECTED' : [], 'UNEXPECTED_BUT_WORKED' : [], 'NOT_CREATED' : [] }

	(status, briefing, message, api_location) = findAPILocation(domain_url)
	if status != 0:
		return (status, briefing, message, None)

	prefix = "test_user_channel_follower"

	for i in range(1, 5):

		username = prefix + str(i)

		if create_user_channel(domain_url, api_location, username):
			CLASSIFIED['CREATED'].append("%s@%s" % (username, domain_url))
		else:
			if user_channel_exists(domain_url, api_location, username):

				if ( delete_user_channel(domain_url, api_location, username)
				and create_user_channel(domain_url, api_location, username) ):
					CLASSIFIED['UNEXPECTED_BUT_WORKED'].append("%s@%s" % (username, domain_url))
				else:
					CLASSIFIED['UNEXPECTED'].append("%s@%s" % (username, domain_url))
			else:
				CLASSIFIED['NOT_CREATED'].append("%s@%s" % (username, domain_url))

	status = 0
	briefing = ""
	message = ""

	if ( len(CLASSIFIED.get('NOT_CREATED', [])) > 0 ):
	
		status = 1
		briefing = "The following test user channels could not be created:"
		message = briefing
		briefing += " <strong>%s</strong>" % string.join(CLASSIFIED['NOT_CREATED'], " | ")
		message += "<br/><br/><strong>%s</strong>" % string.join(CLASSIFIED['NOT_CREATED'], "<br/>")
		message += "<br/>It seems like your HTTP API server is problematic. It had trouble creating "
		message += "user channels - these operations must work."
	
	if ( len(CLASSIFIED.get('UNEXPECTED', [])) > 0 ):

		if status == 0:
			status = 2

		info = "The following test user channels weren't expected to exist but they did, so they could not be created again: "

		if not briefing:
			briefing = info
			briefing += "<strong>%s</strong>" % string.join(CLASSIFIED['UNEXPECTED'], " | ")
			message = info
		else:
			message += "<br/>" + info

		message += "<br/><br/><strong>%s</strong>" % string.join(CLASSIFIED['UNEXPECTED'], "<br/>")
		message += "<br/>The problem is we cannot assert that user channel creation is working."

	if ( len(CLASSIFIED.get('UNEXPECTED_BUT_WORKED', [])) > 0 ):

		info = "The test following user channels weren't expected to exist but they did, so they could not be created again: "

		if not briefing:
			briefing = info
			briefing += "<strong>%s</strong>" % string.join(CLASSIFIED['UNEXPECTED_BUT_WORKED'], " | ")
			message = info
		else:
			message += "<br/>" + info

		message += "<br/><br/><strong>%s</strong>" % string.join(CLASSIFIED['UNEXPECTED_BUT_WORKED'], "<br/>")
		info = "<br/>But we could assert that user channel creation worked for some test user channels."
		briefing += info
		message += info
		message += "<br/>We deleted the existing test user channels and then were successful in creating them again."

	if ( len(CLASSIFIED.get('CREATED', [])) > 0 ):

		info = "We could successfully assert creation of the following test user channels: "
		info += "<br/><br/><strong>%s</strong>" % string.join(CLASSIFIED['CREATED'], "<br/>")
		info += "<br/>These test user channels will be used for testing purposes."

		if not briefing:
			briefing = "Could successfully create the following test user channels: "
			briefing += "<strong>%s</strong>" % string.join(CLASSIFIED['CREATED'], " | ")
			message = info
		else:
			message += "<br/>" + info

	return (status, briefing, message, None)
