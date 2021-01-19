# py_serialization
Python custom objects serialization example

###################################################################
Example of custom python classes JSON serialization/deserialization
###################################################################
1) Serialization:

* For each class, implement a toJson (or whatever) method, which
  will return a json representation of the class. That's the place
  to implement special treatment, eg to avoid duplicating object
  referenced by different properties (see Scores)

* Implement a json.JSONEncoder subclass, overriding default() method
  sothat it detects your custom classes and calls the toJson() method

* Call json.dumps(<instance>, cls=<json.JSONEncoder subclass>) to
  dump to JSON format


2) Deserialization:

* For each class, implement a as<Class> (or whatever) function, which
  will get a JSON dictionary as input and which will build an instance
  with the data from it.

* Call json.loads(<json dictionary>, object_hook=as<main class>), which
  will build the main object from the dictionary, also building the 
  contained objects
