# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 13:46:43 2023

@author: Jereme Outerleys
"""
#%% Imports
import os
import tkinter
from tkinter import filedialog

from pyomeca import Rototrans, Angles, Markers
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
# Turn into pyomeca Rototrans object
l_foot_4X4 = Rototrans(l_foot_4X4)
# Get location of LHEEL in Global
LHEEL = Markers.from_rototrans(LHEEL_POS_Markers, l_foot_4X4)
# Plot LHEEL
LHEEL.isel(axis=1).plot.line(x="time")