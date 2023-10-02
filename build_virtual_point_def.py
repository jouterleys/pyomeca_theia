# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 16:28:44 2023

@author: Blast

Try to build a function that will make it easier to export 3 virtual points per segment to load into opensim

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

# Extract proximal_pose pose
proximal_pose = rotation_data_transposed[keysList.index('l_thigh_4X4')]
# Convert the last colum to meters?
proximal_pose[0:3, 3,:] /= 1000
# Extract Origin
proximal_pose_origin = proximal_pose[:,3,:]
# Add dimension
proximal_pose_origin = proximal_pose_origin[:,np.newaxis]

# Extract distal_pose pose
distal_pose = rotation_data_transposed[keysList.index('l_shank_4X4')]
# Convert the last colum to meters?
distal_pose[0:3, 3,:] /= 1000
# Extract Origin
distal_pose_origin = distal_pose[:,3,:]
# Add dimension
distal_pose_origin = distal_pose_origin[:,np.newaxis]

# Calculate segment length (proximal to distal segment)
valid_points = ~np.isnan(proximal_pose_origin[1]) & ~np.isnan(distal_pose_origin[1])
point1 = proximal_pose_origin[0:3,valid_points]
point2 = distal_pose_origin[0:3,valid_points]
segment_length = []
for frame in range(np.sum(valid_points)):
    diff = point1[:,frame] - point2[:,frame] 
    norm = np.linalg.norm(diff)
    segment_length.append(norm)
segment_length = np.mean(segment_length)


# Need to find points in global 
proximal_pose_mid_local = np.array([0, -0.5*segment_length,-0.5*segment_length,1])
proximal_pose_lat_local = np.array([0, 0.5*segment_length,-0.5*segment_length,1])


