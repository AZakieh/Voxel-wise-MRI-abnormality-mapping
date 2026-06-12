from tkinter import Tk
from tkinter.filedialog import askopenfilename

import nibabel as nib
import numpy as np
import glob


Tk().withdraw()
filename = askopenfilename()
