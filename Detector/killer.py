import os
import psutil

def measure_bytes(process):
	f = open("bytes.txt", "a")
	f.write(str(process.io_counters().write_bytes//1048576) + "\n")
	f.close()

def add_pid(proc, critical_paths):
	if "Downloads" in proc.exe():
		return True
	for path in critical_paths:
		if path in proc.exe():
			return True

def sort_by_read_bytes(processes):
	for i in range(1, len(processes)):
		for j in range(0, len(processes) - i - 1):
			try:
				if processes[j].io_counters().read_bytes < processes[j + 1].io_counters().read_bytes:
					temp = processes[j]
					processes[j] = processes[j+1]
					processes[j+1] = temp
			except:
				pass
	return processes

def sort_by_write_bytes(processes):
	for i in range(1, len(processes)):
		for j in range(0, len(processes) - i - 1):
			try:
				if processes[j].io_counters().write_bytes < processes[j + 1].io_counters().write_bytes:
					temp = processes[j]
					processes[j] = processes[j+1]
					processes[j+1] = temp
			except:
				pass
	return processes

def check_word_whitelist(processes, word_whitelist):

	filtered_processes = list()
	match = False

	for proc in processes:
		if proc.exe() not in ["", "Registry"]:
			for word in word_whitelist:
				if word in proc.exe():
					match = True
			if match == False:
				filtered_processes.append(proc)
			match = False

	return filtered_processes

def check_word_blacklist(processes, word_blacklist):

	blacklist = list()
	suspiciouslist = list()
	match = False

	for proc in processes:
		for word in word_blacklist:
			if word in proc.exe():
				match = True
		if match == True:
			blacklist.append(proc)
		else:
			suspiciouslist.append(proc)
		match = False

	return [blacklist, suspiciouslist]

def get_processes(sort):
	processes = []

	for proc in psutil.process_iter(['pid', 'name']):
		try:
			processes.append(proc)
		except:
			pass
	
	if sort == "r":
		processes = sort_by_read_bytes(processes)
	elif sort == "w":
		processes = sort_by_write_bytes(processes)
		
	#measure_bytes(process)
	
	return processes


def kill_and_delete(word_whitelist, word_blacklist):
    
	processes = get_processes("w")
	processes = check_word_whitelist(processes[0:20], word_whitelist)
	lists = check_word_blacklist(processes, word_blacklist)
	blacklist = lists[0]
	suspiciouslist = lists[1]

	deleted_paths = []
	to_delete_paths = []

	for proc in blacklist:
		path = proc.exe()
		proc.kill()
		try:
			os.chmod(path, 0o777)
			os.remove(path)
			deleted_paths.append(path)
		except:
			if path not in to_delete_paths:
				to_delete_paths.append(path)
	
	to_check_paths = []

	for proc in suspiciouslist:
		to_check_paths.append(proc.exe())
		proc.kill()
	
	if len(deleted_paths) == 0 and len(to_delete_paths) == 0 and len(to_check_paths) == 0:
		return False
	return {"deleted":deleted_paths, "to_delete": to_delete_paths, "to_check":to_check_paths}

