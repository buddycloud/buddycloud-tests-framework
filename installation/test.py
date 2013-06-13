class InstallationTest:

	def __init__(self, name, function):

		self.name = name
		self.function = function
		self.source = "github.com/buddycloud/buddycloud-tests-framework/blob/master/installation/" + name + ".py"

	def jsonfy(self):

		json = { 'name' : self.name,
			 'test' : self.function,
			 'continue_if_fail' : True,
			 'source' : self.source
		}
		return json
