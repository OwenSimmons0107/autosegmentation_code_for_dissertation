import SimpleITK as sitk
import os
import numpy as np

input_dir = "nifti_images_cropped/ct_images"
output_dir = "nifti_images_resampled"


patients = [f for f in os.listdir(input_dir) if f.endswith(".nii")]

target_spacing = [1.50, 1.50, 3.0]  # Desired spacing

for patient in patients:
    # Read the CT volume
    ct_volume = sitk.ReadImage(os.path.join(input_dir, patient))
    print(ct_volume.GetSize())

    # Calculate target dimensions based on desired spacing
    target_dimensions = [int(np.ceil(ct_volume.GetSize()[i] * ct_volume.GetSpacing()[i] / spacing)) for i, spacing in enumerate(target_spacing)]
    #print(target_dimensions)
    
    # Calculate the remainder when dividing by 8
    r = [dim % 8 for dim in target_dimensions]

    # Adjust dimensions by either adding or subtracting remainder to get closer to the desired spacing
    target_dimensions = [
    dim + (8 - r[i]) if r[i] >= 4 else dim - r[i]
    for i, dim in enumerate(target_dimensions)
    ]

    # Calculate new spacing based on target dimensions
    new_spacing = [ct_volume.GetSpacing()[i] * ct_volume.GetSize()[i] / target_dimensions[i] for i in range(3)]

    # Resample the CT volume with the new spacing and dimensions
    resampled_ct = sitk.Resample(ct_volume, target_dimensions, sitk.Transform(), sitk.sitkLinear,
                                 ct_volume.GetOrigin(), new_spacing, ct_volume.GetDirection(),
                                 0.0, ct_volume.GetPixelIDValue())
    
    print(resampled_ct.GetSize())
    print(resampled_ct.GetSpacing())

    # Write the resampled CT volume to the output directory
    output_ct_path = os.path.join(output_dir, "ct_images", patient)
    sitk.WriteImage(resampled_ct, output_ct_path)

    # Similarly, resample the segmentation volume with the new spacing and dimensions
    segmentation_volume = sitk.ReadImage(os.path.join("nifti_images_cropped/mask_images", patient))
    resampled_segmentation = sitk.Resample(segmentation_volume, target_dimensions, sitk.Transform(),
                                           sitk.sitkNearestNeighbor, segmentation_volume.GetOrigin(),
                                           new_spacing, segmentation_volume.GetDirection(),
                                           segmentation_volume.GetPixelIDValue())

    # Write the resampled segmentation volume to the output directory
    output_segmentation_path = os.path.join(output_dir, "mask_images", patient)
    sitk.WriteImage(resampled_segmentation, output_segmentation_path)
