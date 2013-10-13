from posts_management_utils import performPostsManagementTests
from find_api_location import findAPILocation

def testFunction(domain_url):

	(status, briefing, message, api_location) = findAPILocation(domain_url)
	if status != 0:
		return (status, briefing, message, api_location)

	expected_results = {
		'ADD_NEW_POST_AND_GET_BY_ID_DIRECT_ACCESS' : {
			True : [
			"test_user_channel_open@" + domain_url,
			"test_topic_channel_open@topics." + domain_url
			]
		},
		'ADD_NEW_POST_AND_GET_BY_MATCHING_ID' : {
			True : [
			"test_user_channel_open@" + domain_url,
			"test_topic_channel_open@topics." + domain_url
			]
		}
	}

	(status, partial_report) = performPostsManagementTests(domain_url, api_location, "test_user_channel_open", expected_results)

	if status == 0:
		briefing = "Posts management tests for <strong>test_user_channel_open@%s</strong> were successful!" % domain_url
	else:
		briefing = "Posts management tests for <strong>test_user_channel_open@%s</strong> were not entirely successful!" % domain_url

	message = briefing + "<br/>"
	message += partial_report

	return (status, briefing, message, None)
