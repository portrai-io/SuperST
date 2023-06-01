# A. Overview

SuperST is a novel algorithm that employs a deep image prior (_i.e._, Unet) to create dense matrices from low-resolution Spatial Transcriptomics (ST) libraries. The details of how SuperST is run are explained in this repository and are also discussed in our paper. Briefly, SuperST is composed of five units, that said A, B, C, D, and E, which indicate an input H&E image, conceptual down-sampling unit, _‘concatenate’_, conceptual up-sampling unit, and _‘conv2d_25’_, respectively. 

<br>
<center>
<img src="https://github.com/portrai-io/SuperST/assets/55747737/0a664ff6-3cb8-45d8-b98f-1aecc10d00b9" alt="drawing" />
</center>
<br>
<br>

Looking forward, SuperST holds the potential to be utilized across various research domains that employ ST in imaging analysis workflows. Also, SuperST-produced image data could be effortlessly integrated with other spatial omics technologies. Overall, SuperST marks a significant stride forward in the realm of Spatial Transcriptomics, paving the way for a deeper understanding of intricate biological systems.

<br>

---

<br>

# B. Environments

<br>

---

<br>

# C. How to Use 1

<br>

_**step 1.**_ Open your jupyter notebook or jupyter lab. 

<br>

_**step 2.**_ Git clone SuperST at a Linux terminal.

<br>

<code> git clone https://github.com/portrai-io/SuperST.git </code>
  
<br>

_**step 3.**_ Make a jupyter notebook file at the same directory as app.py.

<br>

_**step 4.**_ Import all the functions from app.py into a Jupyter notebook file.

<br>

<code> from app import * </code>

<br>

---

<br>

# D. How to Use 2

<br>

_**step 1.**_ Open a Linux terminal.

<br>

_**step 2.**_ Type a command like below.

<br>

<code> python app.py --tissue_dir ./Data/10X/V1_Adult_Mouse_Brain_Coronal_Section_2/ --Tgenes Rbfox3 Lamp5 --num_iter 32 --is_cut_bg True </code>

<br>

_**step 3.**_ The outfile, SuperST.hdf5, at the same directory as app.py can be open with the following in a jupyter notebook file.

<br>

<code> f = h5py.File("SuperST.hdf5", 'r') </code>

<br>

---

<br>

# E. Example

<br>

Refer to the jupyter notebook file at the Example folder, where two usage methods are briefly introduced.

The example dataset originates from the 10x Genomics Dataset ([ref](https://www.10xgenomics.com/resources/datasets/adult-mouse-brain-section-2-coronal-stains-dapi-anti-gfap-anti-neu-n-1-standard-1-1-0)).

<br>

---

<br>

# F. Who we are
We, as Portrai. Inc., innovate the process of developing new drugs beyond the limits of human cognition, and deliver safer and more effective new drugs to humanity.
