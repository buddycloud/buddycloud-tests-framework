from role_change_utils import performRoleChangePermissionChecks

def testFunction(domain_url, session):

	expected_results = {
		'CHANGE_TO_MODERATOR' : {
			False: [
			"test_user_channel_open@" + domain_url,
			"test_user_channel_authorized@" + domain_url,
			"test_topic_channel_open@topics." + domain_url
			]
		},
		'CHANGE_TO_FOLLOWER_POST' : {
			False: [
			"test_user_channel_open@" + domain_url,
			"test_user_channel_authorized@" + domain_url,
			"test_topic_channel_open@topics." + domain_url
			]
		},
		'CHANGE_TO_FOLLOWER' : {
			False: [
			"test_user_channel_open@" + domain_url,
			"test_user_channel_authorized@" + domain_url,
			"test_topic_channel_open@topics." + domain_url
			]
		},
		'CHANGE_TO_BANNED' : {
			False: [
			"test_user_channel_open@" + domain_url,
			"test_user_channel_authorized@" + domain_url,
			"test_topic_channel_open@topics." + domain_url
			]
		}
	}

	(status, partial_report) = performRoleChangePermissionChecks(domain_url, session, "test_user_channel_not_following", expected_results)

	if status == 0:
		briefing = "Role change permission tests for <strong>test_user_channel_not_following@" + domain_url + "</strong> were successful!"
	else:
		briefing = "Role change permission tests for <strong>test_user_channel_not_following@" + domain_url + "</strong> were not entirely successful!"

	message = briefing + "<br/>"
	message += partial_report

	return (status, briefing, message, None)
