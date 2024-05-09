import hashlib
from pathlib import Path
import json

# folder = ''

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
		print(f'found existing? {img_hash}')
		print(hashes[img_hash])
	except:
		hashes[img_hash] = [ f"{file.parent}/{file.name}" ]
	
	if count % 100 == 0:
		print(f"processed {count}")

with open(f'all hashes.json', mode = 'w') as output_file:
	json.dump(hashes, output_file, default=str)

dupe_hashes = dict()
for key in hashes:
	if len(hashes[key]) > 1:
		dupe_hashes[key] = hashes[key]

with open(f'all hashes - duplicates only.json', mode = 'w') as output_file:
	json.dump(dupe_hashes, output_file, default=str)