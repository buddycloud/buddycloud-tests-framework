import string
from api_utils import user_channel_exists, create_user_channel, open_this_user_channel, delete_user_channel
from find_api_location import findAPILocation


def testFunction(domain_url):

	(status, briefing, message, api_location) = findAPILocation(domain_url)
	if status != 0:
		return (status, briefing, message, None)

	username = "test_user_channel_open"

	if create_user_channel(domain_url, api_location, username):

		if ( open_this_user_channel(domain_url, api_location, username) ):

			status = 0
			briefing = "Could successfully create test user channel: <strong>%s@%s</strong>" % (username, domain_url)
			message = "We could successfully assert creation of test user channel <strong>%s@%s</strong>." % (username, domain_url)
			message += "<br/>That test user channel will be used for testing purposes."

		else:
			
			status = 1
			briefing = "Could successfully create test user channel <strong>%s@%s</strong> " % (username, domain_url)
			briefing += "but could not change privacy setting to <em>open</em>!"
			message = "We could successfully assert creation of test user channel <strong>%s@%s</strong>." % (username, domain_url)
			message += "<br/>The problem is we could not have its privacy setting set to <em>open</em>."
			message += "<br/>That test user channel is intended to be open and will be used for testing purposes."

	else:

		if user_channel_exists(domain_url, api_location, username):			

			status = 2
			briefing = "The test user channel <strong>%s@%s</strong> wasn't " % (username, domain_url)
			briefing += "expected to exist but it did, so it could not be created again."
			message = briefing

			if ( delete_user_channel(domain_url, api_location, username)
			and create_user_channel(domain_url, api_location, username) ):

				status = 0
				additional_info = "<br/>But we could assert that <em>open</em> user channel creation is being "
				additional_info += "properly implemented by your API server."
				briefing += additional_info
				message += additional_info
				message += "<br/>We deleted the existing test user channel and then were successful in creating it again."
			else:
				message += "<br/>The problem is we cannot assert that <em>open</em> user channel creation is working."

		else:

			status = 1
			briefing = "The test user channel <strong>%s@%s</strong> could not be created." % (username, domain_url)
			message = briefing
			message += "<br/>It seems like your HTTP API server is problematic. It had trouble creating an "
			message += "<em>open</em> user channel - that operation must work."
			
	return (status, briefing, message, None)
