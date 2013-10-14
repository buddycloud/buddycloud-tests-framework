import string, json
from api_utils import prepare_and_send_request, user_channel_exists
from names_persistence_utils import obtainActualName


#HTTP_API endpoint: /:channel/content/posts
def add_new_post_and_get_by_id_direct_access(api_location, username, target_channel_name):

	target_username = obtainActualName(target_channel_name.split("@")[0])
	domain_url =  target_channel_name.split("@")[1]
	target_channel_name = "%s@%s" % (target_username, domain_url)

	content_posted = "'You all everybody' by Drive Shaft is the best song ever."

	data = {
		"content" : content_posted
	}

	if username != None:

		username = obtainActualName(username)

		(status, response) = prepare_and_send_request('POST', "%s%s/content/posts" % (api_location,
			target_channel_name), payload=data, authorization=username)
	else:

		(status, response) = prepare_and_send_request('POST', "%s%s/content/posts" % (api_location,
			target_channel_name), payload=data)

	if status:

		try:
			response = json.loads(response.content)
			
			post_id = response['id']
			post_author = response['author']
			content_obtained = response['content']

			if ( post_author != "%s@%s" % (username, domain_url.replace("topics.", "")) or content_obtained != content_posted ):

				return False

			if username != None:

				(status, response) = prepare_and_send_request('GET', "%s%s/content/posts/%s" % (api_location,
					target_channel_name, post_id), authorization=username)
			else:
				
				(status, response) = prepare_and_send_request('GET', "%s%s/content/posts/%s" % (api_location,
					target_channel_name, post_id))

			if status:

				try:

					response = json.loads(response.content)
					return ( post_id == response['id']
					and post_author == response['author']
					and content_obtained == response['content'] )

				except ValueError:
					pass

		except ValueError:
			pass

	return False

#HTTP_API endpoint: /:channel/content/posts
def add_new_post_and_get_by_matching_id(api_location, username, target_channel_name):

	target_username = obtainActualName(target_channel_name.split("@")[0])
	domain_url =  target_channel_name.split("@")[1]
	target_channel_name = "%s@%s" % (target_username, domain_url)

	content_posted = "'Don't tell me what I can't do' is a frequently spoken phrase on Lost."

	data = {
		"content" : content_posted
	}

	if username != None:

		username = obtainActualName(username)

		(status, response) = prepare_and_send_request('POST', "%s%s/content/posts" % (api_location,
			target_channel_name), payload=data, authorization=username)
	else:

		(status, response) = prepare_and_send_request('POST', "%s%s/content/posts" % (api_location,
			target_channel_name), payload=data)

	if status:

		try:
			response = json.loads(response.content)
			
			post_id = response['id']
			post_author = response['author']
			content_obtained = response['content']

			if ( post_author != "%s@%s" % (username, domain_url.replace("topics.", "")) or content_obtained != content_posted ):

				return False

			if username != None:

				(status, response) = prepare_and_send_request('GET', "%s%s/content/posts" % (api_location,
					target_channel_name), authorization=username)
			else:
				
				(status, response) = prepare_and_send_request('GET', "%s%s/content/posts" % (api_location,
					target_channel_name))

			if status:

				try:

					response = json.loads(response.content)
					
					for item in response:

						if ( item['id'] == post_id
						and  item['author'] == post_author
						and  item['content'] == content_obtained ):

							return True

				except ValueError:
					pass

		except ValueError:
			pass

	return False

#HTTP_API endpoint: /:channel/content/posts
def remove_own_post(api_location, username, target_channel_name):

	target_username = obtainActualName(target_channel_name.split("@")[0])
	domain_url =  target_channel_name.split("@")[1]
	target_channel_name = "%s@%s" % (target_username, domain_url)

	content_posted = "The Lost finale was pretty bad."

	data = {
		"content" : content_posted
	}

	if username != None:

		username = obtainActualName(username)

		(status, response) = prepare_and_send_request('POST', "%s%s/content/posts" % (api_location,
			target_channel_name), payload=data, authorization=username)
	else:

		(status, response) = prepare_and_send_request('POST', "%s%s/content/posts" % (api_location,
			target_channel_name), payload=data)

	if status:

		try:
			response = json.loads(response.content)
			
			post_id = response['id']
			post_author = response['author']
			content_obtained = response['content']

			if ( post_author != "%s@%s" % (username, domain_url.replace("topics.", "")) or content_obtained != content_posted ):

				return False

			if username != None:

				(status, response) = prepare_and_send_request('DELETE', "%s%s/content/posts/%s" % (api_location,
					target_channel_name, post_id), authorization=username)
			else:
				
				(status, response) = prepare_and_send_request('DELETE', "%s%s/content/posts/%s" % (api_location,
					target_channel_name, post_id))

			return status

		except ValueError:
			pass

	return False

#HTTP_API endpoint: /:channel/content/posts
def remove_post_created_by_owner(api_location, username, target_channel_name):

	target_username = obtainActualName(target_channel_name.split("@")[0])
	domain_url =  target_channel_name.split("@")[1]
	target_channel_name = "%s@%s" % (target_username, domain_url)

	if ( 'open' in target_username ):
		owner_username = 'test_user_channel_open'
	else:
		owner_username = 'test_user_channel_authorized'

	owner_username = obtainActualName(owner_username)

	content_posted = "By the way, what happened to Waaaaaalt?"

	data = {
		"content" : content_posted
	}

	(status, response) = prepare_and_send_request('POST', "%s%s/content/posts" % (api_location,
			target_channel_name), payload=data, authorization=owner_username)

	if status:

		try:
			response = json.loads(response.content)
			
			post_id = response['id']
			post_author = response['author']
			content_obtained = response['content']

			if ( post_author != "%s@%s" % (owner_username, domain_url.replace("topics.", "")) or content_obtained != content_posted ):

				return False

			if username != None:

				username = obtainActualName(username)
		
				(status, response) = prepare_and_send_request('DELETE', "%s%s/content/posts/%s" % (api_location,
					target_channel_name, post_id), authorization=username)
			else:
				
				(status, response) = prepare_and_send_request('DELETE', "%s%s/content/posts/%s" % (api_location,
					target_channel_name, post_id))

			return status

		except ValueError:
			pass

	return False

