from approve_new_follower_utils import performApproveSubscriptionRequestsPermissionChecks

def testFunction(domain_url, session):

	expected_results = {
		False: [
			"test_user_channel_authorized@" + domain_url,
			"test_topic_channel_open@topics." + domain_url,
			"test_user_channel_open@" + domain_url
		]
	}

	return performApproveSubscriptionRequestsPermissionChecks(domain_url, session, None, expected_results)
