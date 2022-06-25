from multiprocessing.connection import wait
from os.path import expanduser
from threading import Thread
import os
import requests
import time
import re
import json
import rapi

appPath = expanduser("./")
wallsPath = appPath + "walls/"
# create folder if it does not exist
if not os.path.exists(appPath):
    os.makedirs(appPath)

# default config
def getDefaultConfig():
    return {
                "subs": [
                    {
                        "name": "wallpaper",
                        "percent": 100,
                        "sort": "top",
                        "sortType": "month",
                        "limit": 10
                    },
                ],
                "time": "10s",
                "cacheTime": "1h"
                }


# load json file if it exists
config = getDefaultConfig()
if os.path.exists(appPath + "config.json"):
    with open(appPath + "config.json") as f:
        config = json.load(f)

# verfiy subs total equal to 100 percent
if sum(map(lambda x: x['percent'], config['subs'])) != 100:
    raise Exception("Subreddit percentages do not add up to 100")

def getFileNameFromSubmission(submission):
    name = re.sub('[^a-zA-Z0-9 \n\.]', '', submission[1])
    return name.replace(" ", "_") + "." + submission[0].split("?")[0].split(".")[-1]

def downloadWallsToDir():
    for submission in submissions:
        url = submission[0]
        fileName = wallsPath + getFileNameFromSubmission(submission)
        try:
            # check if file exists
            if not os.path.exists(fileName):
                print(f"Downloading {fileName}")
                r = requests.get(url)
                file = open(fileName, "wb")
                file.write(r.content)
                file.close()
        except Exception as e:
            print("Error downloading wall")
            print(e)
    

def refreshWallsCache():
    global submissions
    submissions = []
    for sub in config['subs']:
        submissions.extend(rapi.get_wallpapers(sub['name'], sub['sortType'], sub['sort'], sub['limit']))
    print("Cache refreshed")
    print("Downloading walls")
    downloadWallsToDir()
    print("Walls downloaded")
    waitTime = int(config['cacheTime'])
    print(f"Waiting {waitTime} seconds before refreshing cache.")
    time.sleep(waitTime)

# Deprecated and will be removed in a future commit.
# def setWallpaper():
#     global submissions
#     def setWallpaperOnWindows(url,fileName):
#         try:
#             r = requests.get(url)
#             # check if file exists
#             if not os.path.exists(wallsPath + fileName):
#                 file = open(wallsPath + fileName, "wb")
#                 file.write(r.content)
#                 file.close()
#             PATH = os.path.abspath(wallsPath+fileName)
#             # set_wallpaper(PATH)
#             ctypes.windll.user32.SystemParametersInfoW(20, 0, PATH, 0)
#             print("Wallpaper set")
#         except Exception as e:
#             print("Error setting wallpaper")
#             print(e)
#     def setWallpaperOnLinux(url):
#         os.system(f"gsettings set org.gnome.desktop.background picture-uri {url}")
#     def setWallpaperOnMac(url):
#         os.system(f"osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"{url}\"'")
#     def setWallpaperCrossPlatform():
#         for submission in submissions:
#             # if platform is windows
#             if os.name == 'nt':
#                 setWallpaperOnWindows(submission[0],getFileNameFromSubmission(submission))
#             # if platform is linux
#             elif os.name == 'posix':
#                 setWallpaperOnLinux(submission[0],getFileNameFromSubmission(submission))
#             # if platform is mac
#             elif os.name == 'mac':
#                 setWallpaperOnMac(submission[0],getFileNameFromSubmission(submission))
#             time.sleep(int(config['time']))
#     while True:
#         setWallpaperCrossPlatform()
#         time.sleep(1)
        
    

if __name__ == "__main__":
    refreshWallsCacheThread = Thread(target=refreshWallsCache)
    refreshWallsCacheThread.start()
    refreshWallsCacheThread.join()
    # Deprecated
    # setWallpaperThread = Thread(target=setWallpaper)
    # setWallpaperThread.start()
    # setWallpaperThread.join()




