from approve_new_follower_utils import performApproveSubscriptionRequestsPermissionChecks

def testFunction(domain_url, session):

	follower_post_username = "test_user_channel_follower2"

	expected_results = {
		False: [
			"test_topic_channel_open@topics." + domain_url,
			"test_user_channel_open@" + domain_url,
			"test_user_channel_authorized@" + domain_url
		]
	}

	return performApproveSubscriptionRequestsPermissionChecks(domain_url, session, follower_post_username, expected_results)
