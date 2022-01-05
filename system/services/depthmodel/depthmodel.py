# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		depthmodel.py
# Description:		Apply depth perception TFLite model

# Code modified from https://tfhub.dev/intel/lite-model/midas/v2_1_small/1/lite/1
# TFLite model used without modification.
# Licenced under MIT License

import cv2
import tflite_runtime.interpreter as tflite
from numpy import float32, uint8, empty, exp

class DepthModel :

	# 2D Gaussian function with std_dev of 70 px and peak at 128
	def _Gaussian2D(self, x, y) :
		var = 70**2
		pk = 128
		return exp(-(((x-pk)**2)/(2*var)+((y-pk)**2)/(2*var)))

	# 2D Gaussian filter for reducing effect of gradient on
	# depth estimation
	def _Gaussian2DFilter(self) :
		filt = empty([256, 256])
		for i in range(0, 256) :
			for j in range(0, 256) :
				filt[i, j] = self._Gaussian2D(i, j)
		return filt

	def __init__(self) :
		self._interpreter = tflite.Interpreter(model_path="model_opt.tflite")
		self._mean = [0.485, 0.456, 0.406]
		self._std = [0.229, 0.224, 0.225]

	# Get depth map from an image
	def RunInference(self, img) :
		# Create input tensor
		img = img / 255.0
		img_input = cv2.resize(img, (256,256), interpolation=cv2.INTER_CUBIC)
		img_input = (img_input - self._mean) / self._std
		reshape_img = img_input.reshape(1,256,256,3)
		tensor = reshape_img.astype(float32)
		# Load model
		self._interpreter.allocate_tensors()
		input_details = self._interpreter.get_input_details()
		output_details = self._interpreter.get_output_details()
		# Inference
		self._interpreter.set_tensor(input_details[0]['index'], tensor)
		self._interpreter.invoke()
		output = self._interpreter.get_tensor(output_details[0]['index'])
		output = output.reshape(256, 256)
		# Downsizing result
		prediction = cv2.resize(output, (4, 4), interpolation=cv2.INTER_NEAREST)
		depth_min = prediction.min()
		depth_max = prediction.max()
		# LiDAR measurement may be useful for following line
		img_out = (255 * (prediction - depth_min) / (depth_max - depth_min)).astype("uint8")

		return img_out
