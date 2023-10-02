# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 16:28:44 2023

@author: Blast
"""
#%% Imports
import os
import tkinter
from tkinter import filedialog

from pyomeca import Rototrans, Markers

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

# Extract l_thigh pose
l_thigh_4X4 = rotation_data_transposed[keysList.index('l_thigh_4X4')]
# Convert the last colum to meters?
l_thigh_4X4[0:3, 3,:] /= 1000
# Turn into pyomeca Rototrans object
l_thigh_4X4 = Rototrans(l_thigh_4X4)

# Extract Origin
l_thigh_origin = l_thigh_4X4[:,3,:].data
l_thigh_origin = l_thigh_origin[:,np.newaxis]
l_thigh_origin = Markers(l_thigh_origin)
# Plot Origin
l_thigh_origin.isel(axis=2).plot.line(x="time")
# Check first frame
l_thigh_origin.isel(time=0)

# Extract l_shank pose
l_shank_4X4 = rotation_data_transposed[keysList.index('l_shank_4X4')]
# Convert the last colum to meters?
l_shank_4X4[0:3, 3,:] /= 1000
# Turn into pyomeca Rototrans object
l_shank_4X4 = Rototrans(l_shank_4X4)

# Extract Origin
l_shank_origin = l_shank_4X4[:,3,:].data
l_shank_origin = l_shank_origin[:,np.newaxis]
l_shank_origin = Markers(l_shank_origin)
# Plot Origin
l_shank_origin.isel(axis=2).plot.line(x="time")
# Check first frame
l_shank_origin.isel(time=0)

# Calculate segment length (proximal to distal segment)
valid_points = ~np.isnan(l_thigh_origin.data[1]) & ~np.isnan(l_shank_origin.data[1])
point1 = l_thigh_origin.data[0:3,valid_points]
point2 = l_shank_origin.data[0:3,valid_points]
segment_length = []
for frame in range(np.sum(valid_points)):
    diff = point1[:,frame] - point2[:,frame] 
    norm = np.linalg.norm(diff)
    segment_length.append(norm)
segment_length = np.mean(segment_length)

l_thigh_mid = np.array([0, -0.5*segment_length,-0.5*segment_length])
l_thigh_lat = np.array([0, 0.5*segment_length,-0.5*segment_length])





