#!/usr/bin/python3
import argparse, os, requests, re, json, sys
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TDRC, TRCK, APIC
from ytmusicapi import YTMusic
parser = argparse.ArgumentParser(description="Add metadata to songs and albums with MetaMusic")
parser.add_argument('directory', type=str, help="Specify a directory/file containing an album/song for metadata to be added to.",nargs='?')
parser.add_argument('-d','--delete',action='store_true',help="Delete files/albums' metadata")
parser.add_argument('-f','--first',action='store_true',help="Select the first result in the list.")
parser.add_argument('-i','--stdin',action='store_true',help="Use stdin instead of the directory/song positional argument")
parser.add_argument('-n','--numbered',action='store_true',help="Add the tracks number to the name of the file. (Songs can't be numbered)")
parser.add_argument('-o','--overwrite',action='store_true',help="Overwrite metadata on files/albums")
parser.add_argument('-r','--replace',action='store_true',help="Replace file names with the names of tracks")
parser.add_argument('-s','--song',action='store_true',help="Add the metadata of a single song.")
parser.add_argument('--title', type=str, metavar='TITLE',help="Manually enter the title of the album/song")
args = parser.parse_args()

#parser.add_argument(metavar='S', type=str)
# Set up the header files
try:
    ytmusic = YTMusic()
except:
    print("Please generate a headers_auth.json file and make it accessable on your PATH.")
# TODO Replace this with stdin
# Find the input to search
# Use regex to parse the last directory for querying

indRes = []
results = []
browseIDs = []
pg = 1

def delAlbData(data):
    mp3s = []
    os.chdir(data)
    files = os.listdir()

    for file in files:
        if file.endswith('.mp3'):
            mp3s.append(file)

    for m in mp3s:
        try:
            id3 = ID3(m)
            id3.delete(m)
            id3.save()
            print(m + "'s metadata has been deleted")
        except:
            print(m + "'s metadata can not be deleted. Make sure that the file has metadata or redownload the file. ")
    exit()
def delSongData(data):
    mp3s = []
    files = os.listdir()

    for file in files:
        if file.endswith('.mp3'):
            mp3s.append(file)

    for m in mp3s:
        if re.search(data,m,re.IGNORECASE):
            try:
                id3 = ID3(m)
                id3.delete(m)
                id3.save()
                print(m + "'s metadata has been deleted")
            except:
                print(m + "'s metadata can not be deleted. Make sure that the file has metadata or redownload the file. ")
    exit()

def search(met, results,pg):
    # Searches with the API in order to find
    # albums/songs that match the query and
    # prints them to the screen

    if args.song:
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
                      results.append(d["category"])
                      album = d["album"]
                      results.append(album["name"])
                      t = d["thumbnails"]
                      thumb = t[-1]
                      results.append(thumb['url'])
                      i+=1
                      browseIDs.append(d["videoId"])

                    else:
                        break

                    # So we have as little repeating as possible
                    prevDict = d

                    if pg >= 2:
                        for i in range(len(results) - (25 * pg)):
                            results.pop(0)
    else:

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
                      thumb = t[-1]
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

    isSelecting = True

    while isSelecting:
        try:

            if args.first:
                sel = 1
            else:
                sel = int(input("Make a selection (? for options): "))
        except ValueError:
            sel = 0
        if sel >= 1 and sel <= 5:
            if args.song:
                isSelecting = False
                contents = ytmusic.get_song(browseIDs[sel - 1])
            else:
                isSelecting = False
                contents = ytmusic.get_album(browseIDs[sel - 1])
        elif sel == 6:
            pg += 1
            contents = search(met,results,pg)
        else:
            print ("Please choose a number 1-5 to select an album/song or 6 for a new page of results")

    return contents

