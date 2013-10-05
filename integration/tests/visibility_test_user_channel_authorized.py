from visibility_utils import performVisibilityTests

def testFunction(domain_url):

	expected_results = {
		'ALL_METADATA_ACCESS'	: { True : ["test_user_channel_authorized@" + domain_url] },
		'MOOD_STATUS_ACCESS'	: { True : ["test_user_channel_authorized@" + domain_url] },
		'POSTS_READ_ACCESS'	: { True : ["test_user_channel_authorized@" + domain_url] },
		'SUBSCRIBERS_ACCESS'	: { True : ["test_user_channel_authorized@" + domain_url] },
		'BANNED_SUBSCRIBERS_ACCESS' : { True : ["test_user_channel_authorized@" + domain_url] }
#		'OUTSIDE_ROLES_ACCESS'	: { True : ["test_user_channel_authorized@" + domain_url] }#,
#		'GEOLOC_ACCESS'		: { True : ["test_user_channel_authorized@" + domain_url] }
	}

	(status, partial_report) = performVisibilityTests(domain_url, "test_user_channel_authorized", expected_results)

	if status == 0:
		briefing = "Visibility tests for <strong>test_user_channel_authorized@%s</strong> were successful!" % domain_url
	else:
		briefing = "Visibility tests for <strong>test_user_channel_authorized@%s</strong> were not entirely successful!" % domain_url

	message = briefing + "<br/>"
	message += partial_report

	return (status, briefing, message, None)
