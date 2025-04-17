import dhash
from PIL import Image # pip install pillow
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
list_of_images = list(Path('mid').glob('**/*.jpg'))

logging.info(f"found {len(list_of_images)} to process")
count = 0
for image in list_of_images:
	count += 1

	# check if it's been renamed to start with the hash:
	# md5 format:   md5_2a91ffe0f5ab40b5a9b8b720ef4dc625_[stem]
	# dhash format: dha_c1c4e4a484a0809083fbffcc0040831e_[stem]
	#   - using dhash.format_hex(row, col)
	
	if image.stem[:4] != "dhs_":
		with Image.open(image) as image_stream:
			row, col = dhash.dhash_row_col(image_stream)
			img_hash_orig = dhash.format_hex(row, col)
			# decompose into hex digits, then sort and re-encode and combine:
			img_hash = ''.join([hex(item)[2:4] for item in sorted(bytes.fromhex(img_hash_orig))])

		# overwrite md5_ hash:
		if image.stem[:4] == "md5_" or image.stem[:4] == "dha_":
			image.rename(image.with_stem(f"dhs_{img_hash}_{image.stem[37:]}"))
		else:
			image.rename(image.with_stem(f"dhs_{img_hash}_{image.stem}"))

	if count % 25 == 0:
		logging.info(f"processed {count}")
