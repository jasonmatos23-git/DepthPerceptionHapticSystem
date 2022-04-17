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

	# Maxpool uses 85x85 kernel on 256x256 image ignoring
	# right and bottom-most pixels.
	def maxpool(self, array) -> np.ndarray:
		res: np.ndarray = np.empty((3,3))
		for i in range(0, 3) :
			for j in range(0, 3) :
				res[i,j] = array[i*85:(i+1)*85, j*85:(j+1)*85].max()
		return res

	# Locks map values to previous value unless decreased to zero.
	# Set the output map to 0 if the input map is set to 0.
	# Otherwise, only allow increases to the depth map.
	def schmitt_trigger(self, array_in: np.ndarray) -> np.ndarray:
		temp: np.ndarray = array_in - self._history
		self._history = self._history * (array_in != 0) + (temp > 0) * temp
		return self._history

	def __init__(self) -> None:
		self._interpreter: MNN.Interpreter = MNN.Interpreter("system/services/depthmodel/model_opt_uint8.mnn")
		self._session: MNN.Session = self._interpreter.createSession()
		self._input_tensor: MNN.Tensor = self._interpreter.getSessionInput(self._session)
		self._output_tensor: MNN.Tensor = self._interpreter.getSessionOutput(self._session)
		self._mean: list = [0.485, 0.456, 0.406]
		self._std: list = [0.229, 0.224, 0.225]
		self._exp_mean = 700.0		# Experimentally determined mean (very roughly 2 meters)
		self._exp_maximum = 1200.0	# Experimentally determined maximum estimated closeness
		self._exp_N_levels = 4		# Discrete levels of output on [0, N)
		# Floor, edge, and cieling box filter
		grad_magnitude: np.ndarray = 900.0	# Experimentally estimated floor gradient magnitude
		ramp: np.ndarray = np.pad(np.ones((140,192)), ((32,84),(32,32)), mode='linear_ramp', end_values=0)
		self._floor_filter: np.ndarray = (1 - ramp) * grad_magnitude
		# History for Schmitt-like trigger
		self._history: np.ndarray = np.zeros((3,3))

	# Get depth map from an image
	def RunInference(self, img: np.ndarray) -> np.ndarray:
		# Run CNN model
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
		# Remove floor and clip
		output = output - self._floor_filter
		clipped: np.ndarray = np.clip(output, self._exp_mean, self._exp_maximum)
		# Discretize
		discrete: np.ndarray = self._exp_N_levels * ((clipped - self._exp_mean)/ \
			(1 + self._exp_maximum - self._exp_mean))
		# Maxpool floored on [0, self._exp_N_levels)
		maxpooled: np.ndarray = np.floor(self.maxpool(discrete))
		# Schmitt trigger
		schmitt: np.ndarray = self.schmitt_trigger(maxpooled)
		# Return percentage of haptic response
		return schmitt/(self._exp_N_levels - 1)
