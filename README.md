buddycloud-tests-framework
===========================

This project is all about testing buddycloud technology,
as well as helping one check if a given buddycloud installation
is correctly setup and able to federate with the world.

A test version is currently being deployed in Heroku at http://buddycloud-inspection.herokuapp.com !

Want to help? It's pretty easy:

Adding a new test to a suite
============================

There are two test suites, each having completely different roles.

The ```installation``` test suite is composed of a series of tests to make sure a given buddycloud installation
is correctly setup and able to federate and socialize with others. DNS lookups, XMPP communication checks and other
things like that are done to ensure everything is right.

To add  a new test to this suite:

1:
==

Write a python test file (e.g named ```example.py```) containing a function called ```testFunction```.


2:
==

Write your test inside that function. Once you're finished, save that test file into the ```installation/tests``` folder.


3:
==

Make sure your function always returns a tuple with four elements in the following format:

```(exit_status, briefing, message, output)``` where
```exit_status``` (int)
	should be equal to ```0``` if test was successful or any other integer otherwise,
```briefing``` (str)
	should be a brief explanation of what happened during the test,
```message``` (str)
	should be a longer message with more information and
```output``` (anything)
	is anything your test could output if you are intend that your test is reused by other tests - otherwise just return None

4:
==

Then append a new line to the ```installation/installation_tests.cfg``` configuration file containing only the name
of your new test file. Make sure NOT to add the extension ```.py``` (e.g. just add ```example``` if your test file name is ```example.py```)


5:
==
Note: you can always prepend a hashtag to a line of the configuration file to make the suite skip executing that particular test.


And, congratulations! You're done! You've just added a new test to our test fiute!


The process of adding new tests to the ```integration``` test suite is the same as for adding new tests to the ```installation``` test suite.


So, That's it!

Please send pull requests with new tests.
