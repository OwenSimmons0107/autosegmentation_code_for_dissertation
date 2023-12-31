import SimpleITK as sitk
import numpy as np
import os
from os.path import join

from utils import getFiles


#this script preprocesses CT images and combined masks to be used to train the model

image_dir = ""
mask_dir = ""
output_dir = ""

pat_fnames = sorted(getFiles(image_dir))

for fname in pat_fnames:
    # load
    image = sitk.ReadImage(join(image_dir, fname))
    mask = sitk.ReadImage(join(mask_dir, fname))
    
    # check head-first vs. feet-first orientation
    if(np.sign(image.GetDirection()[-1]) == -1):
        image = sitk.Flip(image, [False, False, True])
        mask = sitk.Flip(mask, [False, False, True])
    
    # convert to numpy
    image = sitk.GetArrayFromImage(image).astype(float)
    mask = sitk.GetArrayFromImage(mask).astype(int)
    
    # put into worldmatch Hounsfield Units -> !!!! for CT !!!! (not sure what you're using)
    if image.min() < -1:
        image += 1024
    
    # save
    os.makedirs(join(output_dir, "CTs"), exist_ok=True)
    os.makedirs(join(output_dir, "Structures"), exist_ok=True)
    np.save(join(output_dir, "CTs", fname), image)
    np.save(join(output_dir, "Structures", fname), mask)
