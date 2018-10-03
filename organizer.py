import glob
import json
import timeit
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
        self.showup = show_approval[0]
        self.showdown = show_approval[1]
    def __repr__(self):
        return "\n"+self.groupname+" - "+str(self.showup)+"/"+str(self.showdown)



def parse_data(data):
    groupname = data["Group"]["Group Name"]
    grouplang = data["Group"]["Primary Language"]
    numshows = len(data["Subbed Projects"])

    for show in data["Subbed Projects"]:
        showname = show["Show Name"]
        #Try catch the case that a show has no rating
        try:
            approval_str = show["User Approval"]
            show_approval = getShowRatings(approval_str)
        except KeyError as e:
            show_approval = (0,0)
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
        groups.sort(key=keyUp,reverse=True)

#Make shows dict output not look like ass
def prettify():
    output = ""
    for show, groups in shows.items():
        output+="\n-----\n"+show+":"
        for group in groups:
            output+=str(group)
    return output

def tests():

    # Test sample data
    #Open file and read one group's data
    with open("test_data/3x3m.json") as f:
        data = json.load(f)
    parse_data(data)

    #Open a different file that has unique shows
    with open("test_data/Gayako.json") as f:
        data = json.load(f)
    parse_data(data)

    #Open a file that has 2 shows in common and update the shows dict
    with open("test_data/Mixed.json") as f:
        data = json.load(f)
    parse_data(data)

    # Test Sorting
    with open('test_data/unsorted.txt', 'w') as f:
        f.write(str(shows))
    sortShowsByRating()
    with open('test_data/sorted.txt', 'w') as f:
        f.write(str(shows))

    #Test Prettify
    with open('test_data/pretty.txt', 'w') as f:
        f.write(prettify())
    f.close()

def main(): 
    start = timeit.timeit()
    filepath = 'data/**/*.json'
    for filename in glob.glob(filepath):
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
            parse_data(data)
        f.close()
    sortShowsByRating()
    with open("Fansubs.txt", "w", encoding="utf-8") as outfile:
        outfile.write(prettify())
    outfile.close()
    end = timeit.timeit()
    print("Time elapsed: ")
    print(end-start)


main()