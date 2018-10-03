import json
from pprint import pprint

#TODO
#Prettify string result of shows list

#Master dictionary of shows to list of groups, rating for current show)
shows = {}

#Holds a group's details and its rating for a particular show
#Multiple Group objects can share a name for different shows
class Group:
    def __init__(self, groupname, grouplang, showname, show_approval, show_comments):  
        self.showname = showname
        self.groupname = groupname
        self.grouplang = grouplang
        if ',' in show_approval:
            self.show_approval = show_approval[0:show_approval.find(',')]
        else:
            self.show_approval = show_approval
        self.show_comments = show_comments 
    def __repr__(self):
        return "\nGroup: "+self.groupname+"\nRating: "+self.show_approval



def parse_data(data):
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

    #print (shows)

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

    print(shows)

main()