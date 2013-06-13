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

Write a python test file containing a function called ```testFunction```.


2:
==

Write your test inside that function. Once you're finished, save that test file into the ```installation/tests``` folder.


3:
==

Then append a new line to the ```installation/installation_tests.cfg``` configuration file containing only the name
of your new test file.


4:
==
Note: you can always prepend a hashtag to a line of the configuration file to make the suite skip executing that particular test.


And, congratulations! You're done! You've just added a new test to our test fiute!


The process of adding new tests to the ```integration``` test suite is the same as for adding new tests to the ```installation``` test suite.


So, That's it!

Please send pull requests with new tests.
