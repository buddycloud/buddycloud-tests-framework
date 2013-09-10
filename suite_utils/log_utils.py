import string, logging

class LogStream():

	def __init__(self):
		self.content = ""
		self.delimiter = "\n"
	
	def setDelimiter(self, delimiter):
		self.delimiter = delimiter

	def write(self, message):

		if ( self.content != "" ):
			self.content = string.join([self.content, message], self.delimiter)
		else:
			self.content = message

	def flush(self):
		pass

	def reset(self):
		self.content = ""

	def getContent(self):
		return self.content


def getLogStream(logger):

	logger.setLevel(logging.DEBUG)

	log_stream = LogStream()

	handler = logging.StreamHandler(log_stream)
	handler.setLevel(logging.DEBUG)

	logger.addHandler(handler)

	return log_stream
