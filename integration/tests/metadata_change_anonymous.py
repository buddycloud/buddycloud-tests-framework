from metadata_modification_utils import performMetadataModificationTests
from find_api_location import findAPILocation

def testFunction(domain_url):

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

	(status, partial_report) = performMetadataModificationTests(domain_url, api_location, None, expected_results)

	if status == 0:
		briefing = "Metadata modification tests for <strong>anonymous user@%s</strong> were successful!" % domain_url
	else:
		briefing = "Metadata modification tests for <strong>anonymous user@%s</strong> were not entirely successful!" % domain_url

	message = briefing + "<br/>"
	message += partial_report

	return (status, briefing, message, None)
