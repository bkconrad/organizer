#!/usr/bin/env python
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from util import *
# return the value of the first key in the given list which exists in arr
def take_any(arr, *args):
	for k in args:
		if arr.has_key(k):
			return arr[k]
	
class AudioFile:
	def __init__(self, filename):
		self.title = None
		self.album = None
		self.artist = None
		self.track = None
		self.valid = True

		ext = filename.split('.')[-1:][0]
		if ext == 'mp3':
			m = MP3(filename, ID3=EasyID3)
			try:
				self.title = m["title"][0]
			except:
				pass
			try:
				self.album = m["album"][0]
			except:
				pass
			try:
				self.artist = m["artist"][0]
			except:
				pass
			try:
				self.track = m["track"][0]
			except:
				pass
		else:
			log("Unknown extension \"%s\" in file \n%s", ext, filename)
			self.valid = False

		if self.title == None:
			# just the filename if all else fails
			self.title = os.path.basename(filename).split(".")[-2:][0]

	def pprint(self):
		print "%s by %s on %s" % (self.title, self.artist, self.album)
