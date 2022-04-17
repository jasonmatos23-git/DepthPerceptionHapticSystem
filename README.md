# Depth Perception Haptic System (DPHS)
Senior Design II Spring 2022

Department of Electrical and Computer Engineering

Univeristy of Central Florida

**Abstract**: Blind/low-vision individuals typically use canes to navigate their environments. Canes allow for people to check their immediate walking path,
but nothing beyond or above the floor. Our project intends to provide a hands-free alternative to the cane. Robot vision and distance sensors
are combined to create a map of the space in front of the user. This map is then projected on to a vest lined with vibrating motors. Similar
alternatives are either uncomfortable (containing several distance sensors), are not hands-free, or rely on complicated machinery.

## Software Overview
![github_software_overview](https://user-images.githubusercontent.com/58221112/163727501-40fac566-02ba-4580-a344-ebcb86e55d96.png)

The software integrates the Benewake TFMini-S LiDAR (I2C), Raspberry Pi Camera v2 (Legacy stack), and PCA9685 PWM Controller (I2C) on a
custom carryout board for the Raspberry Pi Compute Module 4. The core functionality of the project comes from the Depth Perception Service
which implements a depth inferencing model to relay information about obstacles to the user.

The final version of this project uses [MiDaS v2.1 Small](https://github.com/isl-org/MiDaS/releases/tag/v2_1) created by Ranftl et al. The Tensorflow Lite
version of the model was converted to the MNN framework, and then quantized using [RedWebv1](https://sites.google.com/site/redwebcvpr18/).

![image](https://user-images.githubusercontent.com/58221112/163728304-893168a5-93c9-41f6-80cd-23126a3ffa16.png)

Results of running MiDaS on TFLite, TFLite + XNNPACK delegate, and MNN are provided. The MNN quantized model was generated with the following dataset configuration JSON:
```
{
    "format":"RGB",
    "mean":[123.675,116.28,103.53],
    "normal":[0.01712475,0.017507,0.01742919],
    "width":256,
    "height":256,
    "path":"/home/pi/quantization/Imgs/",
    "feature_quantize_method":"KL",
    "weight_quantize_method":"MAX_ABS"
}
```

## Contributers
- Christa Lawerance (cal47day@gmail.com)
- Cristopher Matos (jasonmatos23@gmail.com)
- Kathryn Pagano (kpagano3179@gmail.com)
- Chad Pauley (chadpauley65@gmail.com)

## References
K. Xian, C. Shen, Z. Cao, “The IEEE Conference on
Computer Vision and Pattern Recognition (CVPR),” 2018.
https://sites.google.com/site/redwebcvpr18/

R. Ranftl, K. Lasinger, D. Hafner, K. Schindler,
and Vladlen Koltun, “Towards Robust Monocular Depth
Estimation: Mixing Datasets for Zero-shot Cross-dataset
Transfer,” 2020 IEEE Transactions on Pattern Analysis and
Machine Intelligence (TPAMI)

## Special Thanks
Thank you to:
- ISL Org for providing MiDaS and its source code.
- Alibaba for the incredible MNN framework.
- Xian and team for providing the RedWeb dataset.
