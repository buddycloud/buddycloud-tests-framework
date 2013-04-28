import os, json
from flask import Flask, render_template, redirect, url_for, request, make_response
from tests import test_entries, test_names

app = Flask(__name__)

@app.route('/')
def index():
	
	return render_template("index.html", domain_url=None)


@app.route('/test_names', methods=['GET'])
def get_test_names():
	
	entries = []
	for entry in test_entries:
		entries.append({
			'name' : entry['name'],
			'continue_if_fail' : entry['continue_if_fail']
		})
	return json.dumps(entries)

@app.route('/perform_test/<test_name>/<path:domain_url>')
def perform_test(test_name=None, domain_url=None):

	json_return = { 'name' : test_name }

	if test_name == None or test_name.strip() == "" or test_name not in test_names:
		(exit_status, test_output) = 2, "Invalid test name"
		json_return['exit_status'] = exit_status
		json_return['output'] = test_output
	else:
		(exit_status, test_output) = test_entries[test_names[test_name]]['test'](domain_url)
		json_return['exit_status'] = exit_status
		json_return['output'] = test_output
	return json.dumps(json_return)

@app.route('/<path:domain_url>')
def start_tests_launcher(domain_url=None):

	resp = make_response(render_template("index.html", domain_url=domain_url))
	resp.headers['content-type'] = "text/html"
	resp.mimetype = 'text/html'
	return resp

if __name__ == "__main__":
	
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, debug=True)
