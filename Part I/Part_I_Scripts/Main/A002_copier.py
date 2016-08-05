import os
import os.path
import shutil
import threading
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import time


def processCopier():
	#src = "z:\\"
	dst = "c:\\A002\\"
	src = r'C:\A002_Not_Updated'
	#dst = r'C:\Test_Update'
	
	max_delay = timedelta(minutes=1)
	
	if os.path.exists(src):
		for dir in os.listdir(src):
			
			src_dir_path = os.path.join(src,dir)
			dst_dir_path = os.path.join(dst,dir)
			if(not os.path.exists(dst_dir_path)):
				os.mkdir(dst_dir_path)
			if (r"LOG" == dir) or (r"PCIDRV" == dir) or (r"TOOLS" == dir):
				continue
			for files in os.listdir(src_dir_path):
				src_file_path = os.path.join(src_dir_path,files)
				dst_file_path = os.path.join(dst_dir_path,files)
				if os.path.isfile(dst_file_path):
					sfile_mod_time = datetime.fromtimestamp(os.stat(src_file_path).st_mtime)
					dfile_mod_time = datetime.fromtimestamp(os.stat(dst_file_path).st_mtime)
					if sfile_mod_time - dfile_mod_time > max_delay: 
						shutil.copy2(src_file_path, dst_dir_path)
				else: 
					shutil.copy2(src_file_path, dst_dir_path)
					
processCopier()