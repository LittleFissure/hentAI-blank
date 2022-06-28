from pygelbooru import Gelbooru
import asyncio
import urllib.request
import os
import threading
from threading import Thread
import winsound
import json
import math

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
gelbooru = Gelbooru('API_KEY', 'USER_ID')

#make lambda function a defined function with exception handlling for contenttooshort
#add way to load and save a dictionary to a master json file
#check master json file if file exist and delete/skip it

def main():
    tagScheme = []
    for lines in open("tags.txt").read().split('\n'):
        tagScheme.append(([lines],[]))
    
    for i in tagScheme:
        path = os.getcwd() + '\\'  + '_'.join(tags for tags in i[0])
        if len(i[1]) > 0:
            path += '_NOT_' + '_'.join(tags for tags in i[1])
        path += '\\'
        if not os.path.exists(path):
            os.makedirs(path)
        dataEmpty = False
        result = [i for i in asyncio.run(gelbooru.search_posts(tags=i[0], exclude_tags=i[1],page = 0,limit = 1000))]
        minID = result[-1].id
        while not dataEmpty:
            for p in range(19):
                data = [i for i in asyncio.run(gelbooru.search_posts(tags=i[0] + ["id:<"+str(minID)], exclude_tags=i[1],page = p,limit = 1000))]
                if len(data) == 0:
                    break
                print(str(len(data)) + " " + str(len(result)) + " " + str(minID) + " " + str(result[-1]))
                result = result + data
            minID = min(result[-1].id,minID)
            dataEmpty = len(data) == 0
        result = [str(i) for i in result]
        print(len(result))
        while len(result) > 0:
            if threading.active_count() < threads:
                try:
                    master[result[0].split('/')[-1]]
                    result = result[1:]
                except:
                    master[result[0].split('/')[-1]] = True
                    t = Thread(target = downloadFile,args = (result[0],path,))
                    result = result[1:]
                    t.start()
        winsound.Beep(500,500)
        print("Search with whitelist tags:" + ' '.join(tags for tags in i[0]) + "\nand blacklist tags:" + ' '.join(tags for tags in i[1]) + "\nCompleted. Please give some time for the downloads to complete.\n")
    print("\n\nAll supplied search critera completed.")
    while threading.active_count() != 2:
        p = 1
    winsound.Beep(400,2000)

def downloadFile(url,Dir,x=0):
    try:
        urllib.request.urlretrieve(url,Dir + url.split('/')[-1])
    except urllib.error.ContentTooShortError:
        print(f"--Download Failed--\nAttempt: {x}\nFile - {url}\n")
        if x < 10:
            downloadFile(url,Dir,x+1)
    except urllib.error.HTTPError:
        print(f"--DownloadFailed--\n{url} no longer exist. E404\n")
        
def getMasterTable(filterExisting): #make filterExisting TRUE to remove duplicates
    try:
        dataFile = open("data.json")
        dictionary = json.loads(dataFile.read())
        for i in dictionary:
            dictionary[i] = not filterExisting
        dataFile.close()
    except:
        dictionary = {}
    for folder in os.listdir(os.getcwd()):
        if os.path.isdir(os.getcwd() + '\\' + folder):
            for file in os.listdir(os.getcwd() + '\\' + folder):
                try:
                    if dictionary[file]:
                        os.remove(os.getcwd() + '\\' + folder + '\\' + file)
                    dictionary[file] = True
                except:
                    dictionary[file] = True
    dataFile = open("data.json","w")
    json.dump(dictionary,dataFile)
    dataFile.close()
    return dictionary

fileLimit = 1000
threads = 250
master = getMasterTable(False) #Change this to FALSE if doing a new batch with an empty directory. MUST be empty dummy
main()
if 1 == 1:
    dataFile = open("data.json","w")
    json.dump(master,dataFile)
    dataFile.close()
