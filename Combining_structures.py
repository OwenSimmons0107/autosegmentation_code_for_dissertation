#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 09:55:26 2023

@author: owensimmons
"""

import SimpleITK as sitk
import numpy as np

#this code combines the separate masks into one single array

#populate list with patient names
patients = []

rois = ['dentition', 'ethmoid', 'mandible_l', 'mandible_r', 'maxilla_l', 'maxilla_r', 'nasal_bone', 'orbit_l', 'orbit_r', 'sphenoid_l', 'sphenoid_r', 'tmj_l', 'tmj_r']

directory_path = "path_to_mask_directory"
output_path = "path_to_output_directory"

for patient in patients:
    ct_volume = sitk.ReadImage(f"path_to_CT_images/{patient}")
    orig_spacing = ct_volume.GetSpacing()
    orig_origin = ct_volume.GetOrigin()
    ct_slices = sitk.GetArrayFromImage(ct_volume)

    segmentation_array = np.zeros_like(ct_slices)

    for idx, item in enumerate(rois):
        file = f"{directory_path}/{patient}_{item}.nii"
        segmentation_img = sitk.ReadImage(file)
        segmentation_slices = sitk.GetArrayFromImage(segmentation_img)

        # Ignore overlapping segmentations
        segmentation_slices = np.where(segmentation_array == 0, segmentation_slices, 0)

        # Add the current segmentation to the combined array
        segmentation_array += (idx + 1) * segmentation_slices

    combined_image =sitk.GetImageFromArray(segmentation_array)
    combined_image.SetSpacing(orig_spacing)
    combined_image.SetOrigin(orig_origin)
    sitk.WriteImage(combined_image, f"{output_path}/{patient}.nii") 
    
