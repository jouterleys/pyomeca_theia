# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 13:46:43 2023

@author: Jereme Outerleys
"""
#%% Imports
import os
import tkinter
from tkinter import filedialog

from pyomeca import Rototrans, Markers

from scipy.signal import find_peaks
import matplotlib.pyplot as plt

from ezc3d import c3d
import numpy as np

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

trial_length = c['header']['points']['last_frame'] + 1
# Get list of segment pose matricies
keysList = c['parameters']['ROTATION']['LABELS']['value']
#print(keysList)

# Get rotation data
rotation_data = c['data']['rotations']
# Reorder rotation data to make pose label first last (not required)
rotation_data_transposed  = np.transpose(rotation_data, (2, 0, 1, 3))

#print(list(c['parameters']))
#print(list(c['parameters']['THEIA3D']))
#print(list(c['parameters']['THEIA3D']['LHEEL_POS']['value']))

LHEEL_POS = c['parameters']['THEIA3D']['LHEEL_POS']['value']
RHEEL_POS = c['parameters']['THEIA3D']['RHEEL_POS']['value']

# Add ones to last row
LHEEL_POS = np.vstack((LHEEL_POS, np.ones((1, 1))))
# Add frame/time dimension
LHEEL_POS = LHEEL_POS[:,np.newaxis]
# Repeat for length of trial
LHEEL_POS = np.repeat(LHEEL_POS, trial_length, axis=2)
# Turn into pyomeca Markers object
LHEEL_POS_Markers = Markers(LHEEL_POS)

# Extract l_foot pose
l_foot_4X4 = rotation_data_transposed[keysList.index('l_foot_4X4')]
# Convert the last colum to meters?
l_foot_4X4[0:3, 3,:] /= 1000
# Turn into pyomeca Rototrans object
l_foot_4X4 = Rototrans(l_foot_4X4)

# Get location of LHEEL in Global
L_HEEL = Markers.from_rototrans(LHEEL_POS_Markers, l_foot_4X4)
# Plot LHEEL
L_HEEL.sel(axis='z').plot.line(x="time")
# Check first frame
L_HEEL.isel(time=0)

# Get LHEEL with respect to Pelvis (i.e. Zeni)
# Extract l_foot pose
pelvis_shifted_4X4 = rotation_data_transposed[keysList.index('pelvis_shifted_4X4')]
# Convert the last colum to meters?
pelvis_shifted_4X4[0:3, 3,:] /= 1000
# Turn into pyomeca Rototrans object
pelvis_shifted_4X4 = Rototrans(pelvis_shifted_4X4)
# Find transpose
pelvis_shifted_4X4_t = Rototrans.from_transposed_rototrans(pelvis_shifted_4X4)
# LHEEL_pelvis
LHEEL_wrt_pelvis = Markers.from_rototrans(L_HEEL, pelvis_shifted_4X4_t)
# Plot y component
LHEEL_wrt_pelvis.sel(axis='y').plot.line(x="time")
# Find peaks for Heel Strikes Zeni
peaks, _ = find_peaks(LHEEL_wrt_pelvis.sel(axis='y').data.flatten())
# Plot
for peak in peaks:
    plt.axvline(x=peak,color='g')
ax = plt.gca()
ax.set_xlim(1000,2000)
plt.show()
