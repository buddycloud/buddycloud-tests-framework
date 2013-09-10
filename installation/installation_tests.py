from importlib import import_module
import os, sys
os.chdir("installation")
sys.path.insert(0, "tests")

import logging
logger = logging.getLogger(__name__)

class InstallationTest:

	def __init__(self, name, function):

		self.name = name
		self.function = function
		self.source = "github.com/buddycloud/buddycloud-tests-framework/blob/master/installation/tests/" + name + ".py"

	def jsonfy(self):

		json = { 'name' : self.name,
			 'test' : self.function,
			 'continue_if_fail' : True,
			 'source' : self.source
		}
		return json


test_entries = []
config = open("installation_tests.cfg")

for test_name in config.xreadlines():

	test_name = test_name.strip().replace(".py", "")
	if test_name.startswith("#"):
		continue

	problem_loading = False
	test_reference = None
	try:
		test_reference = getattr(import_module(test_name), "testFunction")
		test_reference = InstallationTest(test_name, test_reference)
	except ImportError:
		logger.info("~could not import test "+test_name+"!~")
		logger.info("~the test "+test_name+" doesn't exist~")
		logger.info("~ignoring this test "+test_name+"~")
		problem_loading = True
	except Exception as e:
		logger.info("~could not import test "+test_name+"!~")
		logger.info("~problem: "+str(e)+"~")
		logger.info("~ignoring this test "+test_name+"~")
		problem_loading = True

	if problem_loading or test_reference == None:
		continue

	test_entries.append(test_reference.jsonfy())


config.close()
os.chdir("../")

del config
