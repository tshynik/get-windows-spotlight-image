"""
Script that scans Windows Spotlight folders for new Spotlight images, copies them
to the script folder, and adds a file type extension for those missing one.
"""

import shutil
from pathlib import Path
from datetime import datetime as dt
import json
import dhash
from PIL import Image # pip install pillow

# via https://stackoverflow.com/questions/13733552:
import logging

logging.basicConfig(
	level = logging.INFO,
	format = "%(asctime)s [%(levelname)s] %(message)s",
	handlers = [
		logging.FileHandler("get_today_img.log"),
		logging.StreamHandler()
	]
)
logging.info("NEW RUN")


def clean_filename(filestem:str) -> str:
	filestem = filestem.lower()
	filestem = filestem.replace(', ','-')
	filestem = filestem.replace(' ','_')
	return filestem

## img hash settings
translation_table = str.maketrans(
	"0123456789abcdef",
	"abcdefghijklmnop"
	)
hash_name = 'ds3_'

# where to get the files:
folder_login = Path.home() / Path("AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets")
folder_desktop = Path.home() / Path("AppData/Local/Packages/MicrosoftWindows.Client.CBS_cw5n1h2txyewy/LocalCache/Microsoft/IrisService")
# windows 11 desktop spotlight - subfolders under that
logging.info(f"Looking here:\n{folder_login}\n{folder_desktop}")

# where to save the files:
today = Path.cwd() / Path('today')

# get date from latest files, or create the JSON if it doesn't exist yet.
try:
	with open('logs.json', mode = 'r', encoding = 'UTF-8') as log_file:
		log = json.load(log_file)
		# because it's written to JSON as a string, got to parse it:
		log['latest_file'] = dt.strptime(log['latest_file'],'%Y-%m-%d %H:%M:%S.%f')
except FileNotFoundError:
	log = {'latest_file': dt(1969, 1, 1) }

new_latest_file_time = log['latest_file']
logging.info(f"Only looking for new files since {new_latest_file_time}")

# list all the files in the Windows folder:
spotlight_files_candidates = list(folder_login.glob('**/*')) + list(folder_desktop.glob('**/*'))

for file in spotlight_files_candidates:

	if file.stat().st_size > 200000:
		# get file name and modification time:
		file_mod_time = dt.fromtimestamp(file.stat().st_mtime)

		if file_mod_time > log['latest_file']:
			logging.info(f"NEW - {file.name} modified {file_mod_time}")

			# update the new_latest_file_time which we'll write to the log at the end:
			new_latest_file_time = max(file_mod_time, new_latest_file_time)

			# copy the image:
			new_path = today / Path(file.stem + '.jpg')
			shutil.copy( file, new_path )
			logging.info("copied!")
			
			## create hash:
			with Image.open(new_path) as image_stream:
				row, col = dhash.dhash_row_col(image_stream)
				img_hash_orig = dhash.format_hex(row, col)
				# decompose into hex digits, then sort and re-encode and combine:
				img_hash = ''.join([hex(item)[2:4] for item in sorted(bytes.fromhex(img_hash_orig))])
				img_hash1 = img_hash.translate(translation_table)
			# don't need to check for existing hash in filename because these are new files
			stem = clean_filename(new_path.stem)
			try:
				new_path.rename(new_path.with_stem(f"{hash_name}{img_hash1}_{stem}"))
				logging.info(f"renamed to {hash_name}{img_hash1}")
			except FileExistsError:
				logging.warning(f"{hash_name}{img_hash1} already exists.")
		else:
			logging.info(f"OLD - {file.name[:20]}..., modified {file_mod_time}")

		# if I wanted to do any sorting based on resolution:

		# img = Image.open(new_path)
		# if img.width > img.height:
		# 	img.show()
		# img.close()

log = {'latest_file': new_latest_file_time }
with open('logs.json', mode = 'w', encoding = 'UTF-8') as log_file:
	json.dump(log,log_file, default = str)
logging.info(f"Adjusted datetime cutoff for new files: {new_latest_file_time}")