#HTTP_API endpoint: /:channel/content/posts
def remove_post_created_by_moderator(api_location, username, target_channel_name):

	target_username = obtainActualName(target_channel_name.split("@")[0])
	domain_url =  target_channel_name.split("@")[1]
	target_channel_name = "%s@%s" % (target_username, domain_url)

	owner_username = 'test_user_channel_follower1'
	owner_username = obtainActualName(owner_username)

	content_posted = "By the way, what happened to Waaaaaalt?"

	data = {
		"content" : content_posted
	}

	(status, response) = prepare_and_send_request('POST', "%s%s/content/posts" % (api_location,
			target_channel_name), payload=data, authorization=owner_username)

	if status:

		try:
			response = json.loads(response.content)
			
			post_id = response['id']
			post_author = response['author']
			content_obtained = response['content']

			if ( post_author != "%s@%s" % (owner_username, domain_url.replace("topics.", "")) or content_obtained != content_posted ):

				return False

			if username != None:

				username = obtainActualName(username)
		
				(status, response) = prepare_and_send_request('DELETE', "%s%s/content/posts/%s" % (api_location,
					target_channel_name, post_id), authorization=username)
			else:
				
				(status, response) = prepare_and_send_request('DELETE', "%s%s/content/posts/%s" % (api_location,
					target_channel_name, post_id))

			return status

		except ValueError:
			pass

	return False

POSTS_MANAGEMENT_TESTS = {
	'ADD_NEW_POST_AND_GET_BY_ID_DIRECT_ACCESS' : ( add_new_post_and_get_by_id_direct_access, "Permission to add new post (so that it's readable using id)" ),
	'ADD_NEW_POST_AND_GET_BY_MATCHING_ID'      : ( add_new_post_and_get_by_matching_id, "Permission to add new post (so that it's shown among all posts)" ),
	'REMOVE_OWN_POST'			   : ( remove_own_post, "Permission to remove posts created by itself" ),
	'REMOVE_POST_CREATED_BY_OWNER'		   : ( remove_post_created_by_owner, "Permission to remove posts created by the channel owner" ),
	'REMOVE_POST_CREATED_BY_MODERATOR'	   : ( remove_post_created_by_moderator, "Permission to remove posts created by a channel moderator" )	
}

def performPostsManagementTests(domain_url, api_location, username, expected_results):

	if username != None:

		if not user_channel_exists(domain_url, api_location, username):

			status = 1
			message = "Posts management tests skipped because %s does not exist." % username
			return (status, message)

	actual_results_match_expected_results = {}
	status = 0

	for test in expected_results.keys():

		if not test in POSTS_MANAGEMENT_TESTS:
			continue

		if not test in actual_results_match_expected_results:
			actual_results_match_expected_results[test] = { True : [], False : [] }

		for target_channel_name in expected_results[test].get(True, []):

			if POSTS_MANAGEMENT_TESTS[test][0](api_location, username, target_channel_name):
				veredict = "%s (%s)" % (target_channel_name, "could perform operation, as expected")
				actual_results_match_expected_results[test][True].append(veredict)
			else:
				veredict = "%s (%s)" % (target_channel_name, "should have permission to perform operation")
				actual_results_match_expected_results[test][False].append(veredict)
				status = 1

		for target_channel_name in expected_results[test].get(False, []):

			if POSTS_MANAGEMENT_TESTS[test][0](api_location, username, target_channel_name):
				veredict = "%s (%s)" % (target_channel_name, "should not have permission to perform operation")
				actual_results_match_expected_results[test][False].append(veredict)
				status = 1
			else:
				veredict = "%s (%s)" % (target_channel_name, "could not perform operation, as expected")
				actual_results_match_expected_results[test][True].append(veredict)

	if status == 0:
		partial_report = "<br/>Every posts management test had the expected results!<br/>"
	else:
		partial_report = "<br/>Not all posts management tests had the expected results!<br/>"

	for test in actual_results_match_expected_results.keys():

		if len(actual_results_match_expected_results[test][(status == 0)]) == 0:
			continue

		partial_report += "<br/><em>%s</em>:<br/><strong>%s</strong>" % (POSTS_MANAGEMENT_TESTS[test][1],
				string.join(actual_results_match_expected_results[test][(status == 0)], "<br/>"))

	if (status != 0):

		correct_results = ""

		for test in actual_results_match_expected_results.keys():

			if len(actual_results_match_expected_results[test][(status != 0)]) == 0:
				continue

			correct_results += "<br/><em>%s</em>:<br/><strong>%s</strong>" % (POSTS_MANAGEMENT_TESTS[test][1],
					string.join(actual_results_match_expected_results[test][(status != 0)], "<br/>"))

		if correct_results != "":

			partial_report += "<br/><br/><span class='muted'>The following posts management tests were successful:<br/>"
			partial_report += correct_results + "</span>"

	return (status, partial_report)
