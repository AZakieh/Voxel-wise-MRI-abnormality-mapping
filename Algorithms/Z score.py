from tkinter import Tk
from tkinter.filedialog import askopenfilename
from Verification.MNI_verification import patient_mni_verification

import nibabel as nib
import numpy as np
import glob
import os

atlas_mask = nib.load("/home/adamzakieh/PycharmProjects/MRI-Pipeline/Brain scans/myaparc_60wm5max_Dil_with_Subcortical_Regions_2mm.nii.gz").get_fdata()
atlas_mask = (atlas_mask > 0).astype(float)

MNI152_2mm_Shape = (91, 109, 91)
MNI152_2mm_Affine = np.array([
    [-2,  0,  0,  90],
    [ 0,  2,  0, -126],
    [ 0,  0,  2,  -72],
    [ 0,  0,  0,   1]
], dtype=float)


Tk().withdraw()
filename = askopenfilename()

def z_score(patient):
    patient_mni_verification(patient)

    patient_img = nib.load(patient)
    mean_img = nib.load("Brain scans/mean_map.nii.gz")
    sd_img = nib.load("Brain scans/sd_map.nii.gz")

    patient_data = patient_img.get_fdata()
    patient_data = patient_data * atlas_mask
    mean_data = mean_img.get_fdata()
    sd_data = sd_img.get_fdata()

    z_score_map = (patient_data - mean_data) / sd_data
    z_score_map[~atlas_mask] = 0

    return z_score_map

base_file = os.path.basename(filename)
base_root = os.path.splitext(base_file)
file_root = os.path.splitext(base_root)

patient_z_score_map = z_score(filename)

patient_z_score_img = nib.Nifti1Image(patient_z_score_map, MNI152_2mm_Affine)
nib.save(patient_z_score_img, "../Brain scans/" + file_root + "_z_score.nii.gz")












