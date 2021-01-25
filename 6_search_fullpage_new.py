import re, os, yaml, json, random
from datetime import datetime
# SCRIPT WITH OUR PREVIOUS FUNCTIONS
import functions
###########################################################
# VARIABLES ###############################################
###########################################################
settings = functions.loadYmlSettings("settings.yml")
###########################################################
# FUNCTIONS ###############################################
###########################################################
def searchOCRresults(pathToMemex, searchString):
    print("SEARCHING FOR: `%s`" % searchString) #to keep track of what we are doing 
    files = functions.dicOfRelevantFiles(pathToMemex, ".json") #takes every file with OCR results
    results = {}                      ## create dictionary
    for citationKey, pathToJSON in files.items(): # loop through dictionary; all the files
        data = json.load(open(pathToJSON)) ## load results
        #print(citationKey)
        count = 0
        for pageNumber, pageText in data.items(): #loop for specific file in there
            if re.search(r"\b%s\b" % searchString, pageText, flags=re.IGNORECASE): # search; flags for re to ignore case
                if citationKey not in results:
                    results[citationKey] = {}
                # relative path
                a = citationKey.lower()
                relPath = os.path.join(a[:1], a[:2], citationKey, "pages", "%s.html" % pageNumber) # page to html.page, shows specific page in dictionary - klick on link to get to page
                countM = len(re.findall(r"\b%s\b" % searchString, pageText, flags=re.IGNORECASE)) # count how many matches are on the page; re.findall command; ignore case for better results
                pageWithHighlights = re.sub(r"\b(%s)\b" % searchString, r"<span class='searchResult'>\1</span>", pageText, flags=re.IGNORECASE)#take our page and wrap the match into html, assign a class, add into css file
                results[citationKey][pageNumber] = {} # create empty dic for each page
                results[citationKey][pageNumber]["pathToPage"] = relPath # add path to page
                results[citationKey][pageNumber]["matches"] = countM # number of matches
                results[citationKey][pageNumber]["result"] = pageWithHighlights.replace("\n", "<br>") # and formated page as results
                count  += 1 #count of number of searches that we run; can be done within the loop
        if count > 0: # reformate the results - thats why we want the count; not necessary - only to help with organizing search results
            print("\t", citationKey, " : ", count) # keep track of what is going on
            newKey = "%09d::::%s" % (count, citationKey) #creating a new key for each publication, combines frequency and citationkey
            results[newKey] = results.pop(citationKey) # removes an item from the dictionary - pop; command removes the old item and creates a new one at the same time
            # add time stamp; get datetime library 
            currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')# creates variable - formate the time in the red; string
            results["timestamp"] = currentTime #add extra item to dictionary; the timestampt with the actual time
            # add search string (as submitted)
            results["searchString"] = searchString # add searchstring to dictionary
    saveWith = re.sub("\W+", "", searchString) ## save the results, take the searchstring and remove all word characters
    saveTo = os.path.join(pathToMemex, "searches", "%s.searchResults" % saveWith) # create save path, putting search results in subfolder, assign extension - unique so that it does not exist already
    with open(saveTo, 'w', encoding='utf8') as f9c: #save results
        json.dump(results, f9c, sort_keys=True, indent=4, ensure_ascii=False) # json dump because it is a dictionary

###########################################################
# RUN THE MAIN CODE #######################################
###########################################################

#searchPhrase  = r"corpus\W*based"
#searchPhrase  = r"corpus\W*driven"
#searchPhrase  = r"multi\W*verse"
#searchPhrase  = r"text does ?n[o\W]t exist"
#searchPhrase  = r"corpus-?based"
searchOCRresults(settings["path_to_memex"], "classification")
#exec(open("9_Interface_IndexPage.py").read())