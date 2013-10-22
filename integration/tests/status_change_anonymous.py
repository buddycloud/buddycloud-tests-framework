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

	(status, partial_report) = performStatusManagementTests(session, domain_url, api_location, None, expected_results)

	if status == 0:
		briefing = "Status management tests for <strong>anonymous user</strong> were successful!"
	else:
		briefing = "Status management tests for <strong>anonymous user</strong> were not entirely successful!"

	message = briefing + "<br/>"
	message += partial_report

	return (status, briefing, message, None)
