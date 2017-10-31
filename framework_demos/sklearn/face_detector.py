import logging
logging.basicConfig(level=logging.INFO, format=u"%(asctime)s [%(levelname)s]:%(filename)s, %(name)s, in line %(lineno)s >> %(message)s".encode('utf-8'))
logger = logging.getLogger("face_dector.py")
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

import sys
import os
import sklearn

from sklearn.datasets import fetch_lfw_people
logger.info("sys.version_info")
logger.info("sklearn.__version__")

import math
import numpy as np

from skimage import exposure
import scipy.misc
import caffe
import scipy.io as io

# loading data

lfw_people = fetch_lfw_people(color=True)
lfw_people_color = lfw_people
target_names = lfw_people.target_names
X, y = lfw_people.data, lfw_people.target
# this does not work, deprecated
# lfw_fea_data = io.loadmat('LFW_Feature.mat')

# read targets

target_img = "0.jpg"
image = caffe.io.load_image(target_img)
target = image
plt.figure()
plt.imshow(target)

enhanced = exposure.equalize_hist(image[50:180, 60:170])
scipy.misc.imsave('enhanced0.jpg', enhanced)
plt.figure()
plt.imshow(enhanced)

CAFFE_ROOT = "../caffe/"

model_weights = os.path.join(CAFFE_ROOT, "lwf_caffe_face/face_model.caffemodel")
if os.path.isfile(model_weights):
    print("model %s is found!" % model_weights)
else:
    print("model file is not found!")
model_def = os.path.join(CAFFE_ROOT, "lwf_caffe_face/face_deploy.prototxt.txt")
if os.path.isfile(model_def):
    print("model_def %s is found!" % model_def)
else:
    print("model definition is not found!")

img = "0.jpg"
lfw_attr = "lfw_attributes.txt"

caffe.set_mode_gpu()
caffe.set_device(0)

net = caffe.Net(model_def,
                model_weights,
                caffe.TEST)

img=caffe.io.load_image(img)
target = img
test_img = caffe.io.load_image("Elizabeth_Smart_0004.jpg")

def detect(net, img):
    if img.ndim == 2:
        rows, cols = img.shape
    elif img.ndim == 3:
        rows, cols, ch = img.shape
    # compute scaling
    chunck_shape = (3,) +  net.blobs['data'].data.shape[1:]
    net.blobs['data'].reshape(*chunck_shape)
    net.reshape()
    # print("After reshaping ...")
    # print("net.blobs['data']", net.blobs['data'])
    # print("net.blobs['data'].data.shape", net.blobs['data'].data.shape)
    
    # print(net.blobs['data'].data.shape)
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    # transform mean
    
    # scale
    # transformer.set_raw_scale('data', 255)
    
    if img.ndim == 2:
        img = img[:,:,np.newaxis]
    # print("before transforming, image : ", img.shape)
    transformed_image = transformer.preprocess('data', img)
    # print("transformed image shape is : (%s,%s,%s)" % transformed_image.shape)
    net.blobs['data'].data[0] = transformed_image
    # Forward pass.
    out = net.forward()
    #
    return out

def cosine_(v1, v2):
    v2.dot(v1)
    n1 = np.sqrt(v1.dot(v1))
    n2 = np.sqrt(v2.dot(v2))
    return v1.dot(v2) / (n1 * n2)

def deepfeatureExtract(net, img):
    dim = [3, 112, 96]
    # coord5points = 
    # facial5points = 
    
    origin_img = img
    flip_img = np.flipud(img)
    
    out1 = detect(net, origin_img)['fc5']
    out2 = detect(net, flip_img)['fc5']
    
    return np.hstack([out1, out2])

target_fea_task1 = deepfeatureExtract(net, enhanced)

ret = []
fea_vector = []

n = len(lfw_people_color.images)
for i in range(n):
    logger.info("%sth image fea computing ..." % i)
    img = lfw_people_color.images[i]
    # temp_fea = lfw_fea_data['feature'][:,i]
    temp_fea = deepfeatureExtract(net, img)
    fea_vector.append(temp_fea)

    dis = cosine_(target_fea_task1[0, :], temp_fea[0, :])
    if dis > 0.20:
        logger.info("%s th image ..." % i)
        logger.info("\tfound face id %s with cos similarity %s" % (y[i], dis))
        ret.append((i, dis))

fea_vector = np.array(fea_vector)
fea_vector.dump("fea_vector")

print(len(ret))
ret.sort(key=lambda row: row[1],reverse=True)
print(ret[0:10])
plt.figure()
plt.imshow(test_img)

plt.figure()
plt.imshow(lfw_people_color.images[ret[0][0]] * 255)
print(target_names[y[ret[0][0]]])

logger.info("{} candidate images found, they are: {}".format(len(ret), ",".join(map(lambda item: "<{},{}>".format(*item), ret))))
