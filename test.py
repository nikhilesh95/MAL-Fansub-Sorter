import io
import re
import requests
from bs4 import BeautifulSoup

#Constants
baseurl = "https://myanimelist.net/fansub-groups.php"
lang_en = "Primary Language"

#Group class
class Group:
    def __init__(self):
        self.groupname=""
        self.groupurl=""
        self.groupup=0
        self.groupdown=0
        self.groupshows=[]

class Show:
    def __init__(self):
        self.showname=""
        self.showup=0
        self.showdown=0


def getGroups(letter):
    print("Getting Group Names and URLs for group '"+letter+"'")
    fname = 'data.txt'
    url = baseurl+"?letter="+letter
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find_all("td", class_="borderClass", width="300")
    links = []
    for td in data:
        groupname = td.text
        child=td.findChildren("a")
        groupurl = (str)(child[0])
        groupurl = groupurl[groupurl.find("?") : groupurl.find(">")-1]
        links.append((groupname, groupurl))
        
        #getGroupData(groupname, groupurl)
        #Build data structure

    with io.open(fname, "w", encoding="utf-8") as f:
        f.write((str)(links))
    f.close()


'''
Details: (Primary Language: English)
Group Name, List of Shows, Rating per show
'''
def getGroupData(groupname, groupurl):
    group = Group()
    page = requests.get(baseurl+groupurl)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    text = soup.get_text()

    #Check that subs are in English
    if not lang_check(text):    
        return "NotEnglish"

    (up,down,total) = getTotalRatings(text)
    shows = getShows(text)
    #print(shows)

    #Create the group object using this data
    group.groupname = groupname
    group.groupurl = groupurl
    group.groupdown = down
    group.groupup = up
    group.shows = shows


    return (soup)


'''Helper to check sub language'''
def lang_check(text):
    langpos = text.find(lang_en)+len(lang_en)
    lang = text[langpos:langpos+10]
    if("English" in lang):
        return True
    else:
        return False

'''Helper to get total rating count'''
def getTotalRatings(text):
    up_pos = text.find("approve")
    up_str = text[up_pos-10:up_pos]
    up = (int)(re.findall(r'\d+', up_str)[0])
    down_pos = text.find("disapprove")
    down_str = text[down_pos-10:down_pos]
    down = (int)(re.findall(r'\d+', down_str)[0])
    tr=up+down
    return (up,down,tr)

'''Helper to get Shows and Rating data'''
def getShows(text):
    show = Show()
    startpos = text.find("Group Projects")+len("Group Projects")
    finalpos = text.find("MoreTop Anime")
    currpos = startpos
    endpos = text.find("episodes")
    currtext = text[startpos:endpos]
    # while (currpos < finalpos):
    #     showname = text[startpos:endpos]
    #     (up,down) = getShowRatings(showname)
    #     print(showname)
    return ""

'''Helper to get Show name and number of episodes'''
def getShowNames(text):
    
    positions = [m.start() for m in re.finditer('episodes', text)]
    for pos in positions:
        print(text[pos-50:pos])

'''Helper to get show ratings'''
def getShowRatings(text):
    vote_pos = text.find("approve")
    vote_str = text[vote_pos-20:vote_pos]
    votes = (re.findall(r'\d+', vote_str))
    up = (int)(votes[0])
    down = (int)(votes[1])-up
    return (up,down)

'''Getting show names'''
def getShowNames(soup):
    names = soup.find_all("strong")
    return "shows: "+(str)(names)


def main():
    print ("Starting..")
    getGroups('.')
    groupsoup = getGroupData("8thSin Fansubs","https://myanimelist.net/fansub-groups.php?id=3375")  #English
    #groupdata = getGroupData("https://myanimelist.net/fansub-groups.php?id=5870") #German
    with io.open("groupdata.txt", "w", encoding="utf-8") as f:
        f.write((str)(groupsoup.get_text()))
    f.close()

    print(getShowNames(groupsoup))

#Run main
main()