def getAlbum(albumContents):


    dirTitles = []
    audioFiles = []
    album = []

    # Append all of the tracks in the album into an array
    # for ease of applying tags
    for t in albumContents["tracks"]:
        songs = []
        songs.append(t["title"])
        art = t["artists"]
        art = art[0]
        songs.append(art["name"])
        songs.append(t["album"])

        album.append(songs)

    print(str(albumContents["trackCount"]) + " tracks in " + albumContents["title"] + " - " + art["name"])

    # Since the year and thumbnails are all the same
    # we don't need to put them in the nested arrays
    album.append(albumContents["year"])
    thumb = albumContents["thumbnails"]
    thumb = thumb[3]
    album.append(thumb['url'])

    # Find the files in the cwd
    dirTitles = os.listdir()

    f = 0
    # Find all of the mp3 files
    for files in dirTitles:
        if files.endswith('.mp3'):
            audioFiles.append(files)
            f += 1

    print("Found " + str(f) + " mp3 files")

    # Write the thumbnail img to file
    img = requests.get(thumb['url']).content
    with open (album[0][2] + ".jpeg","wb") as handler:
        handler.write(img)

    albumImgs = os.listdir()

    for files in albumImgs:
        if files.endswith('.jpeg'):
            albumImgs = files
            print("Album art created as: " + files)
            break

    # Copy the album and remove the year and thumbnail so that we
    # only have track data
    tracks = album.copy()
    tracks.pop(-1)
    tracks.pop(-1)

    # Crossreference the songs in albumContents with those in the system
    f = 0
    for i in range(len(tracks)):
        for t in dirTitles:
            fileTitle = re.sub('....$','',t)
            trackNum = str(tracks.index(tracks[i]))
            escapedTrack = re.sub("\(","[",tracks[i][0])
            escapedTrack = re.sub("\)","]",escapedTrack)
            # This if statement checks if the files have the name of the titles within them.
            # it also checks if the tracks are numbered.
            if fileTitle.lower() in tracks[i][0].lower() or re.search("^" + trackNum  + "(?=\.)",fileTitle):

                currentFileName = t
                replacedFileName = ""
                numberedFileName = ""

                id3 = ID3()

                if args.overwrite:
                    id3.delete(t)
                    id3.save(t)
                    print("Overwriting  metadata: " + currentFileName)
                else:
                    print("Adding metadata: " + currentFileName)

                id3.add(TIT2(encoding=3,text=tracks[i][0]))
                id3.add(TPE1(encoding=3,text=tracks[i][1]))
                id3.add(TALB(encoding=3,text=tracks[i][2]))
                id3.add(TDRC(encoding=3,text=album[-2]))
                id3.add(TRCK(encoding=3,text=str(i + 1)))

                with open(albumImgs,'rb') as art:
                    id3.add(APIC(
                       encoding=3,
                       mime='image/jpeg',
                       type=3,desc=u'Cover',
                       data=art.read()
                    ))

                id3.save(t,v2_version=4)

                f += 1

                if args.replace:
                    replacedFileName = tracks[i][0]+".mp3"
                    os.replace(currentFileName,replacedFileName)
                    currentFileName = tracks[i][0]+".mp3"
                    print("Renamed: " + currentFileName + " to: " + replacedFileName)

                if args.numbered:
                    numberedFileName = str(i + 1) + "." + currentFileName
                    os.replace(currentFileName,numberedFileName)
                    currentFileName = numberedFileName + currentFileName
                    print("Numbered: " + currentFileName + " to: " + numberedFileName)

#                print("Metadata applied to " + t)
#   for t in dirTitles:
#     for i in range(len(tracks)):
#         # Ignore the cases because files and and data titles may
#         # capitilize different words

#         # TODO Decide whether we can use just the escaped track string or if
#         # we need both the track title and the escaped string. We probably
#         # just need the escaped track
#         escapedTrack = re.sub("\(","[",tracks[i][0])
#         escapedTrack = re.sub("\)","]",escapedTrack)
#         if escapedTrack.lower() in t.lower():

#             currentFileName = t
#             replacedFileName = ""
#             numberedFileName = ""

#              try:
#             id3 = ID3()
#             except ID3NoHeaderError:
#                 id3 = ID3()
#                 print("Skipping " + t )
#                 continue

#             if args.overwrite:
#                 try:
#                     id3.delete(t)
#                     id3.save()
#                     print("Overwriting  metadata: " + currentFileName)
#                 except:
#                     continue
#             else: print("Adding metadata: " + currentFileName)

#             id3.add(TIT2(encoding=3,text=tracks[i][0]))
#             id3.add(TPE1(encoding=3,text=tracks[i][1]))
#             id3.add(TALB(encoding=3,text=tracks[i][2]))
#             id3.add(TDRC(encoding=3,text=album[-2]))
#             id3.add(TRCK(encoding=3,text=str(i + 1)))

