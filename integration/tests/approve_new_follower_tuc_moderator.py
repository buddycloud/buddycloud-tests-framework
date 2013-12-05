from approve_new_follower_utils import performApproveSubscriptionRequestsPermissionChecks

def testFunction(domain_url, session):

	moderator_username = "test_user_channel_follower1"

	expected_results = {
		True : [
			"test_topic_channel_open@topics." + domain_url
		],
		False: [
			"test_user_channel_open@" + domain_url,
			"test_user_channel_authorized@" + domain_url
		]
	}

	return performApproveSubscriptionRequestsPermissionChecks(domain_url, session, moderator_username, expected_results)
