import os, sys, json, string, linecache, re, random
from flask import Flask, render_template, redirect, url_for, request, make_response, Markup, session
from multiprocessing import Process, Manager

sys.path.append(os.path.join(os.getcwd(), "suite_utils"))

import logging
from log_utils import LogStream


log_stream = LogStream()
logging.basicConfig(level=logging.DEBUG, stream=log_stream)

def perform_tests(domain_url, run):

	sys.path.append(os.path.join(os.getcwd(), "suite_utils"))
	sys.path.append(os.path.join(os.getcwd(), "installation"))
	from installation_tests import test_entries as installation_test_entries
	sys.path.append(os.path.join(os.getcwd(), "integration"))
	from integration_tests import test_entries as integration_test_entries
	test_entries = installation_test_entries + integration_test_entries

	test_names = {}
	for i in range(len(test_entries)):
		test_names[test_entries[i]['name']] = i

	run['run_status'] = 1

	tests = []
	for test_entry in test_entries:

		tests.append({
			'name' : test_entry['name'],
			'test_run_status' : 0,
			'result' : None,
			'source' : test_entry['source']
		})

	run['tests'] = tests

	updated_tests = tests

	run_variables = {}

	for index_test_entry in range(len(test_entries)):

		updated_tests[index_test_entry]['test_run_status'] = 1
		run['tests'] = updated_tests

		response = perform_test(test_entries[index_test_entry]['name'], domain_url, test_names, test_entries, run_variables)

		updated_tests[index_test_entry]['test_run_status'] = 2
		updated_tests[index_test_entry]['result'] = response
		run['tests'] = updated_tests


	run['run_status'] = 2

server = Flask(__name__)
server.secret_key = os.urandom(24)

@server.route('/get_all_runs')
def get_all_runs():

	global runs

	dict_runs = {}

	for session_id in runs.keys():
		dict_runs[session_id] = dict(runs[session_id])

	response = make_response(json.dumps(dict_runs), 200)
	response.headers["Content-Type"] = "application/json"
	return response

@server.route('/is_running/<run_id>')
def is_running(run_id=None):

	if run_id in process_handlers:

		if process_handlers[run_id].is_alive():

			response = make_response(json.dumps({'veredict' : ("Test suite with run_id (%s) is still running." % run_id)}), 200)
			response.headers["Content-Type"] = "application/json"
			return response

		else:

			response = make_response(json.dumps({'veredict' : ("Test suite with run_id (%s) has finished." % run_id)}), 200)
			response.headers["Content-Type"] = "application/json"
			return response

	response = make_response(json.dumps({'veredict' : ("Test suite with run_id (%s) has finished executing and then removed or it never existed." % run_id)}), 200)
	response.headers["Content-Type"] = "application/json"
	return response			

@server.route('/active_session')
def active_session_exists():

	if 'run_id' in session:

		response = make_response(json.dumps({'active_session' : session['run_id'].split("_")[0]}), 200)
		response.headers["Content-Type"] = "application/json"

	else:

		response = make_response(json.dumps({'active_session' : None}), 410)
		response.headers["Content-Type"] = "application/json"
		response.headers["Cache-Control"] = "no-cache"

	return response

@server.route('/get_results')
def get_results():

	global runs

	if 'run_id' in session:

		response = make_response(json.dumps(dict(runs[session['run_id']])), 200)
		response.headers["Content-Type"] = "application/json"

	else:

		response = make_response(json.dumps({'active_session' : None}), 410)
		response.headers["Content-Type"] = "application/json"
		response.headers["Cache-Control"] = "no-cache"

	return response

@server.route('/stop_launcher')
def stop_launcher():

	if 'run_id' in session:

		#add checks to actually make sure that teardown tests have run before destroying the process
		#or issuing teardown processes only right after destroying the process
		#process_handlers[session['run_id']].terminate()
		#del runs[session['run_id']]
		session.pop('run_id')

	response = make_response("", 210)
	response.headers["Cache-Control"] = "no-cache"
	return response

@server.route('/launch/<path:domain_url>')
def launch_tester(domain_url=None):

	global runs
	
	if not 'run_id' in session:

		session['run_id'] = domain_url + "_" + str(random.random()).split(".")[1]


		manager = Manager()
		runs[session['run_id']] = manager.dict()
		runs[session['run_id']]['run_id'] = session['run_id']
		runs[session['run_id']]['run_status'] = 0
		runs[session['run_id']]['tests'] = {}

		p = Process(target=perform_tests, args=(domain_url, runs[session['run_id']],))

		process_handlers[session['run_id']] = p

		p.daemon = True
		p.start()

		response = make_response(json.dumps(dict(runs[session['run_id']])), 200)
		response.headers["Content-Type"] = "application/json"
		return response
	
	else:

		if ( runs[session['run_id']]['run_status'] == 2 ):

			session.pop('run_id')
			return launch_tester(domain_url)

		return get_results()

