# pyspeaker.py
""" PySpeaker2 - a modified version of a python wrapper for espeak, initially by David Worrall.
"""

import os
def initSay():
	""" makes a fifo in /tmp to carry tts data to /usr/locl/speak"""
	try:
		if not "speakFIFO" in os.listdir("/tmp"):
			os.mkfifo("/tmp/speakFIFO", 0666)	    # make an explicit pipe
			print "made FIFO in /tmp"
	except error:
		print " couldn't create fifo in /tmp"

def say(text="", options = ""):
	""" Gets speak to say the string text.
	options := a string of command-line options to speak. Any combination of the following:
	-a<n> (200<=n>=0) amplitude, default = 100
	-f<text file> Textfile to speak. NB don't put quotes around filename
	-k<n> Indicate capital letters with n=1:sound, n=2: the word "capitals"
	n>2 raise pitch for capital (try -k20)
	-m interpret SSML markup and ignore other tags
	-p<n> (99<=n>=0) pitch, default = 50
	-s<n> speed in words/minute, default = 170
	-v<name> use voice "name"
	-x write mnemonics to stdout
	-X write mnemonics and translation trace to stdout
	--punc speak the names of punctuation chars wen speaking
	--voices <lang> List all the available voices for language <lang> """

	os.system( "(/usr/bin/espeak " + options +") < /tmp/speakFIFO &")
	# os.system("(echo 'No apostrophies pleese.') > /tmp/speakFIFO &")
	os.system("(echo " + text + ") > /tmp/speakFIFO &")


def cleanupSay():
	""" removes the fifo to speak"""
	os.remove("/tmp/speakFIFO")

#to use:
#initSay()
#say("Gudday mayte. Use the python help function to display options for the say command.", "-ven+m8 -k5 -s150")
# cleanupSay()
