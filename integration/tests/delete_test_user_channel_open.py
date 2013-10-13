import string
from api_utils import user_channel_exists, create_user_channel, open_this_user_channel, delete_user_channel
from find_api_location import findAPILocation


def testFunction(domain_url):

	(status, briefing, message, api_location) = findAPILocation(domain_url)
	if status != 0:
		return (status, briefing, message, None)

	username = "test_user_channel_open"

	if delete_user_channel(domain_url, api_location, username):

		status = 0
		briefing = "Could successfully delete test user channel: <strong>%s@%s</strong>" % (username, domain_url)
		message = "We could successfully assert deletion of test user channel <strong>%s@%s</strong>." % (username, domain_url)
		message += "<br/>That test user channel was being used for testing purposes."
			
	else:

		if not user_channel_exists(domain_url, api_location, username):			

			status = 2
			briefing "The test user channel <strong>%s@%s</strong> was " % (username, domain_url)
			briefing += "expected to exist but it didn't, so it could not be deleted again."
			message = briefing

			if ( create_user_channel(domain_url, api_location, username)
			and ( open_this_user_channel(domain_url, api_location, username)
			and delete_user_channel(domain_url, api_location, username) ):

				status = 0
				additional_info = "<br/>But we could assert that <em>open</em> user channel deletion is being "
				additional_info += "properly implemented by your API server."
				briefing += additional_info
				message += additional_info
				message += "<br/>We created the expected test user channel and then were successful in deleting it again."
			else:
				message += "<br/>The problem is we cannot assert that <em>open</em> user channel deletion is working."

			return (status, briefing, message, None)
		
		else:

			status = 1
			briefing = "The test user channel <strong>%s@%s</strong> could not be deleted." % (username, domain_url)
			message = briefing
			message += "<br/>It seems like your HTTP API server is problematic. It had trouble deleting an "
			message += "<em>open</em> user channel - that operation must work."
			
			return (status, briefing, message, None)
