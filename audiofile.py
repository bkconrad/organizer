#!/usr/bin/env python
import os
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.easyid3 import EasyID3
from util import *

class AudioFile:

	def __init__(self, filename):

		# some of the keys contain a copyright character (0xA9)
		MP4_map = {
			"\xa9nam" : "title",
			"\xa9ART" : "artist",
			"\xa9alb" : "album"
		}

		self.title = None
		self.album = None
		self.artist = None
		self.tracknumber = None
		self.valid = True

		ext = filename.split('.')[-1:][0]
		if ext == 'm4a' or ext == 'mp4':
			m = MP4(filename)
			# for each key (atom name) set an attribute on self with a name
			# that matches the atom's name's corresonding value in MP4_map and
			# a value equal to the stripped contents of that atom
			# (i.e. route atom contents to attributes on self)
			for k in MP4_map:
				try:
					setattr(self, MP4_map[k], m[k][0].strip())
				except KeyError:
					pass
		elif ext == 'mp3':
			m = MP3(filename, ID3=EasyID3)
			for k in ["title", "artist", "album", "tracknumber"]:
				try:
					setattr(self, k, m[k][0].strip())
				except KeyError:
					pass
		else:
			# not recognized
			self.valid = False

		if self.title == None:
			# just the filename if all else fails
			self.title = os.path.basename(filename).split(".")[-2:][0]

	def pprint(self):
		print "%s by %s on %s" % (self.title, self.artist, self.album)
