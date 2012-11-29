#!/usr/bin/env python
from mutagen.mp3 import MP3
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
		self.valid = True

		ext = filename.split('.')[-1:][0]
		if ext == 'mp3':
			m = MP3(filename)
			self.title = take_any(m, "TIT1", "TIT2")
			self.artist = take_any(m, "TPE1", "TPE2", "TPE3")
			self.album = take_any(m, "TALB")
		else:
			log("Unknown extension \"%s\" in file \n%s", ext, filename)
			self.valid = False

	def pprint(self):
		print "%s by %s on %s" % (self.title, self.artist, self.album)
