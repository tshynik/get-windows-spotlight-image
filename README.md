# get-windows-spotlight-image
Grab the windows spotlight image and save it.

# TODO

- [-] read in the previous hash instead of recalculating
	- pickle and json rundowns: https://stackoverflow.com/questions/7100125/storing-python-dictionaries
- [x] or... put a short rep of the hash at the start of the filename?
- [x] try another hash algorithm
	- Tried dhash - doesn't get duplicates next to each other tho.
	- I think K-means is probably the way to go - get like 3 principal components and then put the top one (or two?) in the filename. So similarity = close to each other in hash.

## some other possible hashes
idk if any are really faster tho.

full rundown of py code for deduplicating using hashing - uses dhash
https://pyimagesearch.com/2017/11/27/image-hashing-opencv-python/

dominant color in an image, using k-means clustering:
https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv

comparing various image hashes, with some comments on speed and motivation:
https://superuser.com/questions/1625385/explain-like-im-5-these-9-methods-to-compare-similar-pictures-hash-md5-sha

image similarity in general:
https://stackoverflow.com/questions/1005115/what-algorithm-could-be-used-to-identify-if-images-are-the-same-or-similar-re

dhash:
https://pypi.org/project/dhash/
https://github.com/benhoyt/dhash
https://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html - comparing dhash to ahash, phash
