import nibabel as nib
import numpy as np
import glob

files = glob.glob("../Brain scans/Control scans/**/*FA*.nii.gz", recursive=True)
atlas_mask = nib.load("/home/adamzakieh/PycharmProjects/MRI-Pipeline/Brain scans/myaparc_60wm5max_Dil_with_Subcortical_Regions_2mm.nii.gz").get_fdata()
atlas_mask = (atlas_mask > 0).astype(float)

MNI152_2mm_Shape = (91, 109, 91)
MNI152_2mm_Affine = np.array([
    [-2,  0,  0,  90],
    [ 0,  2,  0, -126],
    [ 0,  0,  2,  -72],
    [ 0,  0,  0,   1]
], dtype=float)

class WelfordVariance:
    def __init__(self):
        self.mean = 0.0
        self.count = 0
        self.M2 = 0.0

    def add_variable(self, x: np.ndarray):
        self.count += 1
        old_mean = self.mean
        self.mean += (x - self.mean) / self.count
        self.M2 += (x - old_mean) * (x - self.mean)

    def remove_variable(self, x: np.ndarray):
        self.count -= 1
        new_mean = self.mean
        self.mean -= (x - self.mean) / self.count
        self.M2 -= (x - new_mean) * (x - self.mean)

    def get_mean(self) -> np.ndarray:
        return self.mean

    def get_sample_variance(self) -> np.ndarray:
        return self.M2 / (self.count - 1)

Welford = WelfordVariance()


for scan in files:
    img = nib.load(scan)
    data = img.get_fdata()
    data = data * atlas_mask
    data = np.clip(data, 0, 1)
    Welford.add_variable(data)
    del img, data

mean_map = Welford.get_mean()
sd_map = np.sqrt(Welford.get_sample_variance())

mean_img = nib.Nifti1Image(mean_map, MNI152_2mm_Affine)
nib.save(mean_img, "../Brain scans/mean_map.nii.gz")

sd_img = nib.Nifti1Image(sd_map, MNI152_2mm_Affine)
nib.save(sd_img, "../Brain scans/sd_map.nii.gz")
