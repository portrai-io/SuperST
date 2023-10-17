import matplotlib.pyplot as plt
import scanpy as sc
import numpy as np
import pandas as pd
import cv2
import math
from scipy.spatial import distance
from scipy.ndimage import gaussian_filter
import os, h5py
import argparse

from _imagizer_mask import spatial_masked_image, get_spotdist, get_img_coord, spatial_featuremap
from _util import cut_bg, shape_matching, rgb2gray
from _demask import demask_multiple


# Purpose: high resolution for gene expresison 
## kernel_gauss = 5
def spatial_dip(tissue_dir, Tgenes, metafile=None, target_s= 256, mask_bg = 0.95, cut_bg_dilatation=3,
               num_iter = 300, kernel_size=10, sigma=5,verbose=0):
    adata1 = sc.read_visium(tissue_dir) 
    adata1.var_names_make_unique()
    sc.pp.normalize_total(adata1, inplace=True)
    sc.pp.log1p(adata1)
    
    ts_meta_coord1,tsimg1, imscale1 = get_img_coord(tissue_dir, metafile, barcode_tag = '', hires=0)
    spotdist1 = get_spotdist(ts_meta_coord1,imscale1)
    
    #To Target image size
    target_s = float(target_s)
    target_scale = target_s/np.max(tsimg1.shape)
    orig_dim = tsimg1.shape[:2]
    target_dim = (round(orig_dim[0]*target_scale), round(orig_dim[1]*target_scale))
    tsimg1_ = cv2.resize(tsimg1, target_dim)
    imscale1_ = imscale1*target_scale
    spotdist1 = spotdist1*target_scale
    
    ts_meta_coord1_ = pd.merge(adata1.obs,ts_meta_coord1,how = 'inner', right_on ='barcodes' , left_on=adata1.obs.index  )
    
    #Spatial Images
    spatial_images = []
    for Tgene in Tgenes:
        spatial_image,mask_image = spatial_masked_image(np.asarray(adata1[:,Tgene].X.todense()), #FEATURE
                                             tsimg1_,
                                             ts_meta_coord1_,
                                             imscale1_)
        spatial_images.append(spatial_image)
    
    #Mask Generation
    if mask_bg:
        tsimg_gray = rgb2gray(tsimg1_)
        mask_ts = tsimg_gray>np.percentile(tsimg_gray,95)*mask_bg #Mask Condition
        mask_image= np.asarray(mask_image+mask_ts >0, dtype=np.float)
        
    #To Square form
    ttsize = (target_s,target_s,3)
    tsimg1_ = shape_matching(tsimg1_, ttsize)
    spatial_images_=[]
    for spatial_image in spatial_images:
        spatial_image_ = shape_matching(spatial_image, ttsize[:2])
        spatial_images_.append(spatial_image_)
    mask_image_ = shape_matching(mask_image, ttsize[:2])
    spatial_images_ = np.asarray(spatial_images_)
    spatial_images_ = np.transpose(spatial_images_,(1,2,0))
    
    #Conventional Images    
    conv_spatial_images = [] 
    for Tgene in Tgenes:
        conv_spatial_images.append(spatial_featuremap(np.asarray(adata1[:,Tgene].X.todense()),
                                                      tsimg1_, ts_meta_coord1_, imscale1_, radius =2, posonly=True))
    conv_spatial_images_=[]
    for im in conv_spatial_images:
        conv_spatial_images_.append(shape_matching(im, ttsize[:2]))
    conv_spatial_images_ = np.asarray(conv_spatial_images_)
    
    #Demasking using DIP
    demask_image, demask_image_g = demask_multiple(spatial_images_,mask_image_, init_image=tsimg1_, 
                                                   num_iter = num_iter, kernel_size=kernel_size, sigma=sigma,verbose=verbose)
    
    
    demask_image_t = np.transpose(demask_image, (2,0,1))
    demask_image_t_g = np.transpose(demask_image_g, (2,0,1))
    demask_image_t = cut_bg(demask_image_t,tsimg1_,mask_bg = mask_bg, dilatation=cut_bg_dilatation)
    demask_image_t_g = cut_bg(demask_image_t_g,tsimg1_,mask_bg = mask_bg,dilatation=cut_bg_dilatation)
    
    return demask_image_t, demask_image_t_g, tsimg1_, conv_spatial_images_


