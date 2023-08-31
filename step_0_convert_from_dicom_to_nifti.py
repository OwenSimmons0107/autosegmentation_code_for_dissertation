"""
Created on Thu Jun  9 17:54:49 2022

@author: mbcxahc3


Not sure exactly what this does and the paths will need changing but its a start
"""

import os
from DicomRTTool import DicomReaderWriter   # using this magic package to convert from dicom to nifti: https://pypi.org/project/DicomRTTool/
import SimpleITK as sitk


patient_fnames = [
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

for patient in patient_fnames:

    patient_dir = f"/Users/owensimmons/Desktop/repo for autosegmentation/PaediatricRMS_Angie_withcontours/{patient}"
    output_ct_dir = "/Users/owensimmons/Desktop/repo for autosegmentation/nifti images/output_ct_dir"
    output_mask_dir = "/Users/owensimmons/Desktop/repo for autosegmentation/output_mask_dir"

    os.makedirs(output_ct_dir, exist_ok=True)
    os.makedirs(output_mask_dir, exist_ok=True)
    
    reader = DicomReaderWriter()
    reader.walk_through_folders(patient_dir)
    reader.get_images()
    
    sitk.WriteImage(reader.dicom_handle, os.path.join(output_ct_dir, f"{patient}.nii"))
    
    names = reader.return_rois(print_rois=False)
    
    print(names)
    for name in names:
            print("Now converting contour " + name + " to nii format")
            reader.set_contour_names_and_associations([name])
            reader.get_mask()
            sitk.WriteImage(reader.annotation_handle, os.path.join(output_mask_dir, f"{patient}_{name}.nii"))
            print("Completed converting contour " + name)
            
    