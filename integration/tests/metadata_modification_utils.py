import string, json
from api_utils import prepare_and_send_request, user_channel_exists
from names_persistence_utils import obtainActualName


#HTTP_API endpoint: /:channel/metadata/posts
def update_metadata_info(session, api_location, username, target_channel_name, metadata_field, metadata_value):

	target_channel_name = "%s@%s" % (obtainActualName(session, target_channel_name.split("@")[0]), target_channel_name.split("@")[1])
	
	if username != None:

		username = obtainActualName(session, username)

		(status, response) = prepare_and_send_request('GET', "%s%s/metadata/posts" % (api_location,
			target_channel_name), authorization=username)
	else:

		(status, response) = prepare_and_send_request('GET', "%s%s/metadata/posts" % (api_location,
			target_channel_name))

	if status:

		try:
			response = json.loads(response.content)

			if metadata_value.startswith("*"):
				metadata_value = response[metadata_field] + metadata_value.replace("*", "")
			else:
				metadata_value = metadata_value.replace("/", "").replace(response[metadata_field], "")
		except ValueError:
			pass

	data = { metadata_field : metadata_value }

	if username != None:

		(status, response) = prepare_and_send_request('POST', "%s%s/metadata/posts" % (api_location,
			target_channel_name), payload=data, authorization=username)
	else:

		(status, response) = prepare_and_send_request('POST', "%s%s/metadata/posts" % (api_location,
			target_channel_name), payload=data)

	if status:

		if username != None:

			(status, response) = prepare_and_send_request('GET', "%s%s/metadata/posts" % (api_location,
				target_channel_name), authorization=username)
		else:

			(status, response) = prepare_and_send_request('GET', "%s%s/metadata/posts" % (api_location,
				target_channel_name))			

		if status:

			try:
				response = json.loads(response.content)
				return response[metadata_field] == metadata_value
			except ValueError:
				pass
	return False

#HTTP_API endpoint: /:channel/metadata/posts
def update_channel_title(session, api_location, username, target_channel_name):
	return update_metadata_info(session, api_location, username, target_channel_name, metadata_field="title", metadata_value="* (Updated)")

#HTTP_API endpoint: /:channel/metadata/posts
def update_channel_description(session, api_location, username, target_channel_name):
	return update_metadata_info(session, api_location, username, target_channel_name, metadata_field="description", metadata_value="* (Updated)")

#HTTP_API endpoint: /:channel/metadata/posts
def update_channel_access_model(session, api_location, username, target_channel_name):
	return update_metadata_info(session, api_location, username, target_channel_name, metadata_field="access_model", metadata_value="open/authorize")

#HTTP_API endpoint: /:channel/metadata/posts
def update_channel_creation_date(session, api_location, username, target_channel_name):
	return update_metadata_info(session, api_location, username, target_channel_name, metadata_field="creation_date", metadata_value="* (Updated)")

#HTTP_API endpoint: /:channel/metadata/posts
def update_channel_type(session, api_location, username, target_channel_name):
	return update_metadata_info(session, api_location, username, target_channel_name, metadata_field="channel_type", metadata_value="personal/topic")

#HTTP_API endpoint: /:channel/metadata/posts
def update_channel_default_affiliation(session, api_location, username, target_channel_name):
	return update_metadata_info(session, api_location, username, target_channel_name, metadata_field="default_affiliation", metadata_value="member/publisher")


METADATA_MODIFICATION_TESTS = {
	'UPDATE_TITLE'	 		: ( update_channel_title, "Change permission to channel title metadata" ),
	'UPDATE_DESCRIPTION' 		: ( update_channel_description, "Change permission to channel description metadata" ),
	'UPDATE_ACCESS_MODEL'		: ( update_channel_access_model, "Change permission to channel access model metadata" ),
	'UPDATE_CREATION_DATE'		: ( update_channel_creation_date, "Change permission to channel creation date metadata" ),
	'UPDATE_CHANNEL_TYPE'		: ( update_channel_type, "Change permission to channel type metadata" ),
	'UPDATE_DEFAULT_AFFILIATION'	: ( update_channel_default_affiliation, "Change permission to channel default affiliation metadata" )
}

def performMetadataModificationTests(session, domain_url, api_location, username, expected_results):

	if username != None:

		if not user_channel_exists(session, domain_url, api_location, username):

			status = 1
			message = "Metadata modification tests skipped because %s does not exist." % username
			return (status, message)

	actual_results_match_expected_results = {}
	status = 0

	for test in expected_results.keys():

		if not test in METADATA_MODIFICATION_TESTS:
			continue

		if not test in actual_results_match_expected_results:
			actual_results_match_expected_results[test] = { True : [], False : [] }

		for target_channel_name in expected_results[test].get(True, []):

			if METADATA_MODIFICATION_TESTS[test][0](session, api_location, username, target_channel_name):
				veredict = "%s (%s)" % (target_channel_name, "had change permission, as expected")
				actual_results_match_expected_results[test][True].append(veredict)
			else:
				veredict = "%s (%s)" % (target_channel_name, "should have change permission")
				actual_results_match_expected_results[test][False].append(veredict)
				status = 1

		for target_channel_name in expected_results[test].get(False, []):

			if METADATA_MODIFICATION_TESTS[test][0](session, api_location, username, target_channel_name):
				veredict = "%s (%s)" % (target_channel_name, "should not have change permission")
				actual_results_match_expected_results[test][False].append(veredict)
				status = 1
			else:
				veredict = "%s (%s)" % (target_channel_name, "didn't have change permission, as expected")
				actual_results_match_expected_results[test][True].append(veredict)

	if status == 0:
		partial_report = "<br/>Every metadata modification test had the expected results!<br/>"
	else:
		partial_report = "<br/>Not all metadata modification tests had the expected results!<br/>"

	for test in actual_results_match_expected_results.keys():

		if len(actual_results_match_expected_results[test][(status == 0)]) == 0:
			continue

		partial_report += "<br/><em>%s</em>:<br/><strong>%s</strong>" % (METADATA_MODIFICATION_TESTS[test][1],
				string.join(actual_results_match_expected_results[test][(status == 0)], "<br/>"))

	if (status != 0):

		correct_results = ""

		for test in actual_results_match_expected_results.keys():

			if len(actual_results_match_expected_results[test][(status != 0)]) == 0:
				continue

			correct_results += "<br/><em>%s</em>:<br/><strong>%s</strong>" % (METADATA_MODIFICATION_TESTS[test][1],
					string.join(actual_results_match_expected_results[test][(status != 0)], "<br/>"))

		if correct_results != "":

			partial_report += "<br/><br/><span class='muted'>The following metadata modification tests were successful:<br/>"
			partial_report += correct_results + "</span>"

	return (status, partial_report)
