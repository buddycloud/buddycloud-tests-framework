import random

def storeActualName(session, name):

	actual_name = name + str(random.random()).split(".")[1]

#	f = open(name, 'w')
#	f.write(actual_name)
#	f.close()

	session[name] = actual_name

def obtainActualName(session, name):

#	try:
#		f = open(name, 'r')
#		actual_name = f.read().strip()
#		f.close()
#		return actual_name

#	except IOError:
#		storeActualName(name)
#		return obtainActualName(name)

	if not name in session:
		storeActualName(session, name)
	
	return session[name]
