#!/usr/bin/python3
"""
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
  with the data from it

* Call json.loads(<json dictionary>, object_hook=as<main class>), which
  will build the main object from the dictionary, also building the 
  contained objects
"""

import json
import datetime

#######################################################################
# Challenge
#######################################################################

class Challenge(object):
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.teammate = ""

    def toJson(self):
        return {'__{}__'.format(self.__class__.__name__): self.__dict__}


# JSON decoding
def asChallenge(dct):
    if "__Challenge__" in dct:
        data = dct["__Challenge__"]
        c = Challenge(data["name"])
        c.points = data["points"]
        c.teammate = data["teammate"]
        return c
    else:
        return dct


#######################################################################
# Event
#######################################################################

class Event(object):
    def __init__(self, name, date):
        self.name = name
        self.date = date
        self.challenges = {}

    def toJson(self):
        return {'__{}__'.format(self.__class__.__name__): self.__dict__}


# JSON decoding
def asEvent(dct):
    if "__Event__" in dct:
        data = dct["__Event__"]
        e = Event(data["name"], datetime.date.fromisoformat(data["date"]))
        for k, v in data["challenges"].items():
            e.challenges[k] = asChallenge(v)
        return e
    else:
        return dct


#######################################################################
# Scores
#######################################################################

class Scores(object):
    def __init__(self):
        self.active = None
        self.events = {}

    def newEvent(self, evt):
        self.events[evt.name] = evt
        self.active = evt

    def toJson(self):
        d = dict(self.__dict__)
        evt = d.get("active")
        if evt:
            d["active"] = evt.name
        return {'__{}__'.format(self.__class__.__name__): d}

        
# JSON decoding
def asScores(dct):
    if "__Scores__" in dct:
        data = dct["__Scores__"]
        sc = Scores()
        for k, v in data["events"].items():
            sc.events[k] = asEvent(v)
        act = data["active"]
        if act != "":
            sc.active = sc.events[act]
        return sc
    else:
        return dct

#######################################################################
# Global JSON decoding
#######################################################################
class customEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Challenge, Event, Scores)):
            return obj.toJson()
        elif isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        else:
           # Let the base class default method raise the TypeError
           return json.JSONEncoder.default(self, obj)



if __name__ == "__main__":
    # Challenge serialization
    c1 = Challenge("rev1")
    s1 = json.dumps(c1, cls=customEncoder)
    print(s1)
    # deserialization
    cb = json.loads(s1, object_hook=asChallenge)
    print(json.dumps(cb, cls=customEncoder))

    # Event serialization
    e1 = Event("NoobCTF", datetime.date.fromisoformat('2021-01-10'))
    e1.challenges[c1.name] = c1
    c2 = Challenge("pwn1")
    c2.teammate = "grmmpff"
    c2.points = 498
    e1.challenges[c2.name] = c2
    s1 = json.dumps(e1, cls=customEncoder)
    print(s1)
    # deserialization
    eb = json.loads(s1, object_hook=asEvent)
    print(json.dumps(eb, cls=customEncoder))
    
    # Scores serialization
    scores = Scores()
    scores.newEvent(e1)
    scores.newEvent(Event("LamerCTF", datetime.date.today()))
    s1 = json.dumps(scores, cls=customEncoder)
    print(s1)
    # deserialization
    scb = json.loads(s1, object_hook=asScores)
    print(json.dumps(scb, cls=customEncoder))

