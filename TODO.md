# General
- [x] Handle duplicate files
- [x] Add status codes all throught to assure the user
- [x] Have the ability to look at more than 5 searches
- [x] Fix regex so that it can take input from directories that are on the same working directory
- [x] Add error handling so that if there are no results something is printed to the screen, and the user can be prompted if they enter an incorrect selection
- [x] Refactor try catch no header exception
- [x] Accept stdin
- [x] Add stdin to songs
- [x] Convert file names to unescaped plain text for more matches
- [x] Escape characters on songs as well
- [ ] Recreate the search system so that less identical matches are shown
      when you go to the next page. Eventually stop the searches.
- [ ] Replace the status code that finds the amount of tracks in an album with
      the title and author of the album.

# Argparse/Flags
- [x] Create a CLI interface with the argparse library
- [x] Add a flag to replace the file names with the track titles(https://docs.python.org/3/library/os.html#os.replace)
-    [x] Add a flag to add track numbers to the files
-    [x] Add a flag to scrape data for songs
-    [x] Make the title flag work with the songs flag
-    [x] Make an overwrite flag
-    [x] Make a delete data flag
-    [x] Make a stdin flag
-    [x] Selection flag to select the first result

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

- [x] Fix stdin flag breaking the selection
      SOLUTION Had to close stdin. I was searching
      for a way to close stdin because you have to
      close files using a similar method.

- [x] Titles with special character [] can not be matched

      Escaping special characters in track titles
      in order to match more files to track titles.
      The re.search method does not work with escaped
      special characters since they are regex characters.

      Searching for a new method to find escaped substrings
      within a string.

      SOLUTION Track names refrain from using [] instead using
      (). Substituted those out and discovered the obvious
      solution to case insensitive substring matching by converting
      both strings to lowercase and using the in Python keyword.
