import string
from api_utils import change_topic_channel_subscriber_role, has_subscriber_role_in_topic_channel, change_another_user_channel_subscriber_role, has_subscriber_role_in_user_channel
from find_api_location import findAPILocation
from names_persistence_utils import obtainActualName

def change_role_permission(session, api_location, target_channel_name, tested_username, new_follower_username, subscription):

	topic_channel = "topics." in target_channel_name.split("@")[1]
	channel_name = obtainActualName(session, target_channel_name.split("@")[0])
	domain = target_channel_name.split("@")[1].replace("topics.", "")

	if tested_username != None:
		tested_username = obtainActualName(session, tested_username)

	new_follower_username = obtainActualName(session, new_follower_username)

	if ( not topic_channel ):

		if ( change_another_user_channel_subscriber_role(session, domain, api_location, channel_name, new_follower_username, tested_username, subscription) ):

			if ( has_subscriber_role_in_user_channel(session, domain, api_location, new_follower_username, channel_name, subscription) ):

				return True

			else:

				return False

		else:
			
			return False

	else:

		if ( change_topic_channel_subscriber_role(session, domain, api_location, tested_username, new_follower_username, channel_name, subscription) ):

			if ( has_subscriber_role_in_topic_channel(session, domain, api_location, new_follower_username, channel_name, subscription) ):

				return True

			else:

				return False

		else:

			return False

def change_to_moderator_permission(session, api_location, target_channel_name, tested_username, new_follower_username):

	return change_role_permission(session, api_location, target_channel_name, tested_username, new_follower_username, "moderator")

def change_to_follower_post_permission(session, api_location, target_channel_name, tested_username, new_follower_username):

	return change_role_permission(session, api_location, target_channel_name, tested_username, new_follower_username, "publisher")

def change_to_follower_permission(session, api_location, target_channel_name, tested_username, new_follower_username):

	return change_role_permission(session, api_location, target_channel_name, tested_username, new_follower_username, "member")

def change_to_banned_permission(session, api_location, target_channel_name, tested_username, new_follower_username):

	return change_role_permission(session, api_location, target_channel_name, tested_username, new_follower_username, "outcast")

ROLE_CHANGE_PERMISSION_TESTS = {
	'CHANGE_TO_MODERATOR'		: (change_to_moderator_permission, "Permission to promote to moderator" ),
	'CHANGE_TO_FOLLOWER_POST'	: (change_to_follower_post_permission, "Permission to promote to follower+post" ),
	'CHANGE_TO_FOLLOWER'		: (change_to_follower_permission, "Permission to promote to follower" ),
	'CHANGE_TO_BANNED'		: (change_to_banned_permission, "Permission to ban" )
}

def performRoleChangePermissionChecks(domain_url, session, tested_username, expected_results):

	(sts, bri, mes, api_location) = findAPILocation(domain_url)
	if ( sts != 0 ):
		return (sts, mes)

	if ( tested_username != None ):
		new_follower_username = tested_username + "_new_follower"
	else:
		new_follower_username = "test_user_channel_anonymous_new_follower"

	actual_results_match_expected_results = {}
	status = 0

	for test in expected_results.keys():

		if not test in ROLE_CHANGE_PERMISSION_TESTS:
			continue

		if not test in actual_results_match_expected_results:
			actual_results_match_expected_results[test] = { True : [], False : [] }

		for target_channel_name in expected_results[test].get(True, []):

			if ROLE_CHANGE_PERMISSION_TESTS[test][0](session, api_location, target_channel_name, tested_username, new_follower_username):
				veredict = "%s (%s)" % (target_channel_name, "had permission, as expected")
				actual_results_match_expected_results[test][True].append(veredict)
			else:
				veredict = "%s (%s)" % (target_channel_name, "should have permission")
				actual_results_match_expected_results[test][False].append(veredict)
				status = 1

		for target_channel_name in expected_results[test].get(False, []):

			if ROLE_CHANGE_PERMISSION_TESTS[test][0](session, api_location, target_channel_name, tested_username, new_follower_username):
				veredict = "%s (%s)" % (target_channel_name, "should not have permission")
				actual_results_match_expected_results[test][False].append(veredict)
				status = 1
			else:
				veredict = "%s (%s)" % (target_channel_name, "didn't have permission, as expected")
				actual_results_match_expected_results[test][True].append(veredict)

	if status == 0:
		partial_report = "<br/>Every role change permission test had the expected results!<br/>"
	else:
		partial_report = "<br/>Not all role change permission tests had the expected results!<br/>"

	for test in actual_results_match_expected_results.keys():

		if len(actual_results_match_expected_results[test][(status == 0)]) == 0:
			continue

		partial_report += "<br/><em>%s</em>:<br/><strong>%s</strong>" % (ROLE_CHANGE_PERMISSION_TESTS[test][1],
				string.join(actual_results_match_expected_results[test][(status == 0)], "<br/>"))

	if (status != 0):

		correct_results = ""

		for test in actual_results_match_expected_results.keys():

			if len(actual_results_match_expected_results[test][(status != 0)]) == 0:
				continue

			correct_results += "<br/><em>%s</em>:<br/><strong>%s</strong>" % (ROLE_CHANGE_PERMISSION_TESTS[test][1],
					string.join(actual_results_match_expected_results[test][(status != 0)], "<br/>"))

		if correct_results != "":

			partial_report += "<br/><br/><span class='muted'>The following role change permission tests were successful:<br/>"
			partial_report += correct_results + "</span>"

	return (status, partial_report)
