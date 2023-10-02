# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 19:37:33 2023

@author: Blast
"""

# Extract l_thigh pose
pelvis_4X4 = rotation_data_transposed[keysList.index('pelvis_4X4')]
# Convert the last colum to meters?
pelvis_4X4[0:3, 3,:] /= 1000
# Turn into pyomeca Rototrans object
pelvis_4X4 = Rototrans(pelvis_4X4)

# Extract Origin
pelvis_origin = pelvis_4X4[:,3,:].data
pelvis_origin = pelvis_origin[:,np.newaxis]
pelvis_origin = Markers(pelvis_origin)
# Plot Origin
pelvis_origin.isel(axis=2).plot.line(x="time")
# Check first frame
pelvis_origin.isel(time=0)

# Extract l_shank pose
pelvis_shifted_4X4 = rotation_data_transposed[keysList.index('pelvis_shifted_4X4')]
# Convert the last colum to meters?
pelvis_shifted_4X4[0:3, 3,:] /= 1000
# Turn into pyomeca Rototrans object
pelvis_shifted_4X4 = Rototrans(pelvis_shifted_4X4)

# Extract Origin
pelvis_shifted_origin = pelvis_shifted_4X4[:,3,:].data
pelvis_shifted_origin = pelvis_shifted_origin[:,np.newaxis]
pelvis_shifted_origin = Markers(pelvis_shifted_origin)
# Plot Origin
pelvis_shifted_origin.isel(axis=2).plot.line(x="time")
# Check first frame
pelvis_shifted_origin.isel(time=0)

# Calculate segment length (proximal to distal segment)
valid_points = ~np.isnan(pelvis_4X4.data[1]) & ~np.isnan(pelvis_shifted_4X4.data[1])
point1 = pelvis_4X4.data[0:3,valid_points]
point2 = pelvis_shifted_4X4.data[0:3,valid_points]
segment_length = []
for frame in range(np.sum(valid_points)):
    diff = point1[:,frame] - point2[:,frame] 
    norm = np.linalg.norm(diff)
    segment_length.append(norm)
segment_length = np.mean(segment_length)

segment_length