'''
author: Ujjal Das
github: ujjaldas132
date: June, 2023
<p>

'''

from json import JSONEncoder
class Action:
    def __init__(self):
        self.action = ""
        self.access = ""
        self.description = ""
        self.resources = []
        self.conditionKey = []
        self.dependentActions = []


class Prefix :
    def __init__(self):
        self.prefix = ""
        self.link = []
        self.actions = []
        self.resources = []
        self.conditions = []


class Resource:
    def __init__(self):
        self.resourceType = ""
        self.arn = ""
        self.conditionKey = []

class Condition:
    def __init__(self):
        self.conditionKey = ""
        self.desc = ""
        self.type = ""


class ServiceEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__