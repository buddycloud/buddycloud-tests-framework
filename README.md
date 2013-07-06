buddycloud-tests-framework
===========================

A framework for issuing tests to a given buddycloud
---------------------------------------------------

This project is all about testing buddycloud technology,
as well as helping one check if a given buddycloud installation
is correctly setup and able to federate with the world.

A test version is currently being deployed at http://protocol.buddycloud.com!

Want to help? It's pretty easy!

Adding a new test to a test suite
----------------------------------

First things, first. There are two test suites, each having different roles.

The ```installation``` test suite is composed of a series of tests to make sure a given buddycloud installation
is correctly setup. Otherwise, it won't be able to federate and socialize with others. DNS lookups, XMPP communication checks and other
things like that are done to ensure the installation process was successful.

The ```integration``` test suite is composed, as the name suggests, of integration tests for the buddycloud technology.
These tests are necessary because they will exercise your buddycloud installation enough
 so we can be safe that your buddycloud will be able to federate and socialize with others.


Here's how you can add a new test to one of these suites. First, determine to which suite the new test is going to be added.

<dl><dt>Determine which test suite you want to contribute to</dl></dt>

> You can pick either the ```installation``` or the ```integration``` suite.
> Please bear in mind the purposes of each test suite before adding a new test.

<dl><dt>Create a new test file</dl></dt>

> Write a python test file (e.g named ```example.py```) containing a function called ```testFunction```.  
> 
> As of now, this ```testFuncion``` must have only one parameter corresponding to the domain to be tested.
> Future versions may allow something more flexible.
>
> Make sure your ```testFunction``` always returns a tuple with four elements in the following format:
>
> ```(exit_status, briefing, message, output)``` where:
>
> * ```exit_status type:int```
>	should be equal to ```0``` if test was successful or any other integer otherwise,
>
> * ```briefing type:str```
>	should be a brief explanation of what happened during the test,
>
> * ```message type:str```
>	should be a longer message with more information and
>
> * ```output type:anything```
>	should be anything your test could output if you want this test's results to be reused by other tests,
>	otherwise just return ```None```
>
> *Important:*
>
> 1. Your test runs within an execution_context folder with read/write permissions. Anything your test writes will be placed there (e.g. logs).
>
> 2. Your test can import any library that is installed in the server. If you need some other library to be installed, let us know.
>
> 3. Your test can import other ```testFuncion```s defined in other existing tests belonging to the same test suite as well.
> Here's an example of a test that reuses the test defined at ```api_lookup.py```:
>
>	```from api_server_lookup import testFunction as apiLookup```

<dl><dt>Declare that your test should be run as part of the test suite</dl></dt>

> Append a new line to the ```installation/installation_tests.cfg``` configuration file containing only the name
> of your new test file.  
> Make sure *NOT* to add the extension ```.py``` (e.g. just add ```example``` if your test file name is ```example.py```)
>
> *Important:*
>
> 1. You can always prepend a hashtag to a line of the configuration file to make sure the test suite won't include that particular test.


So, that's all, folks!
--------------

Please send pull requests with new tests.
