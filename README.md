# A. Overview

SuperST is a novel algorithm that employs a deep image prior (_i.e._, Unet) to create dense matrices from low-resolution Spatial Transcriptomics (ST) libraries. The details of how SuperST is run are explained in this repository and are also discussed in our paper. Briefly, SuperST is composed of five units, that said A, B, C, D, and E, which indicate an input H&E image, conceptual down-sampling unit, _‘concatenate’_, conceptual up-sampling unit, and and the output of U-Net, respectively.

<br>
<center>
<img src="https://github.com/portrai-io/SuperST/assets/55747737/1306cb22-60ee-47ff-aa53-91791c6e6eca" alt="drawing" />
</center>
<br>
<br>

Looking forward, SuperST holds the potential to be utilized across various research domains that employ ST in imaging analysis workflows. Also, SuperST-produced image data could be effortlessly integrated with other spatial omics technologies. Overall, SuperST marks a significant stride forward in the realm of Spatial Transcriptomics, paving the way for a deeper understanding of intricate biological systems.

<br>

_**Publication**_

1. Park, J.B. et al. (2023). _Generation of Super-resolution Images from Low-resolution Spatial Transcriptomics Library by Using Deep Image Prior_. bioRxiv. [[Link]](https://www.biorxiv.org/content/10.1101/2023.06.26.546529v1) 

<br>

---

# B. Environments

_**Python Version**_ 

<br>

| **Language** | **Version** |
| --- | --- |
| Python | 3.8.13 |

<br>

_**Python Packages**_

<br>

| **Package** | **Version**  |
| --- | --- |
| h5py | 3.8.0 |
| keras | 2.4.3 |
| matplotlib | 3.6.2 |
| numpy | 1.21.6 |
| opencv-python | 4.6.0.66 |
| pandas | 1.5.3 |
| protobuf | 3.19.1 |
| scanpy | 1.9.1 |
| scikit-image | 0.18.3 |
| scipy | 1.10.1 |
| tensorflow | 2.4.3 |

<br>

Note that Python=3.8, protobuf <= 3.20 and tensorflow=2 are required or preferred for SuperST. Also, it is recommended to install tensorflow and keras at first due to dependencies.

<br>

---

# C. Data

When specifying 'tissue_dir', ensure the directory includes five crucial files typically produced by the 10X Visium platform:

- `filtered_feature_bc_matrix.h5`
- `spatial/tissue_positions_list.csv`
- `spatial/scalefactors_json.json`
- `spatial/tissue_lowres_image.png`
- `spatial/tissue_hires_image.png`

<br>

---

# D. How to Use 1

_**step 1.**_ Open a Linux terminal.

<br>

_**step 2.**_ Git clone SuperST at the Linux terminal.

<br>

<code>git clone https://github.com/portrai-io/SuperST.git </code>

<br>

_**step 3.**_ Make a jupyter notebook file at the same directory as app.py.
  
<br>

_**step 4.**_ Open your jupyter notebook or jupyter lab. 

<br>

_**step 5.**_ Import all the functions from app.py into a Jupyter notebook file, and use the functions with the following manner.

<br>

<code>from app import *
&nbsp;tissue_dir = './Data/10X/V1_Adult_Mouse_Brain_Coronal_Section_2/'
&nbsp;Tgenes = ['Rbfox3', 'Lamp5']
&nbsp;demask_image_t, demask_image_t_g, tsimg1_, conv_spatial_images_=\\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;merge(tissue_dir, Tgenes, num_iter = 32, is_cut_bg = True)</code>

<br>

---

# E. How to Use 2

_**step 1.**_ Open a Linux terminal.

<br>

_**step 2.**_ Git clone SuperST at the Linux terminal.

<br>

<code>git clone https://github.com/portrai-io/SuperST.git </code>

<br>

_**step 3.**_ Type a command like below.

<br>

<code>python app.py \\
&nbsp;&nbsp; --tissue_dir ./Data/10X/V1_Adult_Mouse_Brain_Coronal_Section_2/ \\
&nbsp;&nbsp; --Tgenes Rbfox3 Lamp5 \\
&nbsp;&nbsp; --num_iter 32 \\
&nbsp;&nbsp; --is_cut_bg True </code>

<br>

_**step 4.**_ The outfile, SuperST.hdf5, at the same directory as app.py can be open with the following in a jupyter notebook file.

<br>

<code>import h5py 
&nbsp;f = h5py.File("SuperST.hdf5", 'r')
&nbsp;dset1 = f['demask_image_t'] 
&nbsp;dset2 = f['demask_image_t_g'] 
&nbsp;dset3 = f['tsimg1_'] 
&nbsp;dset4 = f['conv_spatial_images_']</code>

<br>

---

# F. Example

Refer to the jupyter notebook file at the Example directory, where the usage methods are briefly introduced. The example dataset originates from the 10x Genomics Dataset ([ref](https://www.10xgenomics.com/resources/datasets/adult-mouse-brain-section-2-coronal-stains-dapi-anti-gfap-anti-neu-n-1-standard-1-1-0)).

<br>

---

# G. Contact

We, as Portrai. Inc., innovate the process of developing new drugs beyond the limits of human cognition, and deliver safer and more effective new drugs to humanity. For any questions or inquiries, please contact us at [contact@portrai.io](mailto:contact@portrai.io).
