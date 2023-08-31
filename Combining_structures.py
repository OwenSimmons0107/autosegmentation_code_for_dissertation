#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 09:55:26 2023

@author: owensimmons
"""

import SimpleITK as sitk
import numpy as np


patients = [
#   'PT_3 (110850487)',
#    'PT_4 (331844332)',
#    'PT_9 (555118529)'
#    '740810725'
#    'PT_10 (596032881)'
#    'PT_5 UIDQQ0X7axq0q1'
#    'PT_2 UIDQQ0X70Q87a7'
#    'PT_7 UIDQQ0X70X7AQ1'
#    'PT_6 UIDQQ0X80hzruh'
#    'PT_8 UIDQQ0X70Xhzr8'
    'PT_1 UIDQQ0X1x1Hx7'
]

rois = ['dentition', 'ethmoid', 'mandible_l', 'mandible_r', 'maxilla_l', 'maxilla_r', 'nasal_bone', 'orbit_l', 'orbit_r', 'sphenoid_l', 'sphenoid_r', 'tmj_l', 'tmj_r']

directory_path = "/Users/owensimmons/Desktop/repo for autosegmentation/output_mask_dir"
output_path = "/Users/owensimmons/Desktop/repo for autosegmentation/nifti images/combined_mask_dir"



for patient in patients:
    ct_volume = sitk.ReadImage(f"/Users/owensimmons/Desktop/repo for autosegmentation/nifti images/output_ct_dir/{patient}.nii")
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


    unique_values = np.unique(segmentation_array)

    # The number of segmentations is the length of the unique_values array
    num_segmentations = len(unique_values) - 1

    print("Number of segmentations:", num_segmentations)

    combined_image =sitk.GetImageFromArray(segmentation_array)
    combined_image.SetSpacing(orig_spacing)
    combined_image.SetOrigin(orig_origin)
    sitk.WriteImage(combined_image, f"{output_path}/{patient}.nii") 
    