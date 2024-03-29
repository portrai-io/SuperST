import pandas as pd
import matplotlib.pyplot as plt
import json
from skimage import draw
import numpy as np
from scipy.stats import norm
import cv2


def get_img_coord(tissue_dir, metafile, barcode_tag = '_1', hires=1):
    tissue_pos_file = tissue_dir+ 'spatial/tissue_positions_list.csv'
    imcoord = pd.read_csv( tissue_pos_file,
                           header=None, names= ['barcodes','tissue','row','col','imgrow','imgcol'])
    if hires:
        imgfile = tissue_dir + 'spatial/tissue_hires_image.png'
    else:
        imgfile = tissue_dir + 'spatial/tissue_lowres_image.png'

    tsimg = cv2.imread(imgfile)
    
    scale_file = tissue_dir+ 'spatial/scalefactors_json.json'

    with open(scale_file, "r") as st_json:
        scalefactor = json.load(st_json)
    print(scalefactor)

    imcoord_tissue = imcoord.loc[imcoord.tissue==1,:]
    if hires:
        imscale = scalefactor['tissue_hires_scalef']
    else:
        imscale = scalefactor['tissue_lowres_scalef']
    #For barcode tag from multiple data (e.g. Seurat)--> _1 
    imcoord_tissue.barcodes = [bname + barcode_tag for bname in imcoord_tissue.barcodes]
    
    if metafile:
        ts_meta = pd.read_csv(metafile)
        #Merged Items
        ts_meta_coord = pd.merge(ts_meta, imcoord_tissue, 
                                 how = 'inner', right_on ='barcodes' , left_on='Unnamed: 0')
    else:
        ts_meta_coord = imcoord_tissue
    
    return ts_meta_coord, tsimg, imscale

def spatial_masked_image(t_features, img, pd_coord_tissue, imscale):
    tsimg = np.zeros(img.shape[:2])    
    mask = np.zeros(img.shape[:2])    
    tsimg_row = np.array(round(pd_coord_tissue.loc[:,'imgrow']*imscale), dtype=int)
    tsimg_col = np.array(round(pd_coord_tissue.loc[:,'imgcol']*imscale), dtype=int)
    tsimg[tsimg_row,tsimg_col] = np.squeeze(t_features)
    mask[tsimg_row,tsimg_col] = 1
    return tsimg, mask

def get_spotdist(pd_coord_tissue, imscale):
    spotdist = (np.max(pd_coord_tissue.imgcol)-np.min(pd_coord_tissue.imgcol))/(np.max(pd_coord_tissue.col) - np.min (pd_coord_tissue.col))*imscale
    return spotdist*2

def spatial_featuremap(t_features, img, pd_coord_tissue, imscale, radius = 10, posonly=True):
    tsimg = np.zeros(img.shape[:2])    
    tsimg_row = np.array(round(pd_coord_tissue.loc[:,'imgrow']*imscale), dtype=int)
    tsimg_col = np.array(round(pd_coord_tissue.loc[:,'imgcol']*imscale), dtype=int)
    for rr, cc,t in zip(tsimg_row, tsimg_col,t_features):
        r, c = draw.circle(rr, cc, radius = radius)
        if posonly:
            if t>0:
                tsimg[r,c]= t
        else:
            tsimg[r,c]=t
    return tsimg