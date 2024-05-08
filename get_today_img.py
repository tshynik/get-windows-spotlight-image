import shutil
from pathlib import Path
# from PIL import Image 
import subprocess
from datetime import datetime as dt

# where to get the files:
windows_folder = Path.home() / Path("AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets")
print(windows_folder)

# where to save the files:
today = Path('all/today')
# print(today.resolve())


# list all the files in the Windows folder:
windows_folder_files = list(windows_folder.glob('**/*'))

for file in windows_folder_files:

	# print(file.name)
 
	if file.stat().st_size > 400000:
		print(file.name)
		print(dt.fromtimestamp(file.stat().st_mtime))
		new_path = today / Path(file.name + '.jpg')
		shutil.copy2( file, new_path )
		print("copied!")
		
		# if I wanted to do any sorting based on resolution:
  
		# img = Image.open(new_path)
		# if img.width > img.height:
		# 	img.show()
		# img.close()

# open Windows Explorer at the end to review:
subprocess.Popen(fr'explorer /select,"{today.resolve()}"')


## TODO: checking for duplicates with the same name: MD5 hash? But I think they're already hashed, must be subtle differences. Hm.
# import hashlib
# hash = hashlib.MD5(your_text_here).hexdigest()
