import nibabel as nib
import glob

files = glob.glob("../Brain scans/Control scans/**/*FA*.nii.gz", recursive=True)

def control_voxel_verification(files):
    for scan in files:
        img = nib.load(scan)
        data = img.get_fdata()
        outside_mask = (data < 0) | (data > 1)
        pct_outside = outside_mask.sum() / data.size * 100
        if pct_outside > 1:
            print(pct_outside, scan)


control_voxel_verification(files)


