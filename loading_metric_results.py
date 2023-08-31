import numpy as np


# Load the results numpy array from the file
results1 = np.load('output_dir2/fold1/fold1/results/fold1_results_vec.npy')
results2 = np.load('output_dir2/fold5/fold5/results/fold5_results_vec.npy')

# Now you can analyze the results array
# The array has dimensions: (num_samples, nClass-1, 3)

# For example, let's print the individual Hausdorff95 and MeanDTA values for each organ:
nClass_minus_1 = results1.shape[1]
organs = ["dentition", "ethmoid", "mandible_l", "mandible_r", "maxilla_l", "maxilla_r",
          "nasal_bone", "orbit_l", "orbit_r", "sphenoid_l", "sphenoid_r", "tmj_l", "tmj_r"]

for organ_idx, organ_name in enumerate(organs):
    print(f"Structure: {organ_name}")
    print("Results for both datasets:")
    for sample_idx in range(1):
        hausdorff95_1 = results1[sample_idx, organ_idx, 0]
        mean_dta_1 = results1[sample_idx, organ_idx, 1]
        dice_coefficient_1 = results1[sample_idx, organ_idx, 2]

        hausdorff95_2 = results2[sample_idx, organ_idx, 0]
        mean_dta_2 = results2[sample_idx, organ_idx, 1]
        dice_coefficient_2 = results2[sample_idx, organ_idx, 2]

        print(f"Sample {sample_idx + 1}:")
        print(f"Dataset 1 - Hausdorff95: {hausdorff95_1:.3f} mm, MeanDTA: {mean_dta_1:.3f} mm, Dice: {dice_coefficient_1:.3f}")
        print(f"Dataset 2 - Hausdorff95: {hausdorff95_2:.3f} mm, MeanDTA: {mean_dta_2:.3f} mm, Dice: {dice_coefficient_2:.3f}")
        print("---")


