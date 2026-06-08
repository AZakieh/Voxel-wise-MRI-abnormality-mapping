import nibabel as nib
import matplotlib.pyplot as plt
import glob

files = glob.glob("../Brain scans/Control scans/**/*FA*.nii.gz", recursive=True)
for scan in files:
    img = nib.load(scan)
    data = img.get_fdata().flatten()
    plt.hist(data)
    del img, data

plt.show()