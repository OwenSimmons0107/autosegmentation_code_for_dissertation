# autosegmentaion_code
Code used for my dissertation project

# Preliminary instructions
1. Clone this repository
2. create a new python virtual environment: _python -m venv autosegmentation_env_
3. activate the virtual environment: _source autosegmentation_env/bin/activate_
4. install requirements: _pip install -r requirements.txt_

# Main instructions
0. Convert Dicom to Nifti using step_0_convert_from_dicom_to_nifti.py
1. Combine structures into a single mask with Combining_structures.py
2. Crop the images with crop_crop.py
3. Use resampling.py to reduce size further and make images a consistent spacing
4. use preprocess.py to preprocess the data
5. train using train.py
6. test using test.py

   
