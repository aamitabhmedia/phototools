# Types of fixes
1. Missing image Date Shot
2. Image Date Shot does not match image file name
3. Image Date Shot does not match album year
4. Duplicate image acronyms

# Library-wide Tasks

## Run download_local_library.py
Update the cache

## Run test_dup_file_acronym.py
All images should have unique acronym.
The advantage is that you can select all images
in Google Photos by acronym and add them to the album

If images in the album need changes then take this opportunity to update other aspects like:

1. Run fix

## Run test_album_readiness.py
1. Run Only with ***Date Shot missing***
2. Run with:
   1. Bad image name format
   2. Tag mismatch
   3. Missing caption

## Run find_duplicate_image_names.py
Make sure no two files have the same name, just in case


