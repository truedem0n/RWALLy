import praw
from urlextract import URLExtract
from dotenv import dotenv_values
config = dotenv_values(".env")
extractor = URLExtract()
from enum import Enum
from urllib.parse import urlparse
from urllib.parse import parse_qs

class SortType(Enum):
    top = "top"
    new = "new"
    hot = "hot"
    rising = "rising"
    controversial = "controversial"
    all = "all"

class SortLength(Enum):
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"
    year = "year"
    gilded = "gilded"

reddit = praw.Reddit(
    client_id=config["CLIENT_ID"],
    client_secret=config["CLIENT_SECRET"],
    password=config["PASSWORD"],
    user_agent=config["USER_AGENT"],
    username=config["USERNAME"],
)

def get_wallpapers(subredditName, sortlength, sort, limit):
  subreddit = reddit.subreddit(subredditName)
  if sort == "top":
    submissions = subreddit.top(sortlength,limit=limit)
  elif sort == "new":
    submissions = subreddit.new(limit=limit)
  elif sort == "rising":
    submissions = subreddit.rising(limit=limit)
  elif sort == "controversial":
    submissions = subreddit.controversial(limit=limit)
  elif sort == "gilded":
    submissions = subreddit.gilded(limit=limit)
  elif sort == "hot":
    submissions = subreddit.hot(limit=limit)
  filteredSubmissions = []
  for submission in submissions:
    # print("\n\n\n")
    # print(submission.__dict__)
    urls = extractor.find_urls(str(submission.__dict__))
    previewList = list(filter(lambda x: "preview" in x and "award" not in x,urls))
    autoExist = False
    paramDic = {}
    for url in previewList:
      # print("before",url)
      # print("blur in ", url, "blur" not in url)
      if "blur" not in url:
        if "width" in url:
          parsed_url = urlparse(url)
          captured_value = parse_qs(parsed_url.query)['width'][0]
          paramDic[captured_value] = url
        else:
          paramDic["9"] = [url]
          autoExist = True
    keys = list(map(lambda x: int(x),list(paramDic.keys())))
    keys.sort(reverse=True)
    if len(paramDic.keys()): 
      if autoExist: 
        filteredSubmissions.append([paramDic[f"9"][0],submission.__dict__["title"],subredditName])
      else:
        filteredSubmissions.append([paramDic[f"{keys[0]}"],submission.__dict__["title"],subredditName])
  return filteredSubmissions
  


# get_wallpapers("animewallpaper",SortLength.month.value,SortType.top.value,10)