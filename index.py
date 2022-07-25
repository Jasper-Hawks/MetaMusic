import os
import requests
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TDRC, TRCK, APIC
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

pg = 1

def search(met, results,pg):

    i = 0
    prevDict = None
    for d in met:
        for val in d:
            if i < (pg * 5):
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

                if pg >= 2:
                    for i in range(len(results) - (25 * pg)):
                        results.pop(0)

    for j in range(1,26):
       print(results[j-1])
       if j % 5 == 0 and j != 0:
           print("\n")

    sel = int(input("Make a selection:"))

# Add a try catch here incase user puts something dumb
    if sel <= 5 and sel >= 1:
        sel = sel + ((pg - 1)  * 5)
        albumContents = ytmusic.get_album(browseIDs[sel - 1])
    elif sel == 6:
        pg += 1
        albumContents = search(met,results,pg)

    return albumContents

albumContents = search(met,results,pg)

trackCount = int(albumContents["trackCount"])
print(trackCount)

dirTitles = []
album = []
songs = []

for tracks in albumContents["tracks"]:
    songs = []
    songs.append(tracks["title"])
    art = tracks["artists"]
    art = art[0]
    songs.append(art["name"])
    songs.append(tracks["album"])
    album.append(songs)


album.append(albumContents["year"])
thumb = albumContents["thumbnails"]
thumb = thumb[3]
album.append(thumb['url'])

dirTitles = os.listdir()

img = requests.get(thumb['url']).content
with open (album[0][2] + ".jpeg","wb") as handler:
    handler.write(img)

albumImgs = os.listdir()

for files in albumImgs:
    if files.endswith('.jpeg'):
        albumImgs = files
        dirTitles.remove(albumImgs)
        print("Album art created as: " + albumImgs)
#    else:
        #TODO Redo this
        #print("Album art was not generated")



# Crossreference the songs in albumContents with those in the system
tracks = album
tracks.pop(-1)
tracks.pop(-1)
print(tracks)
print(dirTitles)
for t in dirTitles:
  for i in range(len(tracks)):
      if tracks[i][0] in t:
        print("Adding metadata to: " + tracks[i][0])
        id3 = ID3()
        id3.add(TIT2(encoding=3,text=album[i][0]))
        id3.add(TPE1(encoding=3,text=album[i][1]))
        id3.add(TALB(encoding=3,text=album[i][2]))
        id3.add(TDRC(encoding=3,text=album[-2]))
        id3.add(TRCK(encoding=3,text=str(i + 1)))

        with open(albumImgs,'rb') as art:
            id3['APIC'] = APIC(
               encoding=3,
               mime='image/jpeg',
               type=3,desc=u'Cover',
               data=art.read()
            )
        #TODO Error handling if art cant be added to a frame

        id3.save(t,v2_version=4)

