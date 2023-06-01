import numpy as np 
import pandas as pd
import cv2
import h5py
import matplotlib.pyplot as plt
import base64
import argparse
from io import BytesIO
from _Spatial_DIP import spatial_dip


def RGBtoGray(img):
    out = np.empty((img.shape[0], img.shape[1]))

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            out[i:i+1, j:j+1] = ( 0.2989*img[i:i+1, j:j+1, 0:1] + 
                                  0.5870*img[i:i+1, j:j+1, 1:2] + 
                                  0.1140*img[i:i+1, j:j+1, 2:3]
                                ).item()
      
    return out


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


def cut_bg(tmpouts, tsimg):
    tsimg_gray = rgb2gray(tsimg)
    mask = tsimg_gray<np.percentile(tsimg_gray,95)*0.95 #Mask Condition
    
    num = len(tmpouts)
    tmpouts_ = []
    print('number of features:', num)
    for i, tt in enumerate(tmpouts):
        if i%100==0:
            print('...%d/%d'%(i+1,num))
        tmpout_ = tt * mask
        tmpouts_.append(tmpout_)
    return tmpouts_


def merge(tissue_dir, Tgenes, metafile = None, target_s= 256, mask_bg = 0.95, n_cluster = 5, num_iter = 64, is_cut_bg = True):
    JB_demask_image_t, JB_demask_image_t_g, JB_tsimg1_, JB_conv_spatial_images_= spatial_dip(tissue_dir, Tgenes, metafile=metafile, target_s= target_s, mask_bg = mask_bg, cut_bg_dilatation=3,
                        num_iter = num_iter, kernel_size=10, sigma=5,verbose=0)  
    
    if is_cut_bg:
        JB_demask_image_t = cut_bg(JB_demask_image_t, JB_tsimg1_)
    
    return JB_demask_image_t, JB_demask_image_t_g, JB_tsimg1_, JB_conv_spatial_images_

def convert(s):
    new = ""
    for x in s:
        new += x 
    return new


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tissue_dir', type=str)
    parser.add_argument('--Tgenes', nargs="*", type=list)
    parser.add_argument('--num_iter', type=int, default=32)
    parser.add_argument('--is_cut_bg', type=bool, default=True)
    args = parser.parse_args()
    
    tissue_dir = args.tissue_dir
    Tgenes = args.Tgenes
    num_iter = args.num_iter
    is_cut_bg = args.is_cut_bg
    
    Tgenes_ = []
    for i in range(len(Tgenes)):
        Tgenes_.append(convert(Tgenes[i]))
                
    demask_image_t, demask_image_t_g, tsimg1_, conv_spatial_images_ = \
        merge(tissue_dir = tissue_dir, Tgenes = Tgenes_, num_iter = num_iter, is_cut_bg = is_cut_bg)
    
    f = h5py.File("SuperST.hdf5", "w")
    dset1 = f.create_dataset("demask_image_t", dtype='float', data=demask_image_t)
    dset2 = f.create_dataset("demask_image_t_g", dtype = 'float', data=demask_image_t_g)
    dset3 = f.create_dataset("tsimg1_", dtype = 'float', data=tsimg1_)
    dset4 = f.create_dataset("conv_spatial_images_", dtype = 'float', data=conv_spatial_images_)
    f.close