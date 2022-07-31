# General
- [ ] Fix regex so that it can take input from directories that are on the same working directory
- [x] Add status codes all throught to assure the user
- [x] Have the ability to look at more than 5 searches
- [ ] Refactor id3 section for clarity
- [ ] Rename variables for clarity
- [x] Handle duplicate files
- [ ] Add error handling so that if there are no results something is printed to the screen

# Argparse/Flags
- [x] Create a CLI interface with the argparse library
- [x] Add a flag to replace the file names with the track titles(https://docs.python.org/3/library/os.html#os.replace)
-    [x] Add a flag to add track numbers to the files
-    [ ] Add a flag to scrape data for songs

# Bugs
- [x] Fix songs missing metadata
     SOLUTION Files and their metadata  can have small
     variations in their titles. Some albums data has capitalized
     two letter words, downloaded files may have lowercase two
     letter words.

     Replaced the in keyword with a regex search that ignores cases

- [x] Fix r and n flag deleting files
      SOLUTION have the r and n flags work irrespective of metadata
      being applied. Mutagen couldn't add metadata to the file because
      the files name was being changed.

      Added the file name to the ID3 method

