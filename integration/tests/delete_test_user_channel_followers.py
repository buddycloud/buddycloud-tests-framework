import string
from api_utils import user_channel_exists, create_user_channel, delete_user_channel
from find_api_location import findAPILocation


def testFunction(domain_url):

	CLASSIFIED = { 'DELETED' : [], 'UNEXPECTED' : [], 'UNEXPECTED_BUT_WORKED' : [], 'NOT_DELETED' : [] }

	(status, briefing, message, api_location) = findAPILocation(domain_url)
	if status != 0:
		return (status, briefing, message, None)

	prefix = "test_user_channel_follower"

	for i in range(1, 5):

		username = prefix + str(i)

		if delete_user_channel(domain_url, api_location, username):
			CLASSIFIED['DELETED'].append("%s@%s" % (username, domain_url))
		else:
			if not user_channel_exists(domain_url, api_location, username):

				if ( create_user_channel(domain_url, api_location, username)
				and delete_user_channel(domain_url, api_location, username) ):
					CLASSIFIED['UNEXPECTED_BUT_WORKED'].append("%s@%s" % (username, domain_url))
				else:
					CLASSIFIED['UNEXPECTED'].append("%s@%s" % (username, domain_url))
			else:
				CLASSIFIED['NOT_DELETED'].append("%s@%s" % (username, domain_url))

	status = 0
	briefing = ""
	message = ""

	if ( len(CLASSIFIED.get('NOT_DELETED', [])) > 0 ):
	
		status = 1
		briefing = "The following test user channels could not be deleted:"
		message = briefing
		briefing += " <strong>%s</strong>" % string.join(CLASSIFIED['NOT_DELETED'], " | ")
		message += "<br/><br/><strong>%s</strong>" % string.join(CLASSIFIED['NOT_DELETED'], "<br/>")
		message += "<br/>It seems like your HTTP API server is problematic. It had trouble deleting "
		message += "user channels - these operations must work."
	
	if ( len(CLASSIFIED.get('UNEXPECTED', [])) > 0 ):

		if status == 0:
			status = 2

		info = "The following test user channels were expected to exist but they didn't, so they could not be deleted again: "

		if not briefing:
			briefing = info
			briefing += "<strong>%s</strong>" % string.join(CLASSIFIED['UNEXPECTED'], " | ")
			message = info
		else:
			message += "<br/>" + info

		message += "<br/><br/><strong>%s</strong>" % string.join(CLASSIFIED['UNEXPECTED'], "<br/>")
		message += "<br/>The problem is we cannot assert that user channel deletion is working."

	if ( len(CLASSIFIED.get('UNEXPECTED_BUT_WORKED', [])) > 0 ):

		info = "The test following user channels were expected to exist but they didn't, so they could not be deleted again: "

		if not briefing:
			briefing = info
			briefing += "<strong>%s</strong>" % string.join(CLASSIFIED['UNEXPECTED_BUT_WORKED'], " | ")
			message = info
		else:
			message += "<br/>" + info

		message += "<br/><br/><strong>%s</strong>" % string.join(CLASSIFIED['UNEXPECTED_BUT_WORKED'], "<br/>")
		info = "<br/>But we could assert that user channel deletion worked for some test user channels."
		briefing += info
		message += info
		message += "<br/>We created the expected test user channels and then were successful in deleting them again."

	if ( len(CLASSIFIED.get('DELETED', [])) > 0 ):

		info = "We could successfully assert deletion of the following test user channels: "
		info += "<br/><br/><strong>%s</strong>" % string.join(CLASSIFIED['DELETED'], "<br/>")
		info += "<br/>These test user channels were being used for testing purposes."

		if not briefing:
			briefing = "Could successfully delete the following test user channels: "
			briefing += "<strong>%s</strong>" % string.join(CLASSIFIED['DELETED'], " | ")
			message = info
		else:
			message += "<br/>" + info

	return (status, briefing, message, None)
