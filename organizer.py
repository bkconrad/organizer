#!/usr/bin/env python
import os
from audiofile import *
from util import *
if __name__ == "__main__":
	file_list = []
	options = {
			"directory": "."
			}

	# find all files in directory
    # http://stackoverflow.com/questions/120656/directory-listing-in-python
	count = 0
	file_dict = {}
	for dirname, dirnames, filenames in os.walk(options["directory"]):
		for filename in filenames:
			full_path = os.path.join(dirname, filename)
			f = AudioFile(full_path)
			if f.valid:
				count += 1
				file_dict[full_path] = f
				f.pprint()
	if count > 0:
		log("Found %d files", count)
		print file_dict
	else:
		log("No files found")
