import string, sets
from api_utils import user_channel_exists, create_user_channel, subscribe_to_user_channel, subscribe_to_topic_channel, approve_another_user_channel_subscription_request, approve_another_topic_channel_subscription_request, approve_user_channel_subscription_request, approve_topic_channel_subscription_request
from find_api_location import findAPILocation

def performApproveSubscriptionRequestsPermissionChecks(domain_url, session, tested_username, expected_results):

	(sts, bri, mes, api_location) = findAPILocation(domain_url)
	if ( sts != 0 ):
		return (sts, bri, mes, None)

	if ( tested_username != None ):
		new_follower_username = tested_username + "_new_follower"
	else:
		new_follower_username = "test_user_channel_anonymous_new_follower"

	target_user_channels = [ "test_user_channel_open", "test_user_channel_authorized" ]
	target_topic_channels = [ "test_topic_channel_open" ]

	classified = { 'SUCCESS' : [], 'FAIL' : [], 'PROBLEM_SUBSCRIBING' : [], 'PROBLEM_CREATING' : [] }

	if ( create_user_channel(session, domain_url, api_location, new_follower_username)
			or user_channel_exists(session, domain_url, api_location, new_follower_username) ):

		for channel in target_user_channels:

			if subscribe_to_user_channel(session, domain_url, api_location, new_follower_username, channel, "member"):

				if approve_another_user_channel_subscription_request(session,
						domain_url, api_location, channel, tested_username, [new_follower_username]):
					
					if ("%s@%s" % (channel, domain_url)) in expected_results.get(True,[]):
						classified['SUCCESS'].append("%s@%s" % (channel, domain_url))
					else:
						classified['FAIL'].append("%s@%s" % (channel, domain_url))
				else:

					if ("%s@%s" % (channel, domain_url)) in expected_results.get(False,[]):
						classified['SUCCESS'].append("%s@%s" % (channel, domain_url))
					else:
						classified['FAIL'].append("%s@%s" % (channel, domain_url))

					approve_user_channel_subscription_request(session, domain_url, api_location, channel, [new_follower_username])

			else:
				classified['PROBLEM_SUBSCRIBING'].append("%s@%s" % (channel, domain_url))

		for channel in target_topic_channels:

			if subscribe_to_topic_channel(session, domain_url, api_location, new_follower_username, channel, "member"):

				if approve_another_topic_channel_subscription_request(session,
						domain_url, api_location, channel, target_user_channels[0], tested_username, [new_follower_username]):

					if ("%s@topics.%s" % (channel, domain_url)) in expected_results.get(True,[]):
						classified['SUCCESS'].append("%s@topics.%s" % (channel, domain_url))
					else:
						classified['FAIL'].append("%s@topics.%s" % (channel, domain_url))

				else:	
					if ("%s@topics.%s" % (channel, domain_url)) in expected_results.get(False,[]):
						classified['SUCCESS'].append("%s@topics.%s" % (channel, domain_url))
					else:
						classified['FAIL'].append("%s@topics.%s" % (channel, domain_url))

					approve_topic_channel_subscription_request(session, domain_url, api_location, channel, target_user_channels[0], [new_follower_username])
			else:
				classified['PROBLEM_SUBSCRIBING'].append("%s@topics.%s" % (channel, domain_url))

	else:
		classified['PROBLEM_CREATING'].append("%s@%s" % (new_follower_username, domain_url))


	if ( tested_username != None ):
		tested_username = "<strong>%s@%s</strong>" % (tested_username, domain_url)
	else:
		tested_username = "<strong>anonymous user</strong>"

	if ( len(classified.get('PROBLEM_CREATING', [])) > 0 ):

		status = 2
		briefing = "This test failed because we could not create test user channel <strong>%s</strong>." % classified['PROBLEM_CREATING'][0]
		message = briefing + "<br/>We need that user for testing purposes.<br/><br/>It seems like your HTTP API is problematic."
		return (status, briefing, message, None)

	if ( len(classified.get('PROBLEM_SUBSCRIBING', [])) > 0 ):

		status = 2
		briefing = "Could not have test user channel <strong>%s</strong> "
		briefing += "subscribe to the following channels: "
		new_follower_username = "<strong>%s@%s</strong>" % (new_follower_username, domain_url)
		briefing = briefing % new_follower_username
		message = briefing
		briefing += "<strong>%s</strong>" % string.join(classified['PROBLEM_SUBSCRIBING'], " | ")
		message += "<br/><br/><strong>%s</strong>" % string.join(classified['PROBLEM_SUBSCRIBING'], "<br/>")
		message += "<br/><br/>Thus, we could not test if %s can approve new followers." % tested_username
		return (status, briefing, message, None)

	status = 0
	briefing = ""
	message = ""

	if ( len(classified.get('FAIL', [])) > 0 ):

		status = 1
		briefing = "Approve new followers permission tests for <strong>%s</strong> were not entirely successful!" % tested_username
		message = briefing + "<br/>"

		should_have_permission = sets.Set(expected_results.get(True,[]))
		should_not_have_permission = sets.Set(expected_results.get(False,[]))
		had_problems = sets.Set(classified['FAIL'])

		should_have_permission_but_didnt = should_have_permission.intersection(had_problems)
		should_not_have_permission_but_did = should_not_have_permission.intersection(had_problems)

		if ( len(should_have_permission_but_didnt) > 0 ):

			message = "User %s could not approve subscription requests to the "
			message += "following channels (<strong>and it should be able to!</strong>): "
			message = message % (tested_username)
			message += "<br/><br/><strong>%s</strong><br/>" % string.join(should_have_permission_but_didnt, "<br/>")


		if ( len(should_not_have_permission_but_did) > 0 ):

			if ( message != "" ):
				message += "<br/>"

			message += "User %s could approve subscription requests to the "
			message += "following channels (<strong>and it should not be able to!</strong>): "
			message = message % (tested_username)
			message += "<br/><br/><strong>%s</strong><br/>" % string.join(should_not_have_permission_but_did, "<br/>")

	if ( len(classified.get('SUCCESS', [])) > 0 ):

		if ( briefing == "" ):
			briefing += "User %s has correct approve subscription permissions!" % tested_username

		should_have_permission = sets.Set(expected_results.get(True,[]))
		should_not_have_permission = sets.Set(expected_results.get(False,[]))
		had_no_problems = sets.Set(classified['SUCCESS'])

		should_have_permission_and_did = should_have_permission.intersection(had_no_problems)
		should_not_have_permission_and_didnt = should_not_have_permission.intersection(had_no_problems)

		if ( message != "" ):
			message += "<br/>"

		message += "<span class='muted'>The following approve new followers permission tests were successful: <br/>"

		if ( len(should_have_permission_and_did) > 0 ):

			if ( message != "" ):
				message += "<br/>"

			message += "User %s could approve subscription requests to the "
			message += "following channels (<em>as expected!</em>): "
			message = message % (tested_username)
			message += "<br/><br/><strong>%s</strong><br/>" % string.join(should_have_permission_and_did, "<br/>")

		if ( len(should_not_have_permission_and_didnt) > 0 ):

			if ( message != "" ):
				message += "<br/>"

			message += "User %s could not approve subscription requests to the "
			message += "following channels (<em>as expected!</em>): "
			message = message % (tested_username)
			message += "<br/><br/><strong>%s</strong><br/>" % string.join(should_not_have_permission_and_didnt, "<br/>")

		message += "</span>"

	return (status, briefing, message, None)
