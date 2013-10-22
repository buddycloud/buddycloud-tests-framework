from metadata_modification_utils import performMetadataModificationTests
from find_api_location import findAPILocation

def testFunction(domain_url, session):

	(status, briefing, message, api_location) = findAPILocation(domain_url)
	if status != 0:
		return (status, briefing, message, api_location)

	expected_results = {
		'UPDATE_TITLE'	: {
			True : [
			"test_user_channel_authorized@" + domain_url
			]
		},
		'UPDATE_DESCRIPTION'	: {
			True : [
			"test_user_channel_authorized@" + domain_url
			]
		},
		'UPDATE_ACCESS_MODEL'	: {
			True : [
			"test_user_channel_authorized@" + domain_url
			]
		},
		'UPDATE_CREATION_DATE'	: {
			False : [
			"test_user_channel_authorized@" + domain_url
			]
		},
		'UPDATE_CHANNEL_TYPE'	: {
			False : [
			"test_user_channel_authorized@" + domain_url
			]
		},
		'UPDATE_DEFAULT_AFFILIATION' : {
			True : [
			"test_user_channel_authorized@" + domain_url
			]
		}
	}

	(status, partial_report) = performMetadataModificationTests(session, domain_url, api_location, "test_user_channel_authorized", expected_results)

	if status == 0:
		briefing = "Metadata modification tests for <strong>test_user_channel_authorized@%s</strong> were successful!" % domain_url
	else:
		briefing = "Metadata modification tests for <strong>test_user_channel_authorized@%s</strong> were not entirely successful!" % domain_url

	message = briefing + "<br/>"
	message += partial_report

	return (status, briefing, message, None)
