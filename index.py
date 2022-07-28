#!/usr/bin/python3
import argparse, os, requests, re
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TDRC, TRCK, APIC
from ytmusicapi import YTMusic


parser = argparse.ArgumentParser(description="Add metadata to songs and albums with MetaMusic")
parser.add_argument('directory', type=str, help="Specify a directory containing an album for metadata to be added to.")
parser.add_argument('-r','--replace',action='store_true',help="Replace file names with the names of tracks")
parser.add_argument('-n','--numbered',action='store_true',help="Add the tracks number to the name of the file")
parser.add_argument('-s','--song',action='store_true',help="Add the metadata of a single song")
parser.add_argument('--title', type=str, metavar='TITLE',help="Manually enter the title of the name/song")
args = parser.parse_args()

#parser.add_argument(metavar='S', type=str)
# Set up the header files
ytmusic = YTMusic("headers_auth.json")

# TODO Replace this with stdin
# Find the input to search
dir = args.directory
os.chdir(dir)
# Use regex to parse the last directory for querying

indRes = []
results = []
browseIDs = []

if args.title:

    query = args.title

else:
# TODO Regex does not work with directories ending in a slash
# Make regex to get rid of the slash
# TODO Regex doesnt work with passing in directories that the
# user is currently on
    query = re.search('\/(?:.(?!\/))+$',dir,re.MULTILINE)
    q = query.group()
    query = re.sub('\/','',q)

met = ytmusic.search(query,filter='albums')
pg = 1

def search(met, results,pg):
    # Searches with the API in order to find
    # albums/songs that match the query and
    # prints them to the screen

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

    print("\n")
    c = 1
    print("["+ str(c)+"]")
    for j in range(1,26):
       print(results[j-1])
       if j % 5 == 0 and j != 0:
           print("\n")
           c += 1
           print("["+ str(c)+"]")
    print("Next Page")
    print("\n")

    sel = int(input("Make a selection:"))

# TODO Add a try catch here incase user puts something dumb
    if sel <= 5 and sel >= 1:
        sel = sel + ((pg - 1)  * 5)
        albumContents = ytmusic.get_album(browseIDs[sel - 1])
    elif sel == 6:
        pg += 1
        albumContents = search(met,results,pg)

    return albumContents

def getAlbum(albumContents):

    print(str(albumContents["trackCount"]) + " tracks in " + albumContents["title"])

    dirTitles = []
    audioFiles = []
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

    f = 0
    # Clean the listed files for mp3 files
    for files in dirTitles:
        if files.endswith('.mp3'):
            audioFiles.append(files)
            f += 1

    print("Found " + str(f) + " mp3 files")

    img = requests.get(thumb['url']).content
    with open (album[0][2] + ".jpeg","wb") as handler:
        handler.write(img)

    albumImgs = os.listdir()

    for files in albumImgs:
        if files.endswith('.jpeg'):
            albumImgs = files
            print("Album art created as: " + albumImgs)


    tracks = album.copy()
    tracks.pop(-1)
    tracks.pop(-1)

# Crossreference the songs in albumContents with those in the system
    f = 0
    for t in dirTitles:
      for i in range(len(tracks)):
          if re.search(tracks[i][0],t,re.IGNORECASE):
              if args.replace:
                  os.rename(t,tracks[i][0]+".mp3")
                  try:
                      os.remove(t)
                  except (FileNotFoundError):
                      continue

              if args.numbered:
                  if args.replace:
                      os.rename(tracks[i][0]+".mp3",str(i + 1) + "." + tracks[i][0] + ".mp3")
                  else:
                      os.rename(t,str(i + 1) + "." + t)

                  try:
                      os.remove(t)
                  except (FileNotFoundError):
                      continue

              print("Adding metadata to: " + tracks[i][0])
              id3 = ID3()
              id3.add(TIT2(encoding=3,text=tracks[i][0]))
              id3.add(TPE1(encoding=3,text=tracks[i][1]))
              id3.add(TALB(encoding=3,text=tracks[i][2]))
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
              f += 1

    print("MetaMusic added metadata to " + str(f) + " files")
albumContents = search(met,results,pg)

getAlbum(albumContents)
