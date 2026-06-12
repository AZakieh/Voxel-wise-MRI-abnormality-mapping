import nibabel as nib
import numpy as np
import glob

files = glob.glob("../Brain scans/Control scans/**/*FA*.nii.gz", recursive=True)

MNI152_2mm_Shape = (91, 109, 91)
MNI152_2mm_Affine = np.array([
    [-2,  0,  0,  90],
    [ 0,  2,  0, -126],
    [ 0,  0,  2,  -72],
    [ 0,  0,  0,   1]
], dtype=float)

def control_mni_verification(brain_scans):
    for scan in brain_scans:
        img = nib.load(scan)
        if img.shape != MNI152_2mm_Shape:
            print(scan)

        if not np.allclose(img.affine, MNI152_2mm_Affine, atol=1e-3):
            print(scan)

def patient_mni_verification(scan):
        img = nib.load(scan)
        if img.shape != MNI152_2mm_Shape:
            raise ValueError

        if not np.allclose(img.affine, MNI152_2mm_Affine, atol=1e-3):
            raise ValueError

control_mni_verification(files)