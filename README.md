# A. Overview

SuperST is a novel algorithm that employs a deep image prior (_i.e._, Unet) to create dense matrices from low-resolution Visium Spatial Transcriptomics (ST) libraries. The details of how SuperST is run are explained in this repository and are also discussed in our paper. Briefly, SuperST is composed of five units, that said A, B, C, D, and E, which indicate an input H&E image, conceptual down-sampling unit, _‘concatenate’_, conceptual up-sampling unit, and the output of U-Net, respectively.

<br>
<center>
<img src="https://github.com/portrai-io/SuperST/assets/55747737/1306cb22-60ee-47ff-aa53-91791c6e6eca" alt="drawing" />
</center>
<br>
<br>

Looking forward, SuperST holds the potential to be utilized across various research domains that employ ST in imaging analysis workflows. Also, SuperST-produced image data could be effortlessly integrated with other spatial omics technologies. Overall, SuperST marks a significant stride forward in the realm of Spatial Transcriptomics, paving the way for a deeper understanding of intricate biological systems.

<br>

_**Publication**_

* Park, J. et al. (2023). _Generation of Super-resolution Images from Barcode-based Spatial Transcriptomics Using Deep Image Prior_. Cell Reports Methods. [[Link]](https://pmc.ncbi.nlm.nih.gov/articles/pmid/39729996/) 

_**Patent**_

* Patent and Trademark Office, Republic of Korea. Application Number: 10-2023-0060674. Application Date: 2023.05.10. Super resolution Spatial transcriptome image generating method, Apparatus performing the same, and Program recorded in computer readable media for performing the same. 

_**Poster**_

* Park, J., Cook, S., Lee, D., Choi, J., Yoo, S., Im, H.-J., Lee, D., & Choi, H. (2023). Cancer region definition using spatial gene expression patterns by super-resolution reconstruction algorithm for spatial transcriptomics data. Paper presented at the AACR Annual Meeting 2024, San Diego Convention Center, California, USA.

<br>

---

# B. Environments

Download the `superst.yml` file and run the following command in an Anaconda Prompt:

```python
conda env create -f superst.yml
conda activate SuperST
```

<br>

---

# C. Data

When specifying `tissue_dir`, ensure the directory includes five crucial files typically produced by the 10X Visium platform:

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

```python
git clone https://github.com/portrai-io/SuperST.git
```

<br>

_**step 3.**_ Make a jupyter notebook file at the same directory as `app.py`.
  
<br>

_**step 4.**_ Open your jupyter notebook or jupyter lab. 

<br>

_**step 5.**_ Import all the functions from app.py into a Jupyter notebook file, and use the functions with the following manner.

<br>

```python
from app import *
tissue_dir = './Data/10X/V1_Adult_Mouse_Brain_Coronal_Section_2/'
Tgenes = ['Rbfox3', 'Lamp5']
demask_image_t, demask_image_t_g, tsimg1_, conv_spatial_images_ = \\
    merge(tissue_dir, Tgenes, num_iter = 32, is_cut_bg = True)
```

<br>

> Here, `demask_image_t` indicates SuperST images assuming zero-diffusion, while `demask_image_t_g` means SuperST images with a modifiable Gaussian kernel size specified by `kernel_gauss`.

<br>

---

# E. How to Use 2

_**step 1.**_ Open a Linux terminal.

<br>

_**step 2.**_ Git clone SuperST at the Linux terminal.

<br>

```python
git clone https://github.com/portrai-io/SuperST.git
```

<br>

_**step 3.**_ Type a command like below.

<br>

```python
python app.py \\
--tissue_dir ./Data/10X/V1_Adult_Mouse_Brain_Coronal_Section_2/ \\
--Tgenes Rbfox3 Lamp5 \\
--num_iter 32 \\
--is_cut_bg True
```

<br>

_**step 4.**_ The outfile, `SuperST.hdf5`, at the same directory as `app.py` can be open with the following in a jupyter notebook file.

<br>

```import h5py 
f = h5py.File("SuperST.hdf5", 'r')
dset1 = f['demask_image_t'] 
dset2 = f['demask_image_t_g'] 
dset3 = f['tsimg1_'] 
dset4 = f['conv_spatial_images_']
```

<br>

> Here, `demask_image_t` indicates SuperST images assuming zero-diffusion, while `demask_image_t_g` means SuperST images with a modifiable Gaussian kernel size specified by `kernel_gauss`.

<br>

---

# F. Example

Refer to the jupyter notebook file at the Example directory, where the usage methods are briefly introduced. The example dataset originates from the 10x Genomics Dataset ([ref](https://www.10xgenomics.com/resources/datasets/adult-mouse-brain-section-2-coronal-stains-dapi-anti-gfap-anti-neu-n-1-standard-1-1-0)).

<br>

---

# G. Contact

We, as Portrai. Inc., innovate the process of developing new drugs beyond the limits of human cognition, and deliver safer and more effective new drugs to humanity. For any questions or inquiries, please contact us at [contact@portrai.io](mailto:contact@portrai.io).
