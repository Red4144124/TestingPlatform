#!/usr/bin/env python3

# Copyright 2023 RnD Center "ELVEES", JSC

import time
import json
import subprocess
import os
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

time_of_test = 60 #seconds
full_cpuload = 'y'
max_cpu_temp = 90

def full_load():
	for i in range(10):
		os.system("yes > /dev/null&")

def stop_full_load():
	os.system("killall yes")

def main(argv):
	f = open(argv[0], "w")
	current_sec = 0
	start_time = int(time.time())
	if 'y' == full_cpuload:
		full_load()
	while current_sec < time_of_test:
		current_sec = int(time.time())- start_time
		sensors_get = subprocess.run(['sensors', '-j'], stdout=subprocess.PIPE)
		cputemp = json.loads(sensors_get.stdout.decode('utf-8'))['coretemp-isa-0000']['Core 0']['temp2_input']		#for x86
		#cputemp = json.loads(sensors_get.stdout.decode('utf-8'))['mcom03-isa-0000']['cpu']['temp1_input']			#for mcom03
		output_str = f"{current_sec} {cputemp}\n"
		print(output_str)
		f.write(output_str)
		if cputemp >= max_cpu_temp:
			print("Dangerous, overheating!!!")
			break
		time.sleep(1)
	if 'y' == full_cpuload:
		stop_full_load()
	f.close()
	os.system("sync")

if __name__ == "__main__":
	main(sys.argv[1:])