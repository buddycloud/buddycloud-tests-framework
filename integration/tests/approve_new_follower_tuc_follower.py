import string, sets
from api_utils import user_channel_exists, create_user_channel, subscribe_to_user_channel, subscribe_to_topic_channel, approve_another_user_channel_subscription_request, approve_another_topic_channel_subscription_request
from find_api_location import findAPILocation

def testFunction(domain_url, session):

	(sts, bri, mes, api_location) = findAPILocation(domain_url)
	if ( sts != 0 ):
		return (sts, bri, mes, None)

	new_follower_username = "test_user_channel_moderator_new_follower"
	moderator_username = "test_user_channel_follower3"
	target_user_channels = [ "test_user_channel_open", "test_user_channel_authorized" ]
	target_topic_channels = [ "test_topic_channel_open" ]

	expected_results = {
		False: [
			"test_topic_channel_open@topics." + domain_url,
			"test_user_channel_open@" + domain_url,
			"test_user_channel_authorized@" + domain_url
		]
	}

	classified = { 'SUCCESS' : [], 'FAIL' : [], 'PROBLEM_SUBSCRIBING' : [], 'PROBLEM_CREATING' : [] }

	if ( create_user_channel(session, domain_url, api_location, new_follower_username)
			or user_channel_exists(session, domain_url, api_location, new_follower_username) ):

		for channel in target_user_channels:

			if subscribe_to_user_channel(session, domain_url, api_location, new_follower_username, channel, "member"):

				if approve_another_user_channel_subscription_request(session,
						domain_url, api_location, channel, moderator_username, [new_follower_username]):
					
					if ("%s@%s" % (channel, domain_url)) in expected_results[True]:
						classified['SUCCESS'].append("%s@%s" % (channel, domain_url))
					else:
						classified['FAIL'].append("%s@%s" % (channel, domain_url))
				else:

					if ("%s@%s" % (channel, domain_url)) in expected_results[False]:
						classified['SUCCESS'].append("%s@%s" % (channel, domain_url))
					else:
						classified['FAIL'].append("%s@%s" % (channel, domain_url))

			else:
				classified['PROBLEM_SUBSCRIBING'].append("%s@%s" % (channel, domain_url))

		for channel in target_topic_channels:

			if subscribe_to_topic_channel(session, domain_url, api_location, new_follower_username, channel, "member"):

				if approve_another_topic_channel_subscription_request(session,
						domain_url, api_location, channel, target_user_channels[0], moderator_username, [new_follower_username]):

					if ("%s@topics.%s" % (channel, domain_url)) in expected_results[True]:
						classified['SUCCESS'].append("%s@topics.%s" % (channel, domain_url))
					else:
						classified['FAIL'].append("%s@topics.%s" % (channel, domain_url))

				else:	
					if ("%s@topics.%s" % (channel, domain_url)) in expected_results[False]:
						classified['SUCCESS'].append("%s@topics.%s" % (channel, domain_url))
					else:
						classified['FAIL'].append("%s@topics.%s" % (channel, domain_url))

			else:
				classified['PROBLEM_SUBSCRIBING'].append("%s@topics.%s" % (channel, domain_url))

	else:
		classified['PROBLEM_CREATING'].append("%s@%s" % (new_follower_username, domain_url))


	moderator_username = "<strong>%s@%s</strong>" % (moderator_username, domain_url)

	if ( len(classified.get('PROBLEM_CREATING', [])) > 0 ):

		status = 2
		briefing = "This test failed because we could not create test user channel <strong>%s</strong>." % classified['PROBLEM_CREATING'][0]
		message += briefing + "<br/>We need that user for testing purposes.<br/><br/>It seems like your HTTP API is problematic."
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
		message += "<br/><br/>Thus, we could not test if %s can approve new followers." % moderator_username
		return (status, briefing, message, None)

	status = 0
	briefing = ""
	message = ""

	if ( len(classified.get('FAIL', [])) > 0 ):

		status = 1
		briefing = "Problems with following channels: <strong>%s</strong>" % string.join(classified['FAIL'], " | ")

		should_have_permission = sets.Set(expected_results[True])
		should_not_have_permission = sets.Set(expected_results[False])
		had_problems = sets.Set(classified['FAIL'])

		should_have_permission_but_didnt = should_have_permission.intersection(had_problems)
		should_not_have_permission_but_did = should_not_have_permission.intersection(had_problems)

		if ( len(should_have_permission_but_didnt) > 0 ):

			message = "User %s could not approve subscription requests to the "
			message += "following channels (<em>it should be able to!</em>): "
			message = message % (moderator_username)
			message += "<br/><br/><strong>%s</strong><br/>" % string.join(should_have_permission_but_didnt, "<br/>")


		if ( len(should_not_have_permission_but_did) > 0 ):

			if ( message != "" ):
				message += "<br/>"

			message += "User %s could approve subscription requests to the "
			message += "following channels (<em>it should not be able to!</em>): "
			message = message % (moderator_username)
			message += "<br/><br/><strong>%s</strong><br/>" % string.join(should_not_have_permission_but_did, "<br/>")

	if ( len(classified.get('SUCCESS', [])) > 0 ):

		if ( briefing == "" ):
			briefing += "User %s has correct approve subscription permissions!" % moderator_username

		should_have_permission = sets.Set(expected_results[True])
		should_not_have_permission = sets.Set(expected_results[False])
		had_no_problems = sets.Set(classified['SUCCESS'])

		should_have_permission_and_did = should_have_permission.intersection(had_no_problems)
		should_not_have_permission_and_didnt = should_not_have_permission.intersection(had_no_problems)

		if ( len(should_have_permission_and_did) > 0 ):

			if ( message != "" ):
				message += "<br/>"

			message += "User %s could approve subscription requests to the "
			message += "following channels (<em>as expected!</em>): "
			message = message % (moderator_username)
			message += "<br/><br/><strong>%s</strong><br/>" % string.join(should_have_permission_and_did, "<br/>")

		if ( len(should_not_have_permission_and_didnt) > 0 ):

			if ( message != "" ):
				message += "<br/>"

			message += "User %s could not approve subscription requests to the "
			message += "following channels (<em>as expected!</em>): "
			message = message % (moderator_username)
			message += "<br/><br/><strong>%s</strong><br/>" % string.join(should_not_have_permission_and_didnt, "<br/>")

	return (status, briefing, message, None)
