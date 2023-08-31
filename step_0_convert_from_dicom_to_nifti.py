"""
Created on Thu Jun  9 17:54:49 2022

"""

import os
from DicomRTTool import DicomReaderWriter   # using this magic package to convert from dicom to nifti: https://pypi.org/project/DicomRTTool/
import SimpleITK as sitk


#file names for different dicom images
patient_fnames = [
]

for patient in patient_fnames:

    patient_dir = f"directory_of_dicom_images/{patient}"
    output_ct_dir = "path_to_output_ct_dir"
    output_mask_dir = "path_to_output_mask_dir"

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
            
    
