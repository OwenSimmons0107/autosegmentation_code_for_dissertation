#!/usr/bin/env python3
# -*- coding: ut

import nibabel as nib
import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np

patient =    'PT_1 UIDQQ0X1x1Hx7'

# Read the CT volume
ct_volume = sitk.ReadImage(f"/Users/owensimmons/Desktop/repo for autosegmentation/nifti images/output_ct_dir/{patient}.nii")
orig_spacing = ct_volume.GetSpacing()
orig_origin = ct_volume.GetOrigin()
ct_slices = sitk.GetArrayFromImage(ct_volume)

# Read the segmentation mask
segmentation_volume = sitk.ReadImage(f"/Users/owensimmons/Desktop/repo for autosegmentation/nifti images/combined_mask_dir/{patient}.nii")
segmentation_slices = sitk.GetArrayFromImage(segmentation_volume)

x_start, x_end = 143, 351  # Start and end indices in the x-axis (rows)
y_start, y_end = 143, 343  # Start and end indices in the y-axis (columns)
z_start, z_end = 80, 240   # Start and end indices in the z-axis (slices)



# Crop the image using numpy array slicing
cropped_ct = ct_slices[z_start:z_end, y_start:y_end, x_start:x_end]
cropped_segmentation  = segmentation_slices[z_start:z_end, y_start:y_end, x_start:x_end]

print(np.shape(cropped_ct))

# Create a masked array
mask = np.ma.masked_where(cropped_segmentation == 0, cropped_segmentation)

# Plot the CT slices with overlay
for i in range(cropped_ct.shape[0]):
    plt.imshow(cropped_ct[i, :, :], cmap='gray', interpolation='none')
    plt.imshow(mask[i, :, :], cmap="tab20", interpolation='none', alpha=0.5)
    plt.title(f"slice number {i +1}")
    plt.axis('off')
    plt.show()
    
    
cropped_ct_image =sitk.GetImageFromArray(cropped_ct)
cropped_ct_image.SetSpacing(orig_spacing)
cropped_ct_image.SetOrigin(orig_origin)
sitk.WriteImage(cropped_ct_image, f"/Users/owensimmons/Desktop/repo for autosegmentation/cropped_ct/{patient}.nii") 

cropped_seg_image =sitk.GetImageFromArray(cropped_segmentation)
cropped_seg_image.SetSpacing(orig_spacing)
cropped_seg_image.SetOrigin(orig_origin)
sitk.WriteImage(cropped_seg_image, f"/Users/owensimmons/Desktop/repo for autosegmentation/cropped_mask/{patient}.nii") 

