# -*- coding: utf-8 -*-
"""
@author: Jereme Outerleys

"""
#%% Imports
import os
import tkinter
from tkinter import filedialog

from pyomeca import Rototrans, Angles
from ezc3d import c3d
import numpy as np

import matplotlib.pyplot as plt


# Reset tkinter
root = tkinter.Tk()
root.withdraw()
root.call('wm', 'attributes', '.', '-topmost', True)

c3d_file = filedialog.askopenfilename(title='Select theia c3d')

c3d_file = os.path.normpath(c3d_file)

c = c3d(c3d_file)
# Get list of parameters
#keysList = list(c['parameters'])
#print(keysList)

# Get list of segment pose matricies
keysList = c['parameters']['ROTATION']['LABELS']['value']
#print(keysList)

# Get rotation data
rotation_data = c['data']['rotations']
# Reorder rotation data to make pose label first last (not required)
rotation_data_transposed  = np.transpose(rotation_data, (2, 0, 1, 3))

l_thigh_4X4 = rotation_data_transposed[keysList.index('l_thigh_4X4')]

l_shank_4X4 = rotation_data_transposed[keysList.index('l_shank_4X4')]

l_thigh_rt = Rototrans(l_thigh_4X4)

l_shank_rt = Rototrans(l_shank_4X4)

l_thigh_rt_t = Rototrans.from_transposed_rototrans(l_thigh_rt)

#l_knee_rt = l_thigh_rt_t.meca.matmul(l_shank_rt) doesn't work

l_knee_rt = np.einsum('ijt, jkt -> ikt', l_thigh_rt_t, l_shank_rt)

l_knee_rt = Rototrans(l_knee_rt)

l_knee_angles = Angles.from_rototrans(l_knee_rt,'xyz')

l_knee_angles = np.degrees(l_knee_angles)

ax = plt.gca()
l_knee_angles.sel(axis=0).plot.line(x="time")
ax.set_xlim(1000,1300)
plt.show()
