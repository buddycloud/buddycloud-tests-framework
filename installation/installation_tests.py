from importlib import import_module
import os, sys
os.chdir("installation")
sys.path.insert(0, "tests")


test_entries = []
config = open("installation_tests.cfg")

for test_name in config.xreadlines():

	test_name = test_name.strip()
	if test_name.startswith("#"):
		continue

	problem_loading = False
	test_reference = None
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


config.close()
os.chdir("../")

del config
