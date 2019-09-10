# Bookclub Grabber

The first form of my Bookclub Details Grabber, intended to take in a csv (generated from the nominations form) and output a pretty-formatted list of details about each of the book (intended for voting form generation).

The input .csv file must contain labels of the fields in the first row. The default script only requires that there is a field named "Title" and another named "Why", which contain the title of the book and the nominator's reasoning for submitting the book, respectively. The script may be extended to include an "Author Editor" field, but a quick test found that the quality of results returned by goodreads and google books were not improved by the inclusion of this creator information.

Note that at times, though rarely, Goodreads API returns a study guide for the material rather than the asset itself (Cliff's Notes: Moby Dick, e.g.). It is worth clicking through the links to be sure that the correct asset's details have been filled into the output. Google does not have this limitation.