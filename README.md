# Depth Estimation for Colonoscopy Images with Self-supervised Learning from Videos
## Abstract
Depth estimation in colonoscopy images provides geometric
clues for downstream medical analysis tasks, such as polyp detection,
3D reconstruction, and diagnosis. Recently, deep learning technology
has made significant progress in monocular depth estimation for nat-
ural scenes. However, without sufficient ground truth of dense depth
maps for colonoscopy images, it is signicantly challenging to train deep
neural networks for colonoscopy depth estimation. In this paper, we pro-
pose a novel approach that makes full use of both synthetic data and real
colonoscopy videos.We use synthetic data with ground truth depth maps
to train a depth estimation network with a generative adversarial network
model. Despite the lack of ground truth depth, real colonoscopy videos
are used to train the network in a self-supervision manner by exploiting 
temporal consistency between neighboring frames. Furthermore, we
design a masked gradient warping loss in order to ensure temporal consis-
tency with more reliable correspondences. We conducted both quantita-
tive and qualitative analysis on an existing synthetic dataset and a set of
real colonoscopy videos, demonstrating the superiority of our method on
more accurate and consistent depth estimation for colonoscopy images.

[In MICCAI 2021].  

## Prerequisites
- Linux
- Python 3, pytorch1.4
- NVIDIA GPU (11G memory or larger) + CUDA cuDNN

## Plan
We will clean the code and write more detailed instruction soon. 

### Testing
- Test the model (`bash ./scripts/test.sh`):
```bash
#!./scripts/test.sh
python syn_test.py --name colon2depth_512p --no_instance --label_nc 0
```

### Dataset
- For synthetic data, you can download from http://cmic.cs.ucl.ac.uk/ColonoscopyDepth/.
- For real dataset, you can download from https://github.com/dashishi/LDPolypVideo-Benchmark. This is our raw data, the data used for training is the subset of it. We crop the raw image to remove the black corner.

### Multi-GPU training
- Train a model using multiple GPUs (`bash ./scripts/train.sh`):
```bash
#!./scripts/train.sh
python train.py --name colon2depth_512p --batchSize 8 --gpu_ids 1,2 --label_nc 0 --no_instance --tf_log --no_vgg_loss --continue_train```
```

### Citations
The following sources were used as baseline for our research work: 

```

Kai Cheng, Yiting Ma, Bin Sun, Yang Li, and Xuejin Chen, et al. Depth Estimation
for Colonoscopy Images with Self-supervised Learning from Videos. National
Engineering Laboratory for Brain-inspired Intelligence Technology and
Application, University of Science and Technology of China, Hefei, China, 2021.
MICCAI 2021:
https://miccai2021.org/openaccess/paperlinks/2021/09/01/143-Paper0443.html

Boykov, Yuri Y., and M-P. Jolly. "Interactive graph cuts for optimal boundary &
region segmentation of objects in ND images." In Computer Vision, 2001. ICCV
2001. Proceedings. Eighth IEEE International Conference on, vol. 1, pp. 105-112.
IEEE, 2001.

L. Grady, "Random Walks for Image Segmentation," in IEEE Transactions on
Pattern Analysis and Machine Intelligence, vol. 28, no. 11, pp. 1768-1783, Nov.
2006, doi: 10.1109/TPAMI.2006.233.

```

## Acknowledgments
This code borrows from [NVIDIA/pix2pixHD](https://github.com/NVIDIA/pix2pixHD) and completely builds off of CkLibra (https://github.com/ckLibra/Self-Supervised-Depth-Estimation-for-Colonoscopy/blob/main/run_engine.py).
