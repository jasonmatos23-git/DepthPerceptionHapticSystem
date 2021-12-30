# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		depthmodel.py
# Description:		Apply depth perception TFLite model

# Code modified from https://tfhub.dev/intel/lite-model/midas/v2_1_small/1/lite/1
# TFLite model used without modification.
# Licenced under MIT License

import cv2
import tflite_runtime.interpreter as tflite
from numpy import float32 as float32, uint8 as uint8, empty as empty

class DepthModel :

	def __init__(self) :
		self.interpreter = tflite.Interpreter(model_path="model_opt.tflite")
		self.mean = [0.485, 0.456, 0.406]
		self.std = [0.229, 0.224, 0.225]

	def RunInference(self, img) :
		cv2.imwrite("input.png", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))	# Writes input image for demonstration

		# input
		img = img / 255.0
		img_input = cv2.resize(img, (256,256), interpolation=cv2.INTER_CUBIC)
		img_input = (img_input - self.mean) / self.std
		reshape_img = img_input.reshape(1,256,256,3)
		tensor = reshape_img.astype(float32)

		# load model
		self.interpreter.allocate_tensors()
		input_details = self.interpreter.get_input_details()
		output_details = self.interpreter.get_output_details()
		input_shape = input_details[0]['shape']

		# inference
		self.interpreter.set_tensor(input_details[0]['index'], tensor)
		self.interpreter.invoke()
		output = self.interpreter.get_tensor(output_details[0]['index'])
		output = output.reshape(256, 256)

		# output file
		#prediction = cv2.resize(output, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC)
		prediction = output
		depth_min = prediction.min()
		depth_max = prediction.max()
		# LiDAR measurement may be useful for following line
		img_out = (255 * (prediction - depth_min) / (depth_max - depth_min)).astype("uint8")

		return img_out
