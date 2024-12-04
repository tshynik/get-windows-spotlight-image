import hashlib
from pathlib import Path
# import json
import logging

logging.basicConfig(
	level = logging.INFO,
	format = "%(asctime)s [%(levelname)s] %(message)s",
	handlers = [
		# logging.FileHandler("find_duplicates.log"),
		logging.StreamHandler()
	]
)

# list all the files in the Windows folder:
list_of_images = list(Path('').glob('**/*.jpg'))

logging.info(f"found {len(list_of_images)} to process")
count = 0
for image in list_of_images:
	count += 1
	# check if it's been renamed to start with the hash:
	# format: md5_2a91ffe0f5ab40b5a9b8b720ef4dc625_[stem]
	if image.stem[:4] != "md5_":
		img_hash = hashlib.md5(open(image,'rb').read()).hexdigest()
		image.rename(image.with_stem(f"md5_{img_hash}_{image.stem}"))

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
