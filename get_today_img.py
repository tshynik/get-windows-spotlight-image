import shutil
from pathlib import Path
# from PIL import Image 
import subprocess
from datetime import datetime as dt
import json

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

logging.info(f"NEW RUN")

# where to get the files:
windows_folder = Path.home() / Path("AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets")
logging.info(f"Looking here: {windows_folder}")

# where to save the files:
today = Path('today')

# get date from latest files, or create the JSON if it doesn't exist yet.
try:
	with open('logs.json', mode = 'r') as log_file:
		log = json.load(log_file)
		# because it's written to JSON as a string, got to parse it:
		log['latest_file'] = dt.strptime(log['latest_file'],'%Y-%m-%d %H:%M:%S.%f')
except:
	log = {'latest_file': dt(1969, 1, 1) }

new_latest_file_time = log['latest_file']
logging.info(f"Only looking for new files since {new_latest_file_time}")

# list all the files in the Windows folder:
windows_folder_files = list(windows_folder.glob('**/*'))

for file in windows_folder_files:

	# print(file.name)
 
	if file.stat().st_size > 300000:
		# get file name and modification time:
		file_mod_time = dt.fromtimestamp(file.stat().st_mtime)

		if file_mod_time > log['latest_file']:
			logging.info(f"NEW - {file.name} modified {file_mod_time}")

			# update the new_latest_file_time which we'll write to the log at the end:
			if(file_mod_time > new_latest_file_time):
				new_latest_file_time = file_mod_time

			# copy the image:
			new_path = today / Path(file.name + '.jpg')
			shutil.copy2( file, new_path )
			logging.info("copied!")
		else:
			logging.info(f"OLD - {file.name} modified {file_mod_time}")
		
		# if I wanted to do any sorting based on resolution:
  
		# img = Image.open(new_path)
		# if img.width > img.height:
		# 	img.show()
		# img.close()

log = {'latest_file': new_latest_file_time }
with open('logs.json', mode = 'w') as log_file:
    json.dump(log,log_file, default = str)
logging.info(f"Adjusted datetime cutoff for new files: {new_latest_file_time}")
	
# open Windows Explorer at the end to review:
subprocess.Popen(fr'explorer /select,"{today.resolve()}"')


## TODO: checking for duplicates with the same name: MD5 hash? But I think they're already hashed, must be subtle differences. Hm.
# import hashlib
# hash = hashlib.MD5(your_text_here).hexdigest()
