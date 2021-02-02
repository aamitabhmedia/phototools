<!-- <style type="text/css">
  h2 { margin-left: 10px; }
  h3 { margin-left: 20px; }
  h4 { margin-left: 30px; }
</style> -->

<style type="text/css">
h1 { counter-reset: h2counter; }
h2 { counter-reset: h3counter; }
h3 { counter-reset: h4counter; }
h4 { counter-reset: h5counter; }
h5 { counter-reset: h6counter; }
h6 {}

h2:before {
    counter-increment: h2counter;
    content: counter(h2counter) ".\0000a0\0000a0";
}

h3:before {
    counter-increment: h3counter;
    content: counter(h2counter) "." counter(h3counter) ".\0000a0\0000a0";
}

h4:before {
    counter-increment: h4counter;
    content: counter(h2counter) "." counter(h3counter) "." counter(h4counter) ".\0000a0\0000a0";
}

h5:before {
    counter-increment: h5counter;
    content: counter(h2counter) "." counter(h3counter) "." counter(h4counter) "." counter(h5counter) ".\0000a0\0000a0";
}

h6:before {
    counter-increment: h6counter;
    content: counter(h2counter) "." counter(h3counter) "." counter(h4counter) "." counter(h5counter) "." counter(h6counter) ".\0000a0\0000a0";
}</style>

# Steps to fix all the albums

## download_local_library.py
Update the cache

## find_duplicate_image_names.py
Make sure no two files have the same name, just in case

# Steps to fix Albums in a year

## test_album_readiness.py
1. Run Only with `Date Shot missing`
2. Run with:
   1. Bad image format
   2. Tag mismatch
   3. Missing caption

## Run test_dup_file_acronym.py
Make sure no two files have the same name, just in case

