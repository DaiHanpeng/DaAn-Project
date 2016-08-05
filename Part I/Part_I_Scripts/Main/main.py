import os
import os.path
import shutil
import threading
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import time

logging.basicConfig(filename='apscheduler.log',level=logging.DEBUG)

def processPart1_1():
	command_part1_starter = r'start /MIN python "C:\\DaAn\\0804\\Part I\\TimingScanner\\CalibrationTimingScanner.py"'
	os.system(command_part1_starter)

def processPart1_2():
	command_part1_starter = r'start /MIN python "C:\\DaAn\\0804\\Part I\\TimingScanner\\ControlTimingScanner.py"'
	os.system(command_part1_starter)

def processPart1_3():
	command_part1_starter = r'start /MIN python "C:\\DaAn\\0804\\Part I\\TimingScanner\\MtdResultTimingScanner.py"'
	os.system(command_part1_starter)

def processPart1_4():
	command_part1_starter = r'start /MIN python "C:\\DaAn\\0804\\Part I\\TimingScanner\\PrintedReagentTimingScanner.py"'
	os.system(command_part1_starter)

def processPart1_5():
	command_part1_starter = r'start /MIN python "C:\\DaAn\\0804\\Part I\\TimingScanner\\ErrorReportTimingScanner.py"'
	os.system(command_part1_starter)


def processPart1():
		t1 = threading.Thread(target=processPart1_1)
		t2 = threading.Thread(target=processPart1_2)
		t3 = threading.Thread(target=processPart1_3)
		t4 = threading.Thread(target=processPart1_4)
		t5 = threading.Thread(target=processPart1_5)

		t1.start()
		t2.start()
		t3.start()
		t4.start()
		t5.start()
	
def processKiller():
	command_simulator = "taskkill /t /f /im HRSTART.exe"
	os.system(command_simulator)
	
def processCopier():
	print 'copiser start...'
	src = "z:\\"
	dst = "c:\\A002\\"
	max_delay = timedelta(minutes=1)
	
	if os.path.exists(src):
		for dir in os.listdir(src):
			
			src_dir_path = os.path.join(src,dir)
			dst_dir_path = os.path.join(dst,dir)
			if(not os.path.exists(dst_dir_path)):
				os.mkdir(dst_dir_path)
			if (r"LOG" == dir) or (r"PCIDRV" == dir) or (r"TOOLS" == dir):
				continue
			for file in os.listdir(src_dir_path):
				src_file_path = os.path.join(src_dir_path,file)
				dst_file_path = os.path.join(dst_dir_path,file)
				if os.path.isfile(dst_file_path):
					sfile_mod_time = datetime.fromtimestamp(os.stat(src_file_path).st_mtime)
					dfile_mod_time = datetime.fromtimestamp(os.stat(dst_file_path).st_mtime)
					if sfile_mod_time - dfile_mod_time > max_delay: 
						shutil.copy2(src_file_path, dst_dir_path)
						print str(file) + '\t added.'
				else: 
					shutil.copy2(src_file_path, dst_dir_path)
					print str(file) + '\t updated.'
	print 'folder copy finished.'

def reagent():
	print 'run auto it reagent...'
	command_autoit = "autoit3 C:\\DaAn\\AutoIT_Scripts\\reagent.au3"
	os.system(command_autoit)
	
def calibation():
	print 'run auto it calibation...'
	command_autoit = "autoit3 C:\\DaAn\\AutoIT_Scripts\\RTCalibration0.au3"
	os.system(command_autoit)
	
def control():
	print 'run auto it control...'
	command_autoit = "autoit3 C:\\DaAn\\AutoIT_Scripts\\RTControl.au3"
	os.system(command_autoit)

def error_report():
	print 'run auto it error_report...'
	command_autoit = "autoit3 C:\\DaAn\\AutoIT_Scripts\\ErrorReport.au3"
	os.system(command_autoit)
			
def processChecker():
	command_remote = 'pslist \\\\10.10.10.100 -u bmuser -p bmuser HRSTART'
	#if os.system(command_remote) == 0:
	if 1:
		try:
			print 'apscheduler run:'
			print time.localtime(time.time())		
			processKiller()
			processCopier()
			reagent()
			calibation()
			control()
			error_report()
		except Exception as ex:
			print ex
	
processChecker()	
processPart1()
sched = BlockingScheduler()
sched.add_job(processChecker, 'interval', seconds = 200)
sched.start()
