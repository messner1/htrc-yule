# htrc-yule
Yule's K generated for the pre-generated version of the HTRC genre seperated corpus (https://sharc.hathitrust.org/genre).

The CSVs contain the HTID of the volume followed by the K calculated for the volume.  ' Was used as the text seperator. 

The code is messy but fairly straightforward. The basic process is to call one of the three functions in yule_htrc.py -- non_fuzzy, as_single_corpus or fuzzy_restrictions.  The difference between the three is briefly covered in the accompanying blogpost. Each requires an argument with the path to the data to be used (.tsvs, will iterate over child folders to gather them as well), the path to the metadata CSV, and the path to the contextual correction csv.

Why I did this can be found in the blog post here: http://cmessner.com/blog/?p=127
