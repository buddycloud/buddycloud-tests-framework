import os, json, time, random
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

def lookupAPI(domain_url):
	# Look at SRV record of the given domain if the service _buddycloud-api can be found!
	out = "executed lookupAPI test"
	err = "none"
	return "OUT: "+str(out)+", ERR: "+str(err)


def testExample(domain_url):
	# This is a temporary test example, does nothing but wait.
	waittime = random.randint(0,10)
	time.sleep(waittime)
	return "OUT: waited"+str(waittime)


#Test entries: tests to be performed by the inspector, each have a name and a function
test_entries = {}
test_entries['lookupAPI'] = lookupAPI
test_entries['testExample1'] = testExample 
test_entries['testExample2'] = testExample 
test_entries['testExample3'] = testExample 
test_entries['testExample4'] = testExample 
test_entries['testExample5'] = testExample 
test_entries['testExample6'] = testExample 
test_entries['testExample7'] = testExample 
test_entries['testExample8'] = testExample 
test_entries['testExample9'] = testExample 
test_entries['testExample10'] = testExample 


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
	return json.dumps(entry_names)

@app.route('/perform_test/<test_name>/<domain_url>')
def perform_test(test_name=None, domain_url=None):

	json_return = { 'name' : test_name }

	if test_name == None or test_name.strip() == "" or test_name not in test_entries:
		json_return['output'] = "Invalid test name"
	else:
		test_output = test_entries[test_name](domain_url)
		json_return['output'] = test_output

	return json.dumps(json_return)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, debug=True)
