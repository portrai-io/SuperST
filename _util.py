import numpy as np    
import math
from scipy import ndimage


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def cut_bg(tmpouts, tsimg, mask_bg = 0.95, dilatation=3):
    tsimg_gray = rgb2gray(tsimg)
    mask = tsimg_gray<np.percentile(tsimg_gray,95)*mask_bg #Mask Condition
    if dilatation>0:
        mask = ndimage.binary_dilation(mask, iterations = dilatation)
    num = len(tmpouts)
    tmpouts_ = []
    print('number of features:', num)
    for i, tt in enumerate(tmpouts):
        if i%100==0:
            print('...%d/%d'%(i+1,num))
        tmpout_ = tt * mask
        tmpouts_.append(tmpout_)
    return tmpouts_

def shape_matching(im, size):
    sz=im.shape
    if len(sz)==2:
        if sz[0] >size[0]:
            xstart=int(math.ceil(sz[0]/2)- int(size[0]/2-1))
            im=im[xstart-1:xstart+size[0]-1,:]
        else:
            npad1=int(math.floor(float(size[0])/2-float(sz[0])/2))
            npad2=int(math.ceil(float(size[0])/2-float(sz[0])/2))
            im=np.lib.pad(im,((npad1,npad2),
                              (0,0)),'edge')
        if sz[1] >size[1]:
            ystart=int(math.ceil(sz[1]/2)- int(size[1]/2-1))
            im=im[:,ystart-1:ystart+size[1]-1]
        else:
            npad1=int(math.floor(float(size[1])/2-float(sz[1])/2))
            npad2=int(math.ceil(float(size[1])/2-float(sz[1])/2))
            im=np.lib.pad(im,((0,0), (npad1,npad2)),'edge')
    if len(sz)==3: # RGB channels? 
        if sz[0] >size[0]:
            xstart=int(math.ceil(sz[0]/2)- int(size[0]/2-1))
            im=im[xstart-1:xstart+size[0]-1,:,:]
        else:
            npad1=int(math.floor(float(size[0])/2-float(sz[0])/2))
            npad2=int(math.ceil(float(size[0])/2-float(sz[0])/2))
            im=np.lib.pad(im,((npad1,npad2),
                              (0,0),(0,0)),'edge')
        if sz[1] >size[1]:
            ystart=int(math.ceil(sz[1]/2)- int(size[1]/2-1))
            im=im[:,ystart-1:ystart+size[1]-1,:]
        else:
            npad1=int(math.floor(float(size[1])/2-float(sz[1])/2))
            npad2=int(math.ceil(float(size[1])/2-float(sz[1])/2))
            im=np.lib.pad(im,((0,0), (npad1,npad2),(0,0)),'edge')
    return im