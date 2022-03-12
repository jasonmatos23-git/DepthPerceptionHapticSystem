# Primary Author:	Cristopher Matos (jasonmatos23@gmail.com)
# Course:			EEL 4915L Senior Design II, UCF Spring 2022
# File name:		depthmodel.py
# Description:		Apply depth perception model

# Code adapted from https://tfhub.dev/intel/lite-model/midas/v2_1_small/1/lite/1
# and https://github.com/alibaba/MNN/blob/master/pymnn/examples/MNNEngineDemo/mobilenet_demo.py.
# Model model_opt.tflite retrieved from https://github.com/isl-org/MiDaS/releases/tag/v2_1,
# and converted to *.mnn

import MNN
import cv2
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
		self._interpreter: MNN.Interpreter = MNN.Interpreter("system/services/depthmodel/model_opt.mnn")
		self._session: MNN.Session = self._interpreter.createSession()
		self._input_tensor: MNN.Tensor = self._interpreter.getSessionInput(self._session)
		self._output_tensor: MNN.Tensor = self._interpreter.getSessionOutput(self._session)
		self._mean: list = [0.485, 0.456, 0.406]
		self._std: list = [0.229, 0.224, 0.225]
		self._resolution: tuple = resolution

	# Get depth map from an image
	def RunInference(self, img: ndarray) -> ndarray:
		# Create input tensor
		img: ndarray = img / 255.0
		img_input: ndarray = cv2.resize(img, (256,256), interpolation=cv2.INTER_CUBIC)
		img_input = (img_input - self._mean) / self._std
		tmp_input: MNN.Tensor = MNN.Tensor((1,256,256,3), MNN.Halide_Type_Float, \
			img_input.astype(float32), MNN.Tensor_DimensionType_Tensorflow)
		# Load input
		self._input_tensor.copyFrom(tmp_input)
		# Inference
		self._interpreter.runSession(self._session)
		# Get output
		tmp_output: MNN.Tensor = MNN.Tensor((256,256), MNN.Halide_Type_Float, \
			empty((1,256,256,1), dtype=float32), MNN.Tensor_DimensionType_Tensorflow)
		self._output_tensor.copyToHostTensor(tmp_output)
		output: ndarray = tmp_output.getNumpyData()
		# Write result for demo
		# depth_min: float32 = output.min()
		# depth_max: float32 = output.max()
		# img_out: ndarray = (255 * (output - depth_min) / (depth_max - depth_min)).astype("uint8")
		# cv2.imwrite("output256.png", img_out)
		# Downsizing result
		output: ndarray = cv2.resize(output, self._resolution, interpolation=cv2.INTER_NEAREST)
		# depth_min: float32 = output.min()
		# depth_max: float32 = output.max()
		# # LiDAR measurement may be useful for following line
		# img_out: ndarray = (255 * (output - depth_min) / (depth_max - depth_min)).astype("uint8")

		return output
