import string
from api_utils import user_channel_exists, create_user_channel
from find_api_location import findAPILocation

TEST_USERNAME = "test_user_channel_not_following"

def testFunction(domain_url):

	CLASSIFIED = { 'EXISTED' : [], 'CREATED' : [], 'PROBLEM_CREATING' : [] }
	
	api_location = findAPILocation(domain_url)[3]

	username = TEST_USERNAME

	if user_channel_exists(domain_url, api_location, username):

		CLASSIFIED['EXISTED'].append(username + "@" + domain_url)
	else:
		if create_user_channel(domain_url, api_location, username):
	
			CLASSIFIED['CREATED'].append(username + "@" + domain_url)
		else:
			CLASSIFIED['PROBLEM_CREATING'].append(username + "@" + domain_url)

	status = 0

	if ( len(CLASSIFIED.get('PROBLEM_CREATING', [])) > 0 ):
	
		status = 1
		briefing = "Could not create some test user channels: "
		briefing += "<strong>%s</strong>" % string.join(CLASSIFIED['PROBLEM_CREATING'], " | ")
		message = "Something weird happened while we tried creating some user channels for testing purposes."
		message += "<br/>The following test user channels could not be created: <br/><br/>"
		message += "<strong>%s</strong>" % string.join(CLASSIFIED['PROBLEM_CREATING'], "<br/>")
		message += "<br/><br/>It seems like your HTTP API is problematic."

	else:

		briefing = "Could successfully assert creation or existance of some user channels: "
		message = "We could assert that user channels which will be used later for testing purposes were either created "
		message += "successfully or already existed."

	if ( len(CLASSIFIED.get('EXISTED', [])) > 0 ):

		briefing += "<strong>%s</strong>" % string.join(CLASSIFIED['EXISTED'], " | ")
		message += "<br/><br/>The following user channels already existed: <br/><br/>"
		message += "<strong>%s</strong>" % string.join(CLASSIFIED['EXISTED'], "<br/>")

	if ( len(CLASSIFIED.get('CREATED', [])) > 0 ):

		briefing += "| <strong>%s</strong>" % string.join(CLASSIFIED['CREATED'], " | ")
		message += "<br/><br/>The following user channels were successfully created: <br/><br/>"
		message += "<strong>%s</strong>" % string.join(CLASSIFIED['CREATED'], "<br/>")

	return (status, briefing, message, None)
