import json
from pprint import pprint

#Show object
class Show:
    def __init__(self, showname):
        self.showname = showname

#Master dictionary of shows
shows = {}

#Open file and read one group's data
with open("data/3x3m.json") as f:
    data = json.load(f)

pprint(data)
