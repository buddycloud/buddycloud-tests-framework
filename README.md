buddycloud-inspection
=====================

Inspects your XMPP setup and lets you know if you have any problems!

A test version is currently being deployed in Heroku at buddycloud-inspection.herokuapp.com

To add a new test called ```example```:

Write a python file containing your test function(s). Say we wrote a new file called 'example.py' which contains a function named ```testExample```.

All you have to do to add this function to the test suite is import a reference to this function into the ```tests.py``` file by doing:

```from example import testExample```

Then, add a new JSON entry to the 'test_entries' array in the following format:

```javascript
{'name' : '<test_name>', 'test' : testExample/testFunctionReference, 'continue_if_fail' : True/False, 'source' : sources_location+"example.py"/test_source_url })
```
And finally, add another entry into the ```test_names``` map, which has to be the name you just gave to your new test as a key and the next index available:

```python
test_names = {
'xmpp_server_srv_lookup' : 0,
'xmpp_server_a_lookup' : 1,
'xmpp_server_connection' : 2,
'buddycloud_server_disco' : 3,
'api_lookup' : 4,
'api_https_connection' : 5,
'push_server_disco' : 6,
'testExample' : 7   <= "new entry added here"
}
```

Please send pull requests with new tests.
