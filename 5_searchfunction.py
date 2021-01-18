import functions
import yaml, json, re, os
settingsFile = "./settings.yml"
settings = yaml.safe_load(open(settingsFile))
memexPath = settings["path_to_memex"]
def search(seachArgument):
    targetFiles = functions.dicOfRelevantFiles(memexPath, ".json")  #get all the json files
    citeKeys = list(targetFiles.keys()) #list of the citekeys
    results = {}    
    for citeKey in citeKeys:    #loop trough all the keys
        docData = json.load(open(targetFiles[citeKey], "r", encoding="utf8"))   #load the respective json file with the ocr results
        for k, v in docData.items():    #keys = page numbers values = text
            if seachArgument in v:      #if the search Argument is in the page
                matchCounter = len(re.findall(seachArgument, v))    #count how often          
                if not citeKey in results.keys():   #creates an empty dict only if there isnt allready one                           
                    results[citeKey] = {}
                results[citeKey][k] = {}            #creates sub-dict with the page number as key
                results[citeKey][k]["matches"] = matchCounter   #at the key matches the number of matches 
                pagePath = os.path.join(functions.generatePublPath(memexPath, citeKey), "pages//", k + ".html")  #creates the path to the html file for the page
                results[citeKey][k]["pathToPage"] = pagePath
                results[citeKey][k]["result"] = v   #adds the ocred text to the dict
    with open("search.txt", 'w', encoding='utf8') as f9:    #saves it into a file too
        json.dump(results, f9, sort_keys=True, indent=4, ensure_ascii=False)
    return(results)
search("gender")