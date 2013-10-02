import string
from api_utils import user_channel_exists, create_user_channel, is_closed_user_channel, close_this_user_channel
from find_api_location import findAPILocation

TEST_USERNAME = "test_user_channel_closed"

def testFunction(domain_url):

	CLASSIFIED = { 'EXISTED' : [], 'CREATED' : [], 'PROBLEM_CREATING' : [], 'PROBLEM_CLOSING' : [] }

	(status, briefing, message, api_location) = findAPILocation(domain_url)
	if status != 0:
		return (status, briefing, message, None)

	username = TEST_USERNAME

	if user_channel_exists(domain_url, api_location, username):

		if ( is_closed_user_channel(domain_url, api_location, username) 
		or close_this_user_channel(domain_url, api_location, username) ):
			CLASSIFIED['EXISTED'].append(username + "@" + domain_url)
		else:
			CLASSIFIED['PROBLEM_CLOSING'].append(username + "@" + domain_url)
	else:
		if create_user_channel(domain_url, api_location, username):

			if ( is_closed_user_channel(domain_url, api_location, username)
			or close_this_user_channel(domain_url, api_location, username) ):
				CLASSIFIED['CREATED'].append(username + "@" + domain_url)
			else:
				CLASSIFIED['PROBLEM_CLOSING'].append(username + "@" + domain_url)
		else:
			CLASSIFIED['PROBLEM_CREATING'].append(username + "@" + domain_url)

	status = 0

	if ( len(CLASSIFIED.get('PROBLEM_CREATING', [])) > 0 ):
	
		status = 1
		briefing = "Could not create some <em>closed</em> test user channels: "
		briefing += "<strong>%s</strong>" % string.join(CLASSIFIED['PROBLEM_CREATING'], " | ")
		message = "Something weird happened while we tried creating some <em>closed</em> user channels for testing purposes."
		message += "<br/>The following test user channels could not be created: <br/><br/>"
		message += "<strong>%s</strong>" % string.join(CLASSIFIED['PROBLEM_CREATING'], "<br/>")
		message += "<br/><br/>It seems like your HTTP API is problematic."

	elif ( len(CLASSIFIED.get('PROBLEM_CLOSING', [])) > 0 ):

		status = 1
		briefing = "Could not set some user channels privacy setting to <em>closed</em>: "
		briefing += "<strong>%s</strong>" % string.join(CLASSIFIED['PROBLEM_CLOSING'], " | ")
		message = "Something weird happened while we tried creating some <em>closed</em> user channels for testing purposes."
		message += "<br/>The following test user channels could not have privacy settings set to <em>closed</em>: <br/><br/>"
		message += "<strong>%s</strong>" % string.join(CLASSIFIED['PROBLEM_CLOSING'], "<br/>")
		message += "<br/><br/>It seems like your HTTP API is problematic."

	else:

		briefing = "Could successfully assert creation or existance of some <em>closed</em> user channels: "
		message = "We could assert that <em>closed</em> user channels which will be used later for testing purposes were either created "
		message += "successfully or already existed."

	if ( len(CLASSIFIED.get('EXISTED', [])) > 0 ):

		briefing += "<strong>%s</strong>" % string.join(CLASSIFIED['EXISTED'], " | ")
		message += "<br/><br/>The following <em>closed</em> user channels already existed: <br/><br/>"
		message += "<strong>%s</strong>" % string.join(CLASSIFIED['EXISTED'], "<br/>")

	if ( len(CLASSIFIED.get('CREATED', [])) > 0 ):

		briefing += "| <strong>%s</strong>" % string.join(CLASSIFIED['CREATED'], " | ")
		message += "<br/><br/>The following <em>closed</em> user channels were successfully created: <br/><br/>"
		message += "<strong>%s</strong>" % string.join(CLASSIFIED['CREATED'], "<br/>")

	return (status, briefing, message, None)
