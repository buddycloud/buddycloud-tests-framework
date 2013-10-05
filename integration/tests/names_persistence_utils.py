import random

def storeActualName(name):

	actual_name = name + str(random.random()).split(".")[1]

	f = open(name, 'w')
	f.write(actual_name)
	f.close()

def obtainActualName(name):

	try:
		f = open(name, 'r')
		actual_name = f.read().strip()
		f.close()
		return actual_name

	except IOError:
		storeActualName(name)
		return obtainActualName(name)
