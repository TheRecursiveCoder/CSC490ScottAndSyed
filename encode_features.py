from options.train_options import TrainOptions
from data.data_loader import CreateDataLoader
from models.models import create_model
import numpy as np
import os

#Segmentations - Help from: https://scikit-image.org/skimage-tutorials/lectures/4_segmentation.html
import skimage.data as data
import skimage.segmentation as seg
from skimage import filters
from skimage import draw
from skimage import color
from skimage import exposure

def image_show(image, nrows=1, ncols=1, cmap='gray', **kwargs):
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(16, 16))
    ax.imshow(image, cmap='gray')
    ax.axis('off')
    return fig, ax


opt = TrainOptions().parse()
opt.nThreads = 1
opt.batchSize = 1 
opt.serial_batches = True 
opt.no_flip = True
opt.instance_feat = True
opt.continue_train = True

name = 'features'
save_path = os.path.join(opt.checkpoints_dir, opt.name)

############ Initialize #########
data_loader = CreateDataLoader(opt)
dataset = data_loader.load_data()
dataset_size = len(data_loader)
model = create_model(opt)

########### Encode features ###########
reencode = True
if reencode:
	features = {}
	for label in range(opt.label_nc):
		features[label] = np.zeros((0, opt.feat_num+1))
		
	for i, data in enumerate(dataset):    
	    feat = model.module.encode_features(data['image'], data['inst'])
	    for label in range(opt.label_nc):
	    	features[label] = np.append(features[label], feat[label], axis=0) 
			print(features[label], label)
			segmented = seg.random_walker(features[label], label)
			fig, ax = image_show(features[label])
			ax.imshow(segmented == 1, alpha=0.3);

	    print('%d / %d images' % (i+1, dataset_size))    
	save_name = os.path.join(save_path, name + '.npy')
	np.save(save_name, features)

############## Clustering ###########
n_clusters = opt.n_clusters
load_name = os.path.join(save_path, name + '.npy')
features = np.load(load_name).item()
from sklearn.cluster import KMeans
centers = {}
for label in range(opt.label_nc):
	feat = features[label]
	feat = feat[feat[:,-1] > 0.5, :-1]		
	if feat.shape[0]:
		n_clusters = min(feat.shape[0], opt.n_clusters)
		kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(feat)
		centers[label] = kmeans.cluster_centers_
save_name = os.path.join(save_path, name + '_clustered_%03d.npy' % opt.n_clusters)
np.save(save_name, centers)
print('saving to %s' % save_name)