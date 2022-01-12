# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		depthmodel.py
# Description:		Apply depth perception TFLite model

# Code modified from https://tfhub.dev/intel/lite-model/midas/v2_1_small/1/lite/1
# TFLite model used without modification.
# Licenced under MIT License

import cv2
import tflite_runtime.interpreter as tflite
from numpy import float32, uint8, empty, exp, ndarray

class DepthModel :

	# 2D Gaussian function with std_dev of 70 px and peak at 128
	def _Gaussian2D(self, x, y) -> float32:
		var: int = 70**2
		pk: int = 128
		return exp(-(((x-pk)**2)/(2*var)+((y-pk)**2)/(2*var))).astype(float32)

	# 2D Gaussian filter for reducing effect of gradient on
	# depth estimation
	def _Gaussian2DFilter(self) -> ndarray:
		filt: ndarray = empty([256, 256])
		i: int
		j: int
		for i in range(0, 256) :
			for j in range(0, 256) :
				filt[i, j] = self._Gaussian2D(i, j)
		return filt

	def __init__(self, resolution: tuple) -> None:
		self._interpreter: tflite.Interpreter = tflite.Interpreter(model_path="system/services/depthmodel/model_opt.tflite")
		self._mean: list = [0.485, 0.456, 0.406]
		self._std: list = [0.229, 0.224, 0.225]
		self._resolution: tuple = resolution

	# Get depth map from an image
	def RunInference(self, img: ndarray) -> ndarray:
		# Create input tensor
		img: ndarray = img / 255.0
		img_input: ndarray = cv2.resize(img, (256,256), interpolation=cv2.INTER_CUBIC)
		img_input = (img_input - self._mean) / self._std
		tensor: ndarray = img_input.reshape(1,256,256,3).astype(float32)
		# Load model
		self._interpreter.allocate_tensors()
		input_details: list = self._interpreter.get_input_details()
		output_details: list = self._interpreter.get_output_details()
		# Inference
		self._interpreter.set_tensor(input_details[0]['index'], tensor)
		self._interpreter.invoke()
		output: ndarray = self._interpreter.get_tensor(output_details[0]['index'])
		output = output.reshape(256, 256)
		# Writing result for demo
		depth_min: float32 = output.min()
		depth_max: float32 = output.max()
		img_out: ndarray = (255 * (output - depth_min) / (depth_max - depth_min)).astype("uint8")
		cv2.imwrite("output256.png", img_out)
		# Downsizing result
		prediction: ndarray = cv2.resize(output, self._resolution, interpolation=cv2.INTER_NEAREST)
		depth_min: float32 = prediction.min()
		depth_max: float32 = prediction.max()
		# LiDAR measurement may be useful for following line
		img_out: ndarray = (255 * (prediction - depth_min) / (depth_max - depth_min)).astype("uint8")

		return img_out
