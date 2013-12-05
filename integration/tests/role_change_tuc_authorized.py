from role_change_utils import performRoleChangePermissionChecks

def testFunction(domain_url, session):

	expected_results = {
		'CHANGE_TO_MODERATOR' : {
			True: [
			"test_user_channel_authorized@" + domain_url
			]
		},
		'CHANGE_TO_FOLLOWER_POST' : {
			True: [
			"test_user_channel_authorized@" + domain_url
			]
		},
		'CHANGE_TO_FOLLOWER' : {
			True: [
			"test_user_channel_authorized@" + domain_url
			]
		},
		'CHANGE_TO_BANNED' : {
			True: [
			"test_user_channel_authorized@" + domain_url
			]
		}
	}

	(status, partial_report) = performRoleChangePermissionChecks(domain_url, session, "test_user_channel_authorized", expected_results)

	if status == 0:
		briefing = "Role change permission tests for <strong>test_user_channel_authorized@" + domain_url + "</strong> were successful!"
	else:
		briefing = "Role change permission tests for <strong>test_user_channel_authorized@" + domain_url + "</strong> were not entirely successful!"

	message = briefing + "<br/>"
	message += partial_report

	return (status, briefing, message, None)
