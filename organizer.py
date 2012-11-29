#!/usr/bin/env python
import os
from metamut import *
from util import *
if __name__ == "__main__":
	file_list = []
	options = {
			"directory": "."
			}

	# find all files in directory
    # http://stackoverflow.com/questions/120656/directory-listing-in-python
	count = 0
	for dirname, dirnames, filenames in os.walk(options["directory"]):
		for filename in filenames:
			f = AudioFile(os.path.join(dirname, filename))
			count += 1
			if f.valid:
				f.pprint()
	log("Found %d files", count)
