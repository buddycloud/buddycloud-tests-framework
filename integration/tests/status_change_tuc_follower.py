from status_change_utils import performStatusManagementTests
from find_api_location import findAPILocation

def testFunction(domain_url, session):

	(status, briefing, message, api_location) = findAPILocation(domain_url)
	if status != 0:
		return (status, briefing, message, api_location)

	expected_results = {
		'ADD_NEW_STATUS_AND_CHECK' : {
			False : [
			"test_user_channel_open@" + domain_url,
			"test_topic_channel_authorized@" + domain_url
			]
		}
	}

	(status, partial_report) = performStatusManagementTests(session, domain_url, api_location, "test_user_channel_follower3", expected_results)

	if status == 0:
		briefing = "Status management tests for <strong>test_user_channel_follower3@%s</strong> were successful!" % domain_url
	else:
		briefing = "Status management tests for <strong>test_user_channel_follower3@%s</strong> were not entirely successful!" % domain_url

	message = briefing + "<br/>"
	message += partial_report

	return (status, briefing, message, None)
