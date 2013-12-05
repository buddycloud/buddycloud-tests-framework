from posts_management_utils import performPostsManagementTests
from find_api_location import findAPILocation

def testFunction(domain_url, session):

	(status, briefing, message, api_location) = findAPILocation(domain_url)
	if status != 0:
		return (status, briefing, message, api_location)

	expected_results = {
		'ADD_NEW_POST_AND_GET_BY_ID_DIRECT_ACCESS' : {
			True : [
			"test_user_channel_authorized@" + domain_url
			]
		},
		'ADD_NEW_POST_AND_GET_BY_MATCHING_ID' : {
			True : [
			"test_user_channel_authorized@" + domain_url
			]
		},
		'REMOVE_OWN_POST' : {
			True : [
			"test_user_channel_authorized@" + domain_url
			]
		},
		'REMOVE_POST_CREATED_BY_OWNER' : {
			True : [
			"test_user_channel_authorized@" + domain_url
			]
		},
		'REMOVE_POST_CREATED_BY_MODERATOR' : {
			True : [
			"test_user_channel_authorized@" + domain_url
			]
		}
	}

	(status, partial_report) = performPostsManagementTests(session, domain_url, api_location, "test_user_channel_authorized", expected_results)

	if status == 0:
		briefing = "Posts management tests for <strong>test_user_channel_authorized@%s</strong> were successful!" % domain_url
	else:
		briefing = "Posts management tests for <strong>test_user_channel_authorized@%s</strong> were not entirely successful!" % domain_url

	message = briefing + "<br/>"
	message += partial_report

	return (status, briefing, message, None)
