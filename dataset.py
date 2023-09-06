# pyright: reportUnboundVariable=false
import os
import numpy as np
import torch
import torch.utils.data as data
import random
from utils import windowLevelNormalize
from scipy.ndimage import zoom, rotate
import torchio as tio

#this code loads the images of the dataset into the model each epoch whilst applying augmentations to them

class SegDataset3D(data.Dataset):
    def __init__(self, available_ims, imagedir, maskdir, geometric_transforms=False, misc_transforms=False, one_hot_masks=True, test=False):
        self.available_im_fnames = available_ims
        self.imagedir = imagedir
        self.maskdir = maskdir
        self.one_hot_masks = one_hot_masks
        self.geometric_transforms = geometric_transforms
        self.misc_transforms = misc_transforms
        self.test = test
        if self.test:
            self.one_hot_masks = False

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
           idx = idx.tolist()
        imageToUse = np.load(os.path.join(self.imagedir, self.available_im_fnames[idx]))
        maskToUse = np.load(os.path.join(self.maskdir, self.available_im_fnames[idx]))
        image, target_mask = self.generatePair(imageToUse, maskToUse)
        sample = {'image': image, 'target_mask': target_mask, 'fname': self.available_im_fnames[idx]}
        return sample

    def __len__(self):
        return len(self.available_im_fnames)

    def generatePair(self, image, mask):
        image = image.astype(float)        # float conversion here
        image = image[np.newaxis, ...]
        mask = mask[np.newaxis, ...]
        # Convert numpy arrays to Torch tensors
        image_tensor = torch.tensor(image, dtype=torch.float32)
        mask_tensor = torch.tensor(mask, dtype=torch.float32)

        # Convert tensors to torchio Subjects
        subject = tio.Subject(
            image=tio.ScalarImage(tensor=image_tensor),
            segmentation=tio.LabelMap(tensor=mask_tensor),
        )

        #define augmentations
        geometric_transforms = {
            tio.RandomAffine(translation=0, degrees=5):0.35,
            tio.RandomAffine(translation=(10, 25, 25), degrees=0): 0.35,
            tio.RandomElasticDeformation(num_control_points=5, max_displacement=5): 0.25,
            tio.RandomFlip(): 0.05
        }
        misc_transforms = {
            tio.RandomNoise(std=(10, 50)): 0.5,
            tio.RandomBlur(std=(0.5, 1)): 0.5
        }

        transform = tio.Compose([
            tio.OneOf(geometric_transforms, p=0.75),
            tio.OneOf(misc_transforms, p = 0.4)
        ])
        # data augmentations
        if self.test:
            pass
        else:
            if self.geometric_transforms and self.misc_transforms:
                subject = transform(subject)
            
        augmented_image_tensor = subject['image'].data
        augmented_mask_tensor = subject['segmentation'].data

        # Convert tensors to numpy arrays
        image = augmented_image_tensor.squeeze().numpy()
        mask = augmented_mask_tensor.squeeze().numpy()
                
        # Post-augmentations, add channels axis and normalise
        # After augmentations, perform window and level contrast normalisation (add the channels axis here)
        image = windowLevelNormalize(image[..., np.newaxis], level=1512, window=3024) # -> !!!! for CT !!!! (not sure what you're using)
        
        # convert to one-hot mask if required (e.g. for DICE loss)
        if self.one_hot_masks:
            mask = (np.arange(mask.max()+1) == mask[...,None]).astype(int)
        
        # check input data for problems
        assert not np.any(np.isnan(image))
        return image, mask

   
