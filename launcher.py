import os, sys, json
from flask import Flask, render_template, redirect, url_for, request, make_response

sys.path.append(os.path.join(os.getcwd(), "suite_utils"))

sys.path.append(os.path.join(os.getcwd(), "installation"))
from installation_tests import test_entries as installation_test_entries

sys.path.append(os.path.join(os.getcwd(), "integration"))
from integration_tests import test_entries as integration_test_entries

test_entries = installation_test_entries + integration_test_entries

test_names = {}
for i in range(len(test_entries)):
	test_names[test_entries[i]['name']] = i


server = Flask(__name__)

@server.route('/')
def index():
	
	return render_template("index.html", domain_url=None)


@server.route('/test_names', methods=['GET'])
def get_test_names():
	
	entries = []
	for entry in test_entries:

		entries.append({
			'name' : entry['name'],
			'continue_if_fail' : entry['continue_if_fail'],
			'source' : entry['source']
		})

	response = make_response(json.dumps(entries), 200)
	response.headers["Content-Type"] = "application/json"
	return response

@server.route('/perform_test/<test_name>/<path:domain_url>')
def perform_test(test_name=None, domain_url=None):

	print "~about to execute test "+test_name+"~"

	current_dir = os.getcwd()
	os.chdir("execution_context")

	print "\t~changed to execution context~"

	try:

		json_return = { 'name' : test_name }

		error_msg = None

		if test_name == None or test_name.strip() == "":
			
			error_msg = "Invalid test name. It cannot be null."
		
		elif test_name not in test_names:

			error_msg = "Invalid test name. There is no such test called "+test_name+"."

		if error_msg != None:

			print "\t~test doesn't exist~"

			(exit_status, briefing, message, results) = 2, "Invalid test name!", error_msg, None
			json_return['exit_status'] = exit_status
			json_return['briefing'] = briefing
			json_return['message'] = message

		else:
	
			error_msg = None

			test_output = test_entries[test_names[test_name]]['test'](domain_url)

			if ( not (isinstance(test_output, tuple) and len(test_output) == 4) ):
			
				error_msg = "Wrong return type; must be a tuple with exactly 4 elements!"
		
			elif ( not isinstance(test_output[0], int) ):
			
				error_msg = "Exit status must be an integer!"
			
			elif ( not isinstance(test_output[1], str) and not isinstance(test_output[1], unicode) ):
				
				error_msg = "Briefing must be a string!"
	
			elif ( not isinstance(test_output[2], str) and not isinstance(test_output[2], unicode) ):
				
				error_msg = "Message must be a string!"

			if error_msg != None:

				print "\t~test is malformed~"

				exit_status = 2
				briefing = "Malformed test! Reason: " + error_msg
				message = "This test failed because either it is malformed "
				message += "or because a test that this test reuses is malformed."
				message += " <br/>Reason: " + error_msg

				json_return['exit_status'] = exit_status
				json_return['briefing'] = briefing
				json_return['message'] = message

			else:

				print "\t~test performed successfully~"

				(exit_status, briefing, message, results) = test_output 
			
				json_return['exit_status'] = exit_status
				json_return['briefing'] = briefing
				json_return['message'] = message

		return json.dumps(json_return)

	except Exception, e:

		print "\t~test failed unexpectedly: "+str(e)+"~"
		
		json_return = { 'name' : test_name,
				'exit_status' : 1,
				'briefing' : "Unexpected exception raised!!",
				'message' : "This test failed pretty badly.<br/>It raised an unexpected exception: "+str(e)+"!</br>Please fix this problem before issuing this test again.",
				'output' : None
		}
		
		return json.dumps(json_return)

	finally:
		
		print "\t~leaving execution context~"
		os.chdir(current_dir)

@server.route('/<path:domain_url>')
def start_tests_server(domain_url=None):

	resp = make_response(render_template("index.html", domain_url=domain_url))
	resp.headers['content-type'] = "text/html"
	resp.mimetype = 'text/html'
	return resp

if __name__ == "__main__":
	
	port = int(os.environ.get("PORT", 5000))
	server.run(host="0.0.0.0", port=port, debug=True)
