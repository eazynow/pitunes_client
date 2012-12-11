import soundcloud
import sys
import random
import pyspeaker
import time
from vlc import Instance

print "Starting piTunes\n"

class piTunesController:


	def __init__(self):
		pyspeaker.initSay()
		print "Init piTunes controller"
		self.client = soundcloud.Client(client_id='8da91e376c359e86e2ef2ea5f3008514')


		self.client = soundcloud.Client(client_id='8da91e376c359e86e2ef2ea5f3008514',
                           client_secret='7b38fab0df5b9d131d388d7118c43467',
                           username='rob.baines@hibu.com',
                           password='pitunes')
		self.still_running = True

		self.instance = Instance("")
		self.player = self.instance.media_player_new()

	def announce_track(self,track):
		self.say("Announce a track %s" % track)

	def call_request_api(self):
		# return dummy request for now

		request = {}
		request['username'] = 'dj hawkins'
		request['search'] = self.default_search
		request['message'] = 'this one is for my mum'

		print request
		return request

	def filler_speech(self):
		self.say("Filler time")

	def play_track(self,track):
		self.say("Play a track")
		try:
			url = track['stream_url']
			
			print "Playing:" + url 

			media = self.instance.media_new(url)

			self.player.set_media(media)
			self.player.play()

			# wait until track completes
			while(self.player.is_playing()):
				# sleep for a bit
				time.sleep(1)

		except NameError:
			print('NameError: %s (%s vs LibVLC %s)' % (sys.exc_info()[1],
					__version__,
					libvlc_get_version()))
			sys.exit(1)

	def say(self, text):
		pyspeaker.say(text, "-ven+m8 -k5 -s150")
		time.sleep(2)

	def run(self):
		print "Starting piTunes controller"
		self.say("Starting piTunes controller")

		while(self.still_running):

			# get next track
			next_track_req = self.call_request_api()

			# if no track suggested
			if(next_track_req==None):
				self.filler_speech()
			else:
				# search soundcloud
				track=self.search_soundcloud(next_track_req['search'])

				if(track==None):
					self.filler_speech()

				# announce track
				self.announce_track(track)
				
				# play track
				self.play_track(track)

				# filler speak
				self.filler_speech()

			# repeat forever?

	def search_soundcloud(self,search):
		# fetch track to stream

		print "Searching for %s" % search
		self.say("Searching for %s" % search)

		tracks = self.client.get('/tracks', q=search)
		if(tracks==None):
			return None

		total_tracks = len(tracks)

		print "Found %d" % total_tracks

		random_id = int(random.random()*total_tracks)
		print "Random_id:" + str(random_id)
		# get the tracks streaming URL
		track = tracks[random_id]

		stream_url = self.client.get(track.stream_url, allow_redirects=False)

		suggested_track = {}
		suggested_track['stream_url']=stream_url.location
		suggested_track['track_details'] = track

		print "Suggested Track"		
		print "==============="		
		title = suggested_track['track_details'].title
		description = suggested_track['track_details'].description



		if title!= None:
			self.say("time to play %s!" % title)
			print "Title:"+title

		if description!= None:
			print "Description:"+description
	
		return suggested_track

	def set_default_search(self,search):
		# fetch track to stream
		self.default_search = search

	
def main():
    controller = piTunesController()   
    default_search = sys.argv[1]
    if(default_search==None):
    	search_arg = "turkish hip hop"
    
    controller.set_default_search(default_search) 
    controller.run()

if  __name__ =='__main__':main()