def perform_test(test_name, domain_url, test_names, test_entries, run_variables):

	logging.info("~about to execute test "+test_name+"~")

	current_dir = os.getcwd()
	os.chdir("execution_context")

	logging.info("~changed to execution context~")

	try:

		response = { 'name' : test_name }

		error_msg = None

		if test_name == None or test_name.strip() == "":
			
			error_msg = "Invalid test name. It cannot be null."
		
		elif test_name not in test_names:

			error_msg = "Invalid test name. There is no such test called "+test_name+"."

		if error_msg != None:

			logging.info("~the test "+test_name+" doesn't exist~")

			(exit_status, briefing, message, results) = 2, "Invalid test name!", error_msg, None
			response['exit_status'] = exit_status
			response['briefing'] = briefing
			response['message'] = message

		else:
	
			error_msg = None

			print log_stream.getContent()
			log_stream.reset()
			log_stream.setDelimiter("<br/>")

			test_output = None
			arguments = [ domain_url, run_variables ]
			regex = re.compile("^.*takes exactly [0-9]+ arguments? \([0-9]+ given\)")
			for i in range(len(arguments), 0, -1):
				try:
					test_output = test_entries[test_names[test_name]]['test'](*(arguments[:i]))
					break
				except TypeError:
					e_type, e_value, e_trace = sys.exc_info()
					if regex.match(str(e_value)) != None:
						continue
					else:
						raise

			log_stream.setDelimiter("\n")

			if ( test_output == None ):

				error_msg = "Test must receive 1 or 2 arguments!"

			elif ( not (isinstance(test_output, tuple) and len(test_output) == 4) ):
			
				error_msg = "Wrong return type; must be a tuple with exactly 4 elements!"
		
			elif ( not isinstance(test_output[0], int) ):
			
				error_msg = "Exit status must be an integer!"
			
			elif ( not isinstance(test_output[1], str) and not isinstance(test_output[1], unicode) ):
				
				error_msg = "Briefing must be a string!"
	
			elif ( not isinstance(test_output[2], str) and not isinstance(test_output[2], unicode) ):
				
				error_msg = "Message must be a string!"

			if error_msg != None:

				exit_status = 2
				briefing = "Malformed test! Reason: " + error_msg
				message = "This test failed because either it is malformed "
				message += "or because a test that this test reuses is malformed."
				message += " <br/>Reason: " + error_msg

				response['exit_status'] = exit_status
				response['briefing'] = briefing
				response['message'] = message

				logging.info("~the test "+test_name+" is malformed~")

			else:

				(exit_status, briefing, message, results) = test_output 
			
				response['exit_status'] = exit_status
				response['briefing'] = briefing

				if ( log_stream.getContent() != "" ):
					message += "<br/><br><strong>Test Log:</strong><br/>"
					logged_content = map(lambda x: Markup.escape(x).__str__(),
							log_stream.getContent().split("<br/>"))
					message += "<small>%s</small>" % string.join(logged_content, "<br/>")

				response['message'] = message

				logging.info("~the test "+test_name+" performed successfully~")

		return response

	except Exception as e:

		e_type, e_value, e_trace = sys.exc_info()
		e_type = Markup.escape(str(type(e))).__str__()
		filename = e_trace.tb_frame.f_code.co_filename
		line_no = e_trace.tb_lineno
		line_content = linecache.getline(filename, line_no)
		exception_info = "<strong>%s<br/>\"%s\"</strong><br/>" % (e_type, e_value)
		#at <em>%s</em>:<em>%d</em>: <small>\"%s\"</small>" % (e_type, e_value, filename, line_no, line_content)
		
		#TODO get correct filename, file_no and file_content, maybe have it propagate all the way through the framework layers"

		logging.info("~the test "+test_name+" failed unexpectedly: "+exception_info+"~")

		message = "This test failed pretty badly.<br/>It raised an unexpected exception:<br/><br/>"+exception_info+"<br/>"
		message += "</br>Please fix this problem before issuing this test again."

		response = { 'name' : test_name,
				'exit_status' : 1,
				'briefing' : "Unexpected exception raised!!",
				'message' : message,
				'output' : None
		}

		return response

	finally:
		
		logging.info("~leaving execution context~")
		os.chdir(current_dir)

@server.route('/')
def index():
	
	return render_template("index.html", domain_url=None)

@server.route('/<path:domain_url>')
def start_tests_server(domain_url=None):

	resp = make_response(render_template("index.html", domain_url=domain_url))
	resp.headers['content-type'] = "text/html"
	resp.mimetype = 'text/html'
	return resp

if __name__ == "__main__":

	runs = {}
	process_handlers = {}

	port = int(os.environ.get("PORT", 5000))

	logging.info("~about to start protocol server~")

	server.run(host="0.0.0.0", port=port, debug=True)
