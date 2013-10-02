import string
from api_utils import topic_channel_exists, create_topic_channel
from find_api_location import findAPILocation

TEST_TOPIC_CHANNEL_NAME = "test_topic_channel_open"
TEST_TOPIC_CHANNEL_OWNER_USERNAME = "test_user_channel_open"

def testFunction(domain_url):

	CLASSIFIED = { 'EXISTED' : [], 'CREATED' : [], 'PROBLEM' : [] }

	(status, briefing, message, api_location) = findAPILocation(domain_url)
	if status != 0:
		return (status, briefing, message, None)

	if topic_channel_exists(domain_url, api_location, TEST_TOPIC_CHANNEL_NAME):
		CLASSIFIED['EXISTED'].append(TEST_TOPIC_CHANNEL_NAME + "@topics." + domain_url)
	else:
		if create_topic_channel(domain_url, api_location, TEST_TOPIC_CHANNEL_OWNER_USERNAME, TEST_TOPIC_CHANNEL_NAME):
			CLASSIFIED['CREATED'].append(TEST_TOPIC_CHANNEL_NAME + "@topics." + domain_url)
		else:
			CLASSIFIED['PROBLEM'].append(TEST_TOPIC_CHANNEL_NAME + "@topics." + domain_url)

	status = 0

	if ( len(CLASSIFIED.get('PROBLEM', [])) > 0 ):
	
		status = 1
		briefing = "Could not create some test topic channels: "
		briefing += "<strong>%s</strong>" % string.join(CLASSIFIED['PROBLEM'], " | ")
		message = "Something weird happened while we tried creating some topic channels for testing purposes."
		message += "<br/>The following test topic channels could not be created: <br/><br/>"
		message += "<strong>%s</strong>" % string.join(CLASSIFIED['PROBLEM'], "<br/>")
		message += "<br/><br/>It seems like your HTTP API is problematic."
	
	else:

		briefing = "Could successfully assert creation or existance of some topic channels: "
		message = "We could assert that topic channels which will be used later for testing purposes were either created "
		message += "successfully or already existed."

	if ( len(CLASSIFIED.get('EXISTED', [])) > 0 ):

		briefing += "<strong>%s</strong>" % string.join(CLASSIFIED['EXISTED'], " | ")
		message += "<br/><br/>The following topic channels already existed: <br/><br/>"
		message += "<strong>%s</strong>" % string.join(CLASSIFIED['EXISTED'], "<br/>")

	if ( len(CLASSIFIED.get('CREATED', [])) > 0 ):

		briefing += "<strong>%s</strong>" % string.join(CLASSIFIED['CREATED'], " | ")
		message += "<br/><br/>The following topic channels were successfully created: <br/><br/>"
		message += "<strong>%s</strong>" % string.join(CLASSIFIED['CREATED'], "<br/>")

	return (status, briefing, message, None)
