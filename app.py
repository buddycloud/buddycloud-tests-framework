import os
from flask import Flask, render_template, redirect, url_for, request
from multiprocessing import Process

app = Flask(__name__)

def lookupAPI():
	return "LOOKUP API OK"

#Test entries: tests to be performed by the inspector, each have a name and a function
test_entries = {}
test_entries['lookupAPI'] = lookupAPI


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/test_names', methods=['GET'])
def get_test_names():
	entry_names = {}
	entry_names['entries'] = []
	for entry in test_entries:
		entry_names['entries'].append({
			'name' : entry
		})
	return entry_names

@app.route('/perform_test/<test_name>')
def perform_test(test_name=None):

	json_return = { 'name' : test_name }

	if test_name == None or test_name.strip() == "" or test_name not in test_entries:
		json_return['output'] = "Invalid test name"
	else:
		test_output = test_entries[test_name]()
		json_return['output'] = test_output

	return json_return

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, debug=True)
