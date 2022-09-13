
![MetaMusic Logo](./metamusic.png)
MetaMusic is a metadata tag editor that uses an [unofficial Youtube Music API](https://pypi.org/project/ytmusicapi/) to apply tags to mp3 files.

## Installation
Install Python3 and these packages using pip or a Python package manager of your choice.

```
pip install argparse mutagen ytmusicapi requests
```

Copy the index.py file to the /usr/local/bin directory and rename the file to what you would like to invoke on the command line (mm in this case):
```
cp index.py /usr/local/bin/mm
```

With the installed libraries MetaMusic should be ready to use.

## Usage
Below is the help message for MetaMusic:
```
usage: (MetaMusic alias) [-h] [-d] [-f] [-i] [-n] [-o] [-r] [-s] [--title TITLE] [directory]

Add metadata to songs and albums with MetaMusic

positional arguments:
  directory        Specify a directory containing an album for metadata to be added to.

options:
  -h, --help       show this help message and exit
  -d, --delete     Delete files/albums' metadata
  -f, --first      Select the first result in the list.
  -i, --stdin      Use stdin instead of the directory/song positional argument
  -n, --numbered   Add the tracks number to the name of the file. (Songs can't be numbered)
  -o, --overwrite  Overwrite metadata on files/albums
  -r, --replace    Replace file names with the names of tracks
  -s, --song       Add the metadata of a single song.
  --title TITLE    Manually enter the title of the album/song

```

Simply append the optional flags to the MetaMusic alias, and supply a directory/file for the positional argument. Unless you use the -i flag in that case pipe a directory/file and leave the positional directory/file argument blank.

## Like the project? Support me here:
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Q5Q8DP9QS)
