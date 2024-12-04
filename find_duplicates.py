import hashlib
from pathlib import Path
import json
import logging

logging.basicConfig(
	level = logging.INFO,
	format = "%(asctime)s [%(levelname)s] %(message)s",
	handlers = [
		logging.FileHandler("find_duplicates.log"),
		logging.StreamHandler()
	]
)

# list all the files in the Windows folder:
list_of_files = list(Path('').glob('**/*.jpg'))

# initialize dict:
hashes = dict()

count = 0
for file in list_of_files:
	count += 1
	# print(file.name)
	# print(hashlib.md5(open(file,'rb').read()).hexdigest())

	img_hash = hashlib.md5(open(file,'rb').read()).hexdigest()

	# hashes[str(file.name)] = hashlib.md5(open(file,'rb').read()).hexdigest()
	try:
		hashes[img_hash].append( f"{file.parent}/{file.name}" )
		logging.info(f'found existing? {img_hash}')
		logging.info(hashes[img_hash])
	except Exception:
		hashes[img_hash] = [ f"{file.parent}/{file.name}" ]

	if count % 100 == 0:
		logging.info(f"processed {count}")

with open('all hashes.json', mode = 'w', encoding = 'utf8') as output_file:
	json.dump(hashes, output_file, default=str)

dupe_hashes = dict()
for img_hash, img_paths in hashes.items():
	if len(img_paths) > 1:
		dupe_hashes[img_hash] = img_paths

with open('all hashes - duplicates only.json', mode = 'w', encoding = 'utf8') as output_file:
	json.dump(dupe_hashes, output_file, default=str)
