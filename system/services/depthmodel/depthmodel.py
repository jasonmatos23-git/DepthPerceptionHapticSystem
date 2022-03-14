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
import numpy as np

class DepthModel :

	# 2D Gaussian function
	def _Gaussian2D(self, x: int, y: int, peak: np.float32, std_dev: np.float32) -> np.float32:
		var: np.float32 = std_dev**2
		return np.exp(-(((x-peak)**2)+((y-peak)**2))/(2*var)).astype(np.float32)

	# 2D Gaussian filter to implement receptive fields
	def _Gaussian2DFilter(self, shape: tuple, peak: np.float32, std_dev: np.float32) -> np.ndarray:
		filt: np.ndarray = np.empty(shape)
		i: int
		j: int
		for i in range(0, shape[0]) :
			for j in range(0, shape[1]) :
				filt[i, j] = self._Gaussian2D(i, j, peak, std_dev)
		# min-max normalization to ensure max value is 1
		filt_max: np.float32 = filt.max()
		filt_min: np.float32 = filt.min()
		return (filt-filt_min)/(filt_max-filt_min)

	# Creates 3 kernels corresponding to 9 PWMs
	def _createFilters(self, Gaussian: np.ndarray) :
		lsplit, rsplit = np.hsplit(Gaussian, 2)
		sides: np.ndarray = np.concatenate((rsplit, lsplit), 1)
		tsplit, bsplit = np.vsplit(Gaussian, 2)
		bounds: np.ndarray = np.concatenate((bsplit, tsplit))
		tsplit, bsplit = np.vsplit(sides, 2)
		corners: np.ndarray = np.concatenate((bsplit, tsplit))
		return corners, sides, bounds

	def __init__(self) -> None:
		self._interpreter: MNN.Interpreter = MNN.Interpreter("system/services/depthmodel/model_opt.mnn")
		self._session: MNN.Session = self._interpreter.createSession()
		self._input_tensor: MNN.Tensor = self._interpreter.getSessionInput(self._session)
		self._output_tensor: MNN.Tensor = self._interpreter.getSessionOutput(self._session)
		self._mean: list = [0.485, 0.456, 0.406]
		self._std: list = [0.229, 0.224, 0.225]
		self._Gaussian: np.ndarray = self._Gaussian2DFilter((32,32), 15.5, 10)
		self._corners, self._sides, self._bounds = \
			self._createFilters(self._Gaussian)

	# Get depth map from an image
	def RunInference(self, img: np.ndarray) -> np.ndarray:
		# Create input tensor
		img: np.ndarray = img / 255.0
		img_input: np.ndarray = cv2.resize(img, (256,256), interpolation=cv2.INTER_CUBIC)
		img_input = (img_input - self._mean) / self._std
		tmp_input: MNN.Tensor = MNN.Tensor((1,256,256,3), MNN.Halide_Type_Float, \
			img_input.astype(np.float32), MNN.Tensor_DimensionType_Tensorflow)
		# Load input
		self._input_tensor.copyFrom(tmp_input)
		# Inference
		self._interpreter.runSession(self._session)
		# Get output
		tmp_output: MNN.Tensor = MNN.Tensor((256,256), MNN.Halide_Type_Float, \
			np.empty((1,256,256,1), dtype=np.float32), MNN.Tensor_DimensionType_Tensorflow)
		self._output_tensor.copyToHostTensor(tmp_output)
		output: np.ndarray = tmp_output.getNumpyData()
		# Write result for demo
		# depth_min: np.float32 = output.min()
		# depth_max: np.float32 = output.max()
		# img_out: np.ndarray = (255 * (output - depth_min) / (depth_max - depth_min)).astype("uint8")
		# cv2.imwrite("output256.png", img_out)
		# Downsizing result
		output: np.ndarray = cv2.resize(output, (32,32), interpolation=cv2.INTER_LINEAR)
		# depth_min: np.float32 = output.min()
		# depth_max: np.float32 = output.max()
		# Apply kernels
		corner: np.ndarray = output * self._corners
		side: np.ndarray = output * self._sides
		bound: np.ndarray = output * self._bounds
		center: np.ndarray = output * self._Gaussian
		# Maxpool in to 3x3 result
		output = np.array([
			[corner[0:16, 0:16].max(), bound[0:16].max(), corner[0:16, 16:32].max()], \
			[side[:,0:16].max(), center.max(), side[:,16:32].max()], \
			[corner[16:32, 0:16].max(), bound[16:32].max(), corner[16:32, 16:32].max()]
		])
		# # LiDAR measurement may be useful for following line
		# img_out: np.ndarray = (255 * (output - depth_min) / (depth_max - depth_min)).astype("uint8")

		return output
