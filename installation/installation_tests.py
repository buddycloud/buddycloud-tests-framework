from importlib import import_module
import os, sys
os.chdir("installation")
sys.path.append("tests")


config = open("installation_tests.cfg")
test_entries = []
test_names = {}

test_counter = 0

for test_name in config.xreadlines():

	test_name = test_name.strip()
	if test_name.startswith("#"):
		continue

	problem_loading = False
	test_reference = None
	test_reference = import_module(test_name)
	test_reference = test_reference.getTestReference()
	try:
		test_reference = import_module(test_name).getTestReference()
	except ImportError:
		print "Could not import test "+test_name+"!"
		print "Test "+test_name+" does not exist. Ignoring this test..."
		problem_loading = True
	except Exception, e:
		print "Problem: "+str(e)
		print "Error: "+test_name+" could not be loaded. Ignoring this test..."
		problem_loading = True

	if problem_loading or test_reference == None:
		continue

	test_entries.append(test_reference.jsonfy())
	test_names[test_name] = test_counter
	test_counter += 1

config.close()
os.chdir("../")