#             with open(albumImgs,'rb') as art:
#                 id3.add(APIC(
#                    encoding=3,
#                    mime='image/jpeg',
#                    type=3,desc=u'Cover',
#                    data=art.read()
#                 ))
#             # TODO Error handling if art cant be added to a frame

#             id3.save(t,v2_version=4)

#             f += 1

#             if args.replace:
#                 replacedFileName = tracks[i][0]+".mp3"
#                 os.replace(currentFileName,replacedFileName)
#                 currentFileName = tracks[i][0]+".mp3"
#                 print("Renamed: " + currentFileName + " to: " + replacedFileName)

#             if args.numbered:
#                 numberedFileName = str(i + 1) + "." + currentFileName
#                 os.replace(currentFileName,numberedFileName)
#                 currentFileName = numberedFileName + currentFileName
#                 print("Numbered: " + currentFileName + " to: " + numberedFileName)


#   print("MetaMusic added metadata to " + str(f) + " files")

def getSong(songContents):

    songData = []
    files = os.listdir()

    details = songContents["videoDetails"]
    songData.append(details["title"])
    songData.append(details["author"])

    mic = songContents["microformat"]
    mi = mic["microformatDataRenderer"]
    formatDate = re.search('....',mi["publishDate"])

    date = formatDate.group()
    songData.append(date)

    for file in files:
        # TODO Escape track titles similar to the way we did
        # with albums
        escapedTrack = re.sub("\(","[",songData[0])
        escapedTrack = re.sub("\)","]",escapedTrack)
        if file.lower() in songData[0].lower() or file.lower() in escapedTrack.lower():
            currentFileName = file
            if args.overwrite:
                try:
                    id3.delete(file)
                    id3.save()
                    print("Overwriting  metadata: " + songData[0])
                except:
                    continue

            id3 = ID3(file)
            id3.add(TIT2(encoding=3,text=songData[0]))
            id3.add(TPE1(encoding=3,text=songData[1]))
            id3.add(TDRC(encoding=3,text=songData[2]))

            id3.save(file)

            if args.replace:
                replacedFileName = songData[0]+".mp3"
                os.replace(currentFileName,replacedFileName)
                print("Renamed: " + currentFileName + " to: " + replacedFileName)

            print("Metamusic added metadata to " + currentFileName)

if args.song:

    if args.stdin:
        res = []
        for line in sys.stdin:
            res.append(line.rstrip('\n'))

        sys.stdin.close()
        sys.stdin = open(os.ctermid())

        dir = os.path.dirname(res[0])
        filePath = res[0]
        os.chdir(dir)

    else:

        filePath = args.directory
        dir = os.path.realpath(args.directory)
        dir = os.path.dirname(dir)
        os.chdir(dir)

    if args.title:

        query = args.title

    else:
        q = re.search(r'[^\/]*$',filePath)
        q = q.group(0)
        query = re.sub('....$','',q)

    if args.delete:
        delSongData(query)

    met = ytmusic.search(query,filter='songs')

    songContents = search(met,results,pg)
    getSong(songContents)

else:

    if args.delete:
        delAlbData(args.directory)
    try:
        if args.stdin:
            res = []
            for line in sys.stdin:
                res.append(line.rstrip('\n'))

            sys.stdin.close()
            sys.stdin = open(os.ctermid())

            dir = res[0]
            os.chdir(dir)

        else:
            dir = args.directory
            os.chdir(dir)


        if args.title:

            query = args.title

        else:

            # Directories that end in a slash will have that slash removed
            if re.search('\/$',dir):
                dir = re.sub('\/$','',dir)
            # Directories that do not begin with a slash will have a slash
            # added

            if re.search('\/',dir):
                pass
            else:
                dir = "/" + dir

            query = re.search('\/(?!.*\/).*',dir,re.MULTILINE)
            q = query.group()
            query = re.sub('\/','',q)
    except:
        print("Invalid directory")
        exit()

    met = ytmusic.search(query,filter='albums')

    albumContents = search(met,results,pg)
    getAlbum(albumContents)
