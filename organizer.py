import json
from operator import attrgetter
from pprint import pprint

#TODO
#Prettify string result of shows list

#Master dictionary of shows to list of groups, rating for current show)
shows = {}

#Holds a group's details and its rating for a particular show
#Multiple Group objects can share a name for different shows
class Group:
    def __init__(self, groupname, grouplang, showname, show_approval):  
        self.showname = showname
        self.groupname = groupname
        self.grouplang = grouplang
        self.showup = str(show_approval[0])
        self.showdown = str(show_approval[1])
    def __repr__(self):
        return "\nGroup: "+self.groupname+"\nRating: "+self.showup+"/"+self.showdown   



def parse_data(data):
    groupname = data["Group"]["Group Name"]
    grouplang = data["Group"]["Primary Language"]
    numshows = len(data["Subbed Projects"])

    for show in data["Subbed Projects"]:
        showname = show["Show Name"]
        approval_str = show["User Approval"]
        show_approval = getShowRatings(approval_str)
        group = Group(groupname, grouplang, showname, show_approval)
        #append current group to list of groups for a show
        if (showname in shows):
            shows[showname].append(group)
        else:
            shows[showname] = [group]

    #print (shows)

def getShowRatings(approval_str):
    nums = [int(s) for s in approval_str.split() if s.isdigit()]    
    return (nums[0], nums[1])
    
def sortShowsByRating():
    for show, groups in shows.items():
        #sort this show's ratings 
        keyUp = attrgetter("showup")
        groups.sort(key=keyUp)

def main():
    #Open file and read one group's data
    with open("data/3x3m.json") as f:
        data = json.load(f)
    parse_data(data)

    #Open a different file that has unique shows
    with open("data/Gayako.json") as f:
        data = json.load(f)
    parse_data(data)

    #Open a file that has 2 shows in common and update the shows dict
    with open("data/Mixed.json") as f:
        data = json.load(f)
    parse_data(data)

    with open('data/unsorted', 'w') as f:
        f.write(str(shows))
    sortShowsByRating()
    with open('data/sorted', 'w') as f:
        f.write(str(shows))

main()