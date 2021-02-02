<!-- <style type="text/css">
  h2 { margin-left: 10px; }
  h3 { margin-left: 20px; }
  h4 { margin-left: 30px; }
</style> -->

<style type="text/css">
body {
    counter-reset: h1
}

h1 {
    counter-reset: h2
}

h2 {
    counter-reset: h3
}

h3 {
    counter-reset: h4
}

h1:before {
    counter-increment: h1;
    content: counter(h1) ". "
}

h2:before {
    counter-increment: h2;
    content: counter(h1) "." counter(h2) ". "
}

h3:before {
    counter-increment: h3;
    content: counter(h1) "." counter(h2) "." counter(h3) ". "
}

h4:before {
    counter-increment: h4;
    content: counter(h1) "." counter(h2) "." counter(h3) "." counter(h4) ". "
}
</style>

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

