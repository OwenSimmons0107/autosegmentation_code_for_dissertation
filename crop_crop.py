#!/usr/bin/env python3
# -*- coding: ut

import nibabel as nib
import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np

patient =  'patient_file_name'

# Read the CT volume
ct_volume = sitk.ReadImage("path_to_ct_directory/{patient}")
orig_spacing = ct_volume.GetSpacing()
orig_origin = ct_volume.GetOrigin()
ct_slices = sitk.GetArrayFromImage(ct_volume)

# Read the segmentation mask
segmentation_volume = sitk.ReadImage(f"path_to_mask_directory/{patient}")
segmentation_slices = sitk.GetArrayFromImage(segmentation_volume)

#define the parts of the array we wish to crop to
x_start, x_end = 0, 512 # Start and end indices in the x-axis (rows)
y_start, y_end = 0, 512, # Start and end indices in the y-axis (columns)
z_start, z_end = 80, 240   # Start and end indices in the z-axis (slices)



# Crop the image using numpy array slicing
cropped_ct = ct_slices[z_start:z_end, y_start:y_end, x_start:x_end]
cropped_segmentation  = segmentation_slices[z_start:z_end, y_start:y_end, x_start:x_end]

# Create a masked version of the array
mask = np.ma.masked_where(cropped_segmentation == 0, cropped_segmentation)

# Plot the CT slices with overlay to check the crop is correct
for i in range(cropped_ct.shape[0]):
    plt.imshow(cropped_ct[i, :, :], cmap='gray', interpolation='none')
    plt.imshow(mask[i, :, :], cmap="tab20", interpolation='none', alpha=0.5)
    plt.title(f"slice number {i +1}")
    plt.axis('off')
    plt.show()
    
    
cropped_ct_image =sitk.GetImageFromArray(cropped_ct)
cropped_ct_image.SetSpacing(orig_spacing)
cropped_ct_image.SetOrigin(orig_origin)
sitk.WriteImage(cropped_ct_image, "path_to_output_CT_directory/{patient}") 

cropped_seg_image =sitk.GetImageFromArray(cropped_segmentation)
cropped_seg_image.SetSpacing(orig_spacing)
cropped_seg_image.SetOrigin(orig_origin)
sitk.WriteImage(cropped_seg_image, "path_to_output_mask_directory/{patient}") 

