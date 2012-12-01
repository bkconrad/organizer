#!/usr/bin/env python
import pprint
import re
import string
import os
import argparse
from audiofile import *
from util import *

pp = pprint.PrettyPrinter(indent=2)

class CleanerLeaf:
	def __init__(self, dirty):
		exclude = set(string.punctuation)
		self.dirty = dirty
		self.clean = ''.join(ch for ch in dirty.lower().strip() if ch not in exclude)
		self.clean = re.sub(r'\s+', ' ', self.clean)
	def __repr__(self):
		return "%s (%s)" % (self.dirty, self.clean)

def aggregate(file_dict, field = "artist"):
	master_dict = {}

	# find the clean name for each file
	for k in file_dict:
		# make a sub dict to use as the value
		master_dict[k] = CleanerLeaf(getattr(file_dict[k], field))

	# count the number of times each dirty name is used for each clean name
	count_dict = {}
	for k in master_dict:
		dirty = master_dict[k].dirty
		clean = master_dict[k].clean
		if count_dict.has_key(clean):
			if count_dict[clean].has_key(dirty):
				count_dict[clean][dirty] += 1
			else:
				count_dict[clean][dirty] = 1
		else:
			count_dict[clean] = {}
	
	# for each clean name, find the most common dirty name
	name_map = {}
	for clean in count_dict:
		best_count = 0
		best_name = clean
		for dirty in count_dict[clean]:
			if count_dict[clean][dirty] > best_count:
				best_count = count_dict[clean][dirty]
				best_name = dirty
		name_map[clean] = best_name

	# update all files with the same clean name to have the same dirty name
	for k in file_dict:
		if getattr(file_dict[k], field) != name_map[master_dict[k].clean]:
			print("'%s' -> '%s'" % (getattr(file_dict[k], field), name_map[master_dict[k].clean]))
			setattr(file_dict[k], field, name_map[master_dict[k].clean])

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = """
	Audio file mass tagger, renamer, and organizer
	""")
	parser.add_argument('-m', '--move', dest='operation', action='store_const', const='move', default='none')
	parser.add_argument('-c', '--copy', dest='operation', action='store_const', const='copy')
	parser.add_argument('-i', '--idir', '--inputdir', dest='inputdir', default='.', required=False)
	parser.add_argument('-o', '--odir', '--outputdir', dest='outputdir', action='store', default='.', nargs=1)
	parser.add_argument('-f', '--fuzzy', choices=['artist', 'album'], nargs='+', action='store', default=[]) 
	options = parser.parse_args()

	# find all files in directory
    # http://stackoverflow.com/questions/120656/directory-listing-in-python
	count = 0
	file_dict = {}
	for dirname, dirnames, filenames in os.walk(options.inputdir):
		for filename in filenames:
			full_path = os.path.join(dirname, filename)
			f = AudioFile(full_path)
			if f.valid:
				count += 1
				file_dict[full_path] = f
	if count > 0:
		log("Found %d files", count)
	else:
		log("No files found")

	# aggregate artist and albums
	if 'artist' in options.fuzzy:
		aggregate(file_dict, "artist")
	if 'album' in options.fuzzy:
		aggregate(file_dict, "album")
	
	# create folder structure
	if options.operation in ['move', 'copy']:
		# first build a tree
		# structure is { artist: { album: ["songfile", ...] } }
		tree = {}
		for fn in file_dict:
			artist = file_dict[fn].artist
			album = file_dict[fn].album
			if artist in tree:
				if album in tree[artist]:
					tree[artist][album].append(fn)
				else:
					tree[artist][album] = []
			else:
				tree[artist] = {}

		pp.pprint(tree)
