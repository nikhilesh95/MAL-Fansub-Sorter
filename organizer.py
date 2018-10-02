import json
from pprint import pprint

# #Show object
# class Show:
#     def __init__(self, showname):
#         self.showname = showname

#Holds a group's details and its rating for a particular show
#Multiple Group objects can share a name for different shows
class Group:
    def __init__(self, groupname, grouplang, showname, show_approval, show_comments):  
        self.showname = showname
        self.groupname = groupname
        self.grouplang = grouplang
        self.show_approval = show_approval[0:show_approval.find(',')]   #cuts the 'e' from approve when no comments
        self.show_comments = show_comments 
    def __repr__(self):
        result = "\nGroup: "+self.groupname+"\nRating: "+self.show_approval
        return result

#Master dictionary of shows to list of groups, rating for current show)
shows = {}

#Open file and read one group's data
with open("data/3x3m.json") as f:
    data = json.load(f)

groupname = data["Group"]["Group Name"]
grouplang = data["Group"]["Primary Language"]
numshows = len(data["Subbed Projects"])

for show in data["Subbed Projects"]:
    showname = show["Show Name"]
    show_approval = show["User Approval"]
    show_comments = show["Comments"]
    group = Group(groupname, grouplang, showname, show_approval, show_comments)
    #append current group to list of groups for a show
    if (showname in shows):
        shows[showname].append(group)
    else:
        shows[showname] = [group]


#pprint(data)
pprint (shows)