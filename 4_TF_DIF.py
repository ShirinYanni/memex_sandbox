# part 4 of building memex
# connections in the text;
import os, json
import functions 
import yaml
import re
import pandas as pd
from sklearn.feature_extraction.text import (CountVectorizer, TfidfTransformer)
from sklearn.metrics.pairwise import cosine_similarity

### variables
settingsFile = "settings.yml"
settings = yaml.safe_load(open(settingsFile))

memexPath = settings["path_to_memex"]


##code to process all .json files from memex;
def generatetfidfvalues():
    ocrFiles = functions.dicOfRelevantFiles(memexPath, ".json")
    citeKeys = list(ocrFiles.keys())

    docList   = []
    docIdList = []
    
    for citeKey in citeKeys:
        docData = json.load(open(ocrFiles[citeKey],"r",encoding= "utf8"))

        docId = citeKey
        doc   = " ".join(docData.values())
        
        doc = re.sub(r'(\w)-\n(\w)', r'\1\2', doc) #cleaning text
        doc = re.sub('\W+', ' ', doc)
        doc = re.sub('\d+', ' ', doc)
        doc = re.sub(' +', ' ', doc)

        docList.append(doc)
        docIdList.append(docId)
    
   
    ## convert our data into a differnt format
    vectorizer = CountVectorizer(ngram_range=(1,1), min_df= 1, max_df= 0.5) # not sure about the min_df value
    countVectorized = vectorizer.fit_transform(docList)
    tfidfTransformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    vectorized = tfidfTransformer.fit_transform(countVectorized) 
    cosineMatrix = cosine_similarity(vectorized)

    ## matrixes
    tfidfTable = pd.DataFrame(vectorized.toarray(), index=docIdList, columns=vectorizer.get_feature_names())
    print("tfidfTable Shape: ", tfidfTable.shape) # optional
    tfidfTable = tfidfTable.transpose()
    tfidfTableDic = tfidfTable.to_dict()
    ##
    cosineTable = pd.DataFrame(cosineMatrix)
    print("cosineTable Shape: ", cosineTable.shape) # optional
    cosineTable.columns = docIdList
    cosineTable.index = docIdList
    cosineTableDic = cosineTable.to_dict()
    

    ##Task: write the code that filters these dictionaries. filter out words that are not keywords
    ## words with highest values are key words; filter out distances; dic of dics
    ##loop to filter - create new dictionary while looping through;
    ##create empty dic - if values are below threshold exclude them, add the others
    # one json file with the keywords of each publication
    # one json file with the distances between publications (cosine similarities)

 
    filteredDic = {}                                                                  ## create empty dictionary 

    filteredDic = functions.filterDic(tfidfTableDic, 0.05)                            ## with the filterd function in functions.py filter through dic, with 0.05 as threshold

    with open("tfidfTableDic_filtered.txt", 'w', encoding='utf8') as f9:              ## save it into a textfile; avoid extension .json;
        json.dump(filteredDic, f9, sort_keys=True, indent=4, ensure_ascii=False)

    filteredDic = {}                                                                  ## same for the other dictionary
 
    filteredDic = functions.filterDic(cosineTableDic, 0.25)

    with open("cosineTableDic_filtered.txt", 'w', encoding='utf8') as f9:
        json.dump(filteredDic, f9, sort_keys=True, indent=4, ensure_ascii=False)

generatetfidfvalues()