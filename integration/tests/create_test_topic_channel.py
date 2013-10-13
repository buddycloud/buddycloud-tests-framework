import string
from api_utils import topic_channel_exists, create_topic_channel, delete_topic_channel
from find_api_location import findAPILocation


def testFunction(domain_url):

	(status, briefing, message, api_location) = findAPILocation(domain_url)
	if status != 0:
		return (status, briefing, message, None)

	test_topic_channel_name = "test_topic_channel_open"
	test_topic_channel_owner_username = "test_user_channel_open"

	if create_topic_channel(domain_url, api_location, test_topic_channel_owner_username, test_topic_channel_name):
	
		status = 0
		briefing = "Could successfully create test topic channel: <strong>%s@topics.%s</strong>" % (test_topic_channel_name, domain_url)
		message = "We could successfully assert creation of test topic channel <strong>%s@topics.%s</strong>." % (test_topic_channel_name, domain_url)
		message += "<br/>That topic channel will be used for testing purposes."

		return (status, briefing, message, None)

	else:

		if topic_channel_exists(domain_url, api_location, test_topic_channel_name):

			status = 2
			briefing = "The test topic channel <strong>%s@topics.%s</strong> wasn't " % (test_topic_channel_name, domain_url)
			briefing += "expected to exist but it did, so it could not be created again."
			message = briefing

			if ( delete_user_channel(domain_url, api_location, test_topic_channel_owner_username, test_topic_channel_name)
			and create_user_channel(domain_url, api_location, test_topic_channel_owner_username, test_topic_channel_name) ):

				status = 0
				additional_info = "<br/>But we could assert that topic channel creation is being properly implemented by your API server."
				briefing += additional_info
				message += additional_info
				message += "<br/>We deleted the existing test topic channel and then were successful in creating it again."
			else:
				message += "<br/>The problem is we cannot assert that topic channel creation is working."

			return (status, briefing, message, None)

		else:

			status = 1
			briefing = "The test topic channel <strong>%s@topics.%s</strong> could not be created." % (test_topic_channel_name, domain_url)
			message = briefing
			message += "<br/>It seems like your HTTP API server is problematic. It had trouble creating a topic channel - that operation must work."
			
			return (status, briefing, message, None)