# Purpose: high resolution for obs
## Update: 23.10.17
def spatial_dip2(adata1, tissue_dir, feature, metafile=None, target_s= 256, mask_bg = 0.95, cut_bg_dilatation=3,
               num_iter = 300, kernel_size=10, sigma=5,verbose=0):
                   
    ts_meta_coord1,tsimg1, imscale1 = get_img_coord(tissue_dir, metafile, barcode_tag = '', hires=0)
    ts_meta_coord1 = ts_meta_coord1[ts_meta_coord1['barcodes'].isin(adata1.obs.index)]
    spotdist1 = get_spotdist(ts_meta_coord1,imscale1)
    
    #To Target image size
    target_s = float(target_s)
    target_scale = target_s/np.max(tsimg1.shape)
    orig_dim = tsimg1.shape[:2]
    target_dim = (round(orig_dim[0]*target_scale), round(orig_dim[1]*target_scale))
    tsimg1_ = cv2.resize(tsimg1, target_dim)
    imscale1_ = imscale1*target_scale
    spotdist1 = spotdist1*target_scale
    
    ts_meta_coord1_ = pd.merge(adata1.obs,ts_meta_coord1,how = 'inner', right_on ='barcodes' , left_on=adata1.obs.index  )
                   
    #Spatial Images
    spatial_images = []
    spatial_image,mask_image = spatial_masked_image(np.asarray(adata1.obs[feature]), #FEATURE
                                         tsimg1_,
                                         ts_meta_coord1_,
                                         imscale1_)
    spatial_images.append(spatial_image)
                   
    #Mask Generation
    if mask_bg:
        tsimg_gray = rgb2gray(tsimg1_)
        mask_ts = tsimg_gray>np.percentile(tsimg_gray,95)*mask_bg #Mask Condition
        mask_image= np.asarray(mask_image+mask_ts >0, dtype=np.float)
        
    #To Square form
    ttsize = (target_s,target_s,3)
    tsimg1_ = shape_matching(tsimg1_, ttsize)
    spatial_images_=[]
    for spatial_image in spatial_images:
        spatial_image_ = shape_matching(spatial_image, ttsize[:2])
        spatial_images_.append(spatial_image_)
    mask_image_ = shape_matching(mask_image, ttsize[:2])
    spatial_images_ = np.asarray(spatial_images_)
    spatial_images_ = np.transpose(spatial_images_,(1,2,0))
    
    #Conventional Images    
    conv_spatial_images = [] 
    conv_spatial_images.append(spatial_featuremap(np.asarray(adata1.obs[feature]),
                                                  tsimg1_, ts_meta_coord1_, imscale1_, radius =2, posonly=True))
    conv_spatial_images_=[]
                   
    for im in conv_spatial_images:
        conv_spatial_images_.append(shape_matching(im, ttsize[:2]))
    conv_spatial_images_ = np.asarray(conv_spatial_images_)
                   
    #Demasking using DIP
    demask_image, demask_image_g = demask_multiple(spatial_images_,mask_image_, init_image=tsimg1_, 
                                                   num_iter = num_iter, kernel_size=kernel_size, sigma=sigma,verbose=verbose)
    
    demask_image_t = np.transpose(demask_image, (2,0,1))
    demask_image_t_g = np.transpose(demask_image_g, (2,0,1))
    demask_image_t = cut_bg(demask_image_t,tsimg1_,mask_bg = mask_bg, dilatation=cut_bg_dilatation)
    demask_image_t_g = cut_bg(demask_image_t_g,tsimg1_,mask_bg = mask_bg,dilatation=cut_bg_dilatation)

    # Check for NaN values and issue a warning if they exist
    if np.isnan(demask_image_t).any() or np.isnan(demask_image_t_g).any():
        warnings.warn("There might be an Na or NaN data in the adata.obs[feature]. Please check the data.")
                   
    return demask_image_t, demask_image_t_g, tsimg1_, conv_spatial_images_



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--spdir', '-s',type=str, required=True,
                        help='spatial trx location')
    parser.add_argument('--features','-f',type=str, required=True,
                        nargs='+')
    parser.add_argument('--metafile','-m',type=str, 
                        default=None)
    parser.add_argument('--targetsize',type=int,
                        default=256)
    parser.add_argument('--num_iter',type=int,
                        default=32)
    parser.add_argument('--verbose',type=int,
                        default=0)
    parser.add_argument('--maskbg',type=float,
                        default=0.95)
    parser.add_argument('--outdir',type=str,
                        default='./spatialdip_out/')
    args = parser.parse_args()

    tissue_dir = args.spdir
    Tgenes = args.features
    target_s = args.targetsize
    metafile = args.metafile
    num_iter = args.num_iter
    verbose =args.verbose
    mask_bg = args.maskbg
    demask_image_t, demask_image_t_g, tsimg1_, conv_spatial_images_= spatial_dip(tissue_dir, Tgenes, metafile=metafile, target_s= target_s, 
                                                                            mask_bg = mask_bg, cut_bg_dilatation=3,
                                                                            num_iter = num_iter, kernel_size=10, sigma=5,verbose=verbose)

    outdir = args.outdir
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    fname_ =  os.path.basename(os.path.normpath(tissue_dir))
    fname = outdir+fname_+'_spatialdip.h5'
    # Create a new file
    f = h5py.File(fname, 'w')
    f.create_dataset('dip', data=demask_image_t)
    f.create_dataset('dip_sm', data=demask_image_t_g)
    f.create_dataset('tsimg', data = tsimg1_)
    f.create_dataset('conv', data = conv_spatial_images_)
    #f.create_dataset('features', data = Tgenes)
    f.close()
    
    #draw fig
    plt.figure(figsize=(20,10))
    idxall = len(Tgenes)
    for ii in range(idxall):
        plt.subplot(1,idxall,ii+1)
        plt.imshow(tsimg1_)
        plt.imshow(demask_image_t[ii], cmap='jet', vmin=0, vmax=None, alpha=0.5) 
        plt.title(Tgenes[ii])
        plt.axis('off')
        plt.colorbar(shrink=0.5)
    plt.savefig(outdir+fname_+'_out.png')
    
    plt.figure(figsize=(20,10))
    idxall = len(Tgenes)
    for ii in range(idxall):
        plt.subplot(1,idxall,ii+1)
        plt.imshow(tsimg1_)
        plt.imshow(conv_spatial_images_[ii], cmap='jet', vmin=0, vmax=None, alpha=0.5)  
        plt.title(Tgenes[ii])
        plt.axis('off')
        plt.colorbar(shrink=0.5)
    plt.savefig(outdir+fname_+'_out_conventional.png')

