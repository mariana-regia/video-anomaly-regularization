import VideoSequence
import os
import cv2

class VideoDataset:

	def __init__(self, root):

		self.videos = []

		for directory in sorted(os.listdir(root)):

			video_path = os.path.join(root, directory)

			if os.path.isdir(video_path):

				self.videos.append(
					VideoSequence(video_path)
				)

	def __len__(self):
		return len(self.videos)

	def get_video(self, index):
		return self.videos[index]