import os
import cv2

class VideoSequence:

	def __init__(self, video_path):

		self.video_path = video_path

		self.frame_paths = sorted(
			[
				os.path.join(video_path, file)
				for file in os.listdir(video_path)
				if file.endswith(".jpg")
			]
		)

	def __len__(self):
		return len(self.frame_paths)

	def get_frame(self, index):
		return cv2.imread(self.frame_paths[index])

	def get_frame_path(self, index):
		return self.frame_paths[index]