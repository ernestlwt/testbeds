import os
import cv2
import time
import numpy as np
from VideoGet import VideoStream


class VideoManager:
	def __init__ (self, cams, queueSize=5, writeDir=None, reconnectThreshold=20, max_height=720, videoFile=True):
		self.max_height = max_height
		# self.writeDir = writeDir
		self.num_vid_streams = len(cams)
		self.stopped = True

		self.videos = []

		for cam in cams:
			stream = VideoStream(cam.split("/")[-1], cam, queueSize=queueSize, writeDir=writeDir, reconnectThreshold=reconnectThreshold, videoFile=videoFile)
			self.videos.append({'camName':cam.split("/")[-1], 'stream':stream, 'info':{}, 'blank':[]})

	# def _resize(self, frame):
	# 	height, width = frame.shape[:2]
	# 	if height != self.resize_height or width != self.resize_width:
	# 		# print("Resizing from {} to {}".format((height, width), (resize_height, resize_width)))
	# 		frame = cv2.resize(frame, (self.resize_width, self.resize_height))
	# 	return frame

	def start(self):
		if self.stopped:
			# print('vid manager start')
			for vid in self.videos:
				vid['stream'].start()

			# self.init_src()
			self.stopped = False

	def stop(self):
		if not self.stopped:
			# print('vid manager stop')
			self.stopped = True
			# time.sleep(1)

			for vid in self.videos:
				vid['stream'].stop()
				time.sleep(0.5)

	def init_src(self):
		# print('vid manager init')
		for i, vid in enumerate(self.videos):
			info = vid['stream'].init_src()
			vid['info'] = info

			if info['height'] != 0:
				if len(info) > 0 and len(vid['blank']) == 0:
					# print('writing blank frame')
					# if info['height'] > self.max_height:
					# 	self.resize_height = int(self.max_height)
					# 	self.resize_width = int((float(self.max_height) / info['height'])* info['width'])
					# else:
					self.resize_height = info['height']
					self.resize_width = info['width']

				blank = np.zeros((self.resize_height, self.resize_width, 3), dtype='uint8')
				vid['blank'] = blank

			else:
				fake_height = int(self.max_height)
				fake_width = int(self.max_height*16/9)
				vid['info']['height'] = fake_height
				vid['info']['width'] = fake_width

				blank = np.zeros((fake_height, fake_width, 3), dtype='uint8')
				vid['blank'] = blank

	def update_info(self):
		for i, vid in enumerate(self.videos):
			vid['info'] = vid['stream'].vidInfo

	def getAllInfo(self):
		self.init_src()

		all_info = []
		for vid in self.videos:
			all_info.append(vid['info'])
		return all_info

	def read(self):
		statuses = []
		frames = []

		for vid in self.videos:
			# status = vid['stream'].grabbed
			# statuses.append(status)

			# if status:
			if not vid['stream'].more():
				frames.append(vid['blank'])
				statuses.append(False)
			else:
				frame = vid['stream'].read()
				# frames.append(self._resize(frame))
				frames.append(frame)
				statuses.append(True)

		return statuses, frames