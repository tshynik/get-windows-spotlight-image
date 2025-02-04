# import dhash
# from PIL import Image
from pathlib import Path
# import json
import logging

import cv2
import numpy as np
from sklearn.cluster import KMeans


def visualize_colors(cluster, centroids):
	# Get the number of different clusters, create histogram, and normalize
	labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
	(hist, _) = np.histogram(cluster.labels_, bins = labels)
	hist = hist.astype("float")
	hist /= hist.sum()

	# Create frequency rect and iterate through each cluster's color and percentage
	rect = np.zeros((50, 300, 3), dtype=np.uint8)
	colors = sorted([(percent, color) for (percent, color) in zip(hist, centroids)])
	start = 0
	for (percent, color) in colors:
		print(color, "{:0.2f}%".format(percent * 100))
		end = start + (percent * 300)
		cv2.rectangle(rect, (int(start), 0), (int(end), 50), \
					  color.astype("uint8").tolist(), -1)
		start = end
	return rect

logging.basicConfig(
	level = logging.INFO,
	format = "%(asctime)s [%(levelname)s] %(message)s",
	handlers = [
		# logging.FileHandler("find_duplicates.log"),
		logging.StreamHandler()
	]
)

# list all the files in the Windows folder:
list_of_images = list(Path('test').glob('**/*.jpg'))

logging.info(f"found {len(list_of_images)} to process")
count = 0
for image_path in list_of_images:
	count += 1

	# check if it's been renamed to start with the hash:
	# md5 format:   md5_2a91ffe0f5ab40b5a9b8b720ef4dc625_[stem]
	# dhash format: dha_c1c4e4a484a0809083fbffcc0040831e_[stem]
	#   - using dhash.format_hex(row, col)
	
	### CLUSTER VERSION: ###
	# Load image and convert to a list of pixels
	image = cv2.imread(image_path)
	logging.info(f"read image {image_path}")
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	logging.info(f"converted colors of {image_path}")
	# reshape is from numpy: "Gives a new shape to an array without changing its data."
	# I think what this does is turn the image from 2D (with color channels in a 3rd dimension) to 1D (with color channels in the 2nd dimension, 3)
	pixel_list = image.reshape((image.shape[0] * image.shape[1], 3))
	logging.info(f"made pixel list: {pixel_list[:3]}")

	# Find and display most dominant colors
	cluster = KMeans(n_clusters=5).fit(pixel_list)
	print(cluster)
	print(cluster.cluster_centers_)
	
	visualize = visualize_colors(cluster, cluster.cluster_centers_)
	visualize = cv2.cvtColor(visualize, cv2.COLOR_RGB2BGR)
	cv2.imshow('visualize', visualize)
	cv2.waitKey()
	quit()

	# if image_path.stem[:4] != "dha_":
		### DHASH VERSION: ###
		# with Image.open(image) as image_stream:
		# 	row, col = dhash.dhash_row_col(image_stream)
		# 	img_hash = dhash.format_hex(row, col)

		# overwrite md5_ hash:
		# if image_path.stem[:4] == "md5_":
		# 	image_path.rename(image_path.with_stem(f"dha_{img_hash}_{image_path.stem[37:]}"))

		# if image_path.stem[:4] != "md5_":
		# 	image_path.rename(image_path.with_stem(f"dha_{img_hash}_{image_path.stem}"))

	if count % 25 == 0:
		logging.info(f"processed {count}")



# # either load or initialize an empty dict:
# try:
# 	with open('all hashes.json', 'r', encoding = 'utf8') as fp:
# 		hashes = json.load(fp)
# except:
# 	hashes = dict()

# count = 0
# for file in list_of_images:
# 	count += 1
# 	# print(file.name)
# 	# print(hashlib.md5(open(file,'rb').read()).hexdigest())

# 	if file not in hashes:
# 		img_hash = hashlib.md5(open(file,'rb').read()).hexdigest()

# 	# hashes[str(file.name)] = hashlib.md5(open(file,'rb').read()).hexdigest()
# 	try:
# 		hashes[img_hash].append( f"{file.parent}/{file.name}" )
# 		logging.info(f'found existing? {img_hash}')
# 		logging.info(hashes[img_hash])
# 	except Exception:
# 		hashes[img_hash] = [ f"{file.parent}/{file.name}" ]

# 	if count % 100 == 0:
# 		logging.info(f"processed {count}")

# with open('all hashes.json', mode = 'w', encoding = 'utf8') as output_file:
# 	json.dump(hashes, output_file, default=str)

# dupe_hashes = dict()
# for img_hash, img_paths in hashes.items():
# 	if len(img_paths) > 1:
# 		dupe_hashes[img_hash] = img_paths

# with open('all hashes - duplicates only.json', mode = 'w', encoding = 'utf8') as output_file:
# 	json.dump(dupe_hashes, output_file, default=str)
