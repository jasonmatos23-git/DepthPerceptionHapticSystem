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

	def RunInference(self, img) :
		cv2.imwrite("input.png", img)	# Writes input image for demonstration

		# input
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) / 255.0

		img_resized = cv2.resize(img, (256,256), interpolation=cv2.INTER_CUBIC)
		img_input = img_resized
		mean = [0.485, 0.456, 0.406]
		std = [0.229, 0.224, 0.225]
		img_input = (img_input - mean) / std
		reshape_img = img_input.reshape(1,256,256,3)

		tensor = reshape_img.astype(float32)

		# load model
		interpreter = tflite.Interpreter(model_path="model_opt.tflite")
		interpreter.allocate_tensors()
		input_details = interpreter.get_input_details()
		output_details = interpreter.get_output_details()
		input_shape = input_details[0]['shape']

		# inference
		interpreter.set_tensor(input_details[0]['index'], tensor)
		interpreter.invoke()
		output = interpreter.get_tensor(output_details[0]['index'])
		output = output.reshape(256, 256)

		# output file
		prediction = cv2.resize(output, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC)
		print(" Write image to: output.png")
		depth_min = prediction.min()
		depth_max = prediction.max()
		img_out = (255 * (prediction - depth_min) / (depth_max - depth_min)).astype("uint8")

		return img_out
