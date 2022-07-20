import os
from ytmusicapi import YTMusic
import json
import re

# Set up the header files
ytmusic = YTMusic("headers_auth.json")

# TODO Replace this with stdin
# Find the input to search
dir = input("Directory: ")
os.chdir(dir)
# Use regex to parse the last directory for querying
# TODO Regex does not work with directories ending in a slash
# Make regex to get rid of the slash

# TODO Regex doesnt work with passing in directories that the
# user is currently on
indRes = []
results = []
browseIDs = []

query = re.search('\/(?:.(?!\/))+$',dir,re.MULTILINE)
q = query.group()
query = re.sub('\/','',q)

met = ytmusic.search(query,filter='albums')
#print(json.dumps(met, indent=4))

i = 0;
prevDict = None
for d in met:
    for val in d:
        if i < 5:
            if prevDict != d or prevDict == None:

              results.append(d["title"])
              # To find the artists since it is in a nested dictionary we need
              # to assign values to different variables
              a = d["artists"]
              art = a[0]
              results.append(art["name"])
              results.append(d["type"])
              results.append(d["year"])

              t = d["thumbnails"]
              thumb = t[3]
              results.append(thumb['url'])
              i+=1
              browseIDs.append(d["browseId"])

            else:

                break

            # So we have as little repeating as possible
            prevDict = d

for j in range(1,26):
   print(results[j-1])
   if j % 5 == 0 and j != 0:
       print("\n")

sel = int(input("Make a selection:"))

# Add a try catch here incase user puts something dumb
albumContents = ytmusic.get_album(browseIDs[sel - 1])
#print(json.dumps(albumContents, indent=4))

dirTitles = []
titles = []
for tracks in albumContents["tracks"]:
    titles.append(tracks)

dirTitles = os.listdir()
# Crossreference the songs in albumContents with those in the system

for t in dirTitles:
    for i in range(len(titles)):
        if t.contains(titles[i]):


