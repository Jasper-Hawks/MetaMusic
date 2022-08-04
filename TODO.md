# General
- [x] Handle duplicate files
- [x] Add status codes all throught to assure the user
- [x] Have the ability to look at more than 5 searches
- [x] Fix regex so that it can take input from directories that are on the same working directory
- [x] Add error handling so that if there are no results something is printed to the screen, and the user can be prompted if they enter an incorrect selection
- [ ] Refactor id3 section for clarity
- [ ] Rename variables for clarity
- [ ] Convert file names to unescaped plain text for more matches
- [ ] Print the names of the files we did not find (Maybe?)

# Argparse/Flags
- [x] Create a CLI interface with the argparse library
- [x] Add a flag to replace the file names with the track titles(https://docs.python.org/3/library/os.html#os.replace)
-    [x] Add a flag to add track numbers to the files
-    [x] Add a flag to scrape data for songs
-    [x] Make the title flag work with the songs flag
-    [x] Make an overwrite flag
-    [x] Make a delete data flag

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

