import string, json
from api_utils import prepare_and_send_request, user_channel_exists
from names_persistence_utils import obtainActualName


#HTTP_API endpoint: /:channel/content/status
def add_new_status_and_check(session, api_location, username, target_channel_name):

	target_username = obtainActualName(session, target_channel_name.split("@")[0])
	domain_url =  target_channel_name.split("@")[1]
	target_channel_name = "%s@%s" % (target_username, domain_url)

	new_mood = "I'm sad that Lost is over."

	data = {
		"content" : new_mood
	}

	if username != None:

		username = obtainActualName(session, username)

		(status, response) = prepare_and_send_request('POST', "%s%s/content/status" % (api_location,
			target_channel_name), payload=data, authorization=username)
	else:

		(status, response) = prepare_and_send_request('POST', "%s%s/content/status" % (api_location,
			target_channel_name), payload=data)

	if status:

		try:
			response = json.loads(response.content)
			
			new_mood_id = response['id']
			new_mood_author = response['author']
			current_mood = response['content']

			if ( new_mood_author != "%s@%s" % (username, domain_url.replace("topics.", "")) or current_mood != new_mood ):

				return False

			if username != None:

				(status, response) = prepare_and_send_request('GET', "%s%s/content/status/%s" % (api_location,
					target_channel_name, new_mood_id), authorization=username)
			else:
				
				(status, response) = prepare_and_send_request('GET', "%s%s/content/status/%s" % (api_location,
					target_channel_name, new_mood_id))

			if status:

				try:

					response = json.loads(response.content)
					return ( new_mood_id == response['id']
					and new_mood_author == response['author']
					and current_mood == response['content'] )

				except ValueError:
					pass

		except ValueError:
			pass

	return False


STATUS_MANAGEMENT_TESTS = {
	'ADD_NEW_STATUS_AND_CHECK' : ( add_new_status_and_check, "Permission to change status" )
}

def performStatusManagementTests(session, domain_url, api_location, username, expected_results):

	if username != None:

		if not user_channel_exists(session, domain_url, api_location, username):

			status = 1
			message = "Status management tests skipped because %s does not exist." % username
			return (status, message)

	actual_results_match_expected_results = {}
	status = 0

	for test in expected_results.keys():

		if not test in STATUS_MANAGEMENT_TESTS:
			continue

		if not test in actual_results_match_expected_results:
			actual_results_match_expected_results[test] = { True : [], False : [] }

		for target_channel_name in expected_results[test].get(True, []):

			if STATUS_MANAGEMENT_TESTS[test][0](session, api_location, username, target_channel_name):
				veredict = "%s (%s)" % (target_channel_name, "could perform operation, as expected")
				actual_results_match_expected_results[test][True].append(veredict)
			else:
				veredict = "%s (%s)" % (target_channel_name, "should have permission to perform operation")
				actual_results_match_expected_results[test][False].append(veredict)
				status = 1

		for target_channel_name in expected_results[test].get(False, []):

			if STATUS_MANAGEMENT_TESTS[test][0](session, api_location, username, target_channel_name):
				veredict = "%s (%s)" % (target_channel_name, "should not have permission to perform operation")
				actual_results_match_expected_results[test][False].append(veredict)
				status = 1
			else:
				veredict = "%s (%s)" % (target_channel_name, "could not perform operation, as expected")
				actual_results_match_expected_results[test][True].append(veredict)

	if status == 0:
		partial_report = "<br/>Every status management test had the expected results!<br/>"
	else:
		partial_report = "<br/>Not all status management tests had the expected results!<br/>"

	for test in actual_results_match_expected_results.keys():

		if len(actual_results_match_expected_results[test][(status == 0)]) == 0:
			continue

		partial_report += "<br/><em>%s</em>:<br/><strong>%s</strong>" % (STATUS_MANAGEMENT_TESTS[test][1],
				string.join(actual_results_match_expected_results[test][(status == 0)], "<br/>"))

	if (status != 0):

		correct_results = ""

		for test in actual_results_match_expected_results.keys():

			if len(actual_results_match_expected_results[test][(status != 0)]) == 0:
				continue

			correct_results += "<br/><em>%s</em>:<br/><strong>%s</strong>" % (STATUS_MANAGEMENT_TESTS[test][1],
					string.join(actual_results_match_expected_results[test][(status != 0)], "<br/>"))

		if correct_results != "":

			partial_report += "<br/><br/><span class='muted'>The following status management tests were successful:<br/>"
			partial_report += correct_results + "</span>"

	return (status, partial_report)
