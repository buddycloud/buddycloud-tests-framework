from approve_new_follower_utils import performApproveSubscriptionRequestsPermissionChecks

def testFunction(domain_url, session):

	open_username = "test_user_channel_open"

	expected_results = {
		False: [
			"test_user_channel_authorized@" + domain_url
		],
		True: [
			"test_topic_channel_open@topics." + domain_url,
			"test_user_channel_open@" + domain_url
		]
	}

	return performApproveSubscriptionRequestsPermissionChecks(domain_url, session, open_username, expected_results)
