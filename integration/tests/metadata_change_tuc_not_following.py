from metadata_change_utils import performMetadataModificationTests
from find_api_location import findAPILocation

def testFunction(domain_url, session):

	(status, briefing, message, api_location) = findAPILocation(domain_url)
	if status != 0:
		return (status, briefing, message, api_location)

	expected_results = {
		'UPDATE_TITLE'	: {
			False : [
			"test_user_channel_open@" + domain_url,
			"test_topic_channel_open@topics." + domain_url,
			"test_user_channel_authorized@" + domain_url
			]
		},
		'UPDATE_DESCRIPTION'	: {
			False : [
			"test_user_channel_open@" + domain_url,
			"test_topic_channel_open@topics." + domain_url,
			"test_user_channel_authorized@" + domain_url
			]
		},
		'UPDATE_ACCESS_MODEL'	: {
			False : [
			"test_user_channel_open@" + domain_url,
			"test_topic_channel_open@topics." + domain_url,
			"test_user_channel_authorized@" + domain_url
			]
		},
		'UPDATE_CREATION_DATE'	: {
			False : [
			"test_user_channel_open@" + domain_url,
			"test_topic_channel_open@topics." + domain_url,
			"test_user_channel_authorized@" + domain_url
			]
		},
		'UPDATE_CHANNEL_TYPE'	: {
			False : [
			"test_user_channel_open@" + domain_url,
			"test_topic_channel_open@topics." + domain_url,
			"test_user_channel_authorized@" + domain_url
			]
		},
		'UPDATE_DEFAULT_AFFILIATION' : {
			False : [
			"test_user_channel_open@" + domain_url,
			"test_topic_channel_open@topics." + domain_url,
			"test_user_channel_authorized@" + domain_url
			]
		}
	}

	(status, partial_report) = performMetadataModificationTests(session, domain_url, api_location, "test_user_channel_not_following", expected_results)

	if status == 0:
		briefing = "Metadata change tests for <strong>test_user_channel_not_following@%s</strong> were successful!" % domain_url
	else:
		briefing = "Metadata change tests for <strong>test_user_channel_not_following@%s</strong> were not entirely successful!" % domain_url

	message = briefing + "<br/>"
	message += partial_report

	return (status, briefing, message, None)
