import numpy as np

from visbrain.objects import ConnectObj, SceneObj, SourceObj, BrainObj
from visbrain.io import download_file

from matplotlib import pyplot as plt
from scipy import spatial
from scipy import signal

import os
os.chdir('C:/Users/AlbalooCo/Downloads/BCI_EX/EX4')

sc = SceneObj(bgcolor= "black", size=(500, 500))

nodes=np.array(coords)
edges=correlation_matrix[:len(nodes), :len(nodes)]

# nodes
# Coloring method
color_by = 'strength'

# Because we don't want to plot every connections, we only keep connections
# above .7
select = edges > .5
# Define the connectivity object
c_default = ConnectObj('default', nodes, edges, select=select, line_width=2.,
                       cmap='Spectral_r', color_by=color_by)
                       
# Then, we define the sources
s_obj = SourceObj('sources', nodes, color='#ab4642', radius_min=15.)
sc.add_to_subplot(c_default, title='Color by connectivity strength')

# And add connect, source and brain objects to the scene
brain_obj = BrainObj('B1', sulcus=True, verbose=True)
sc.add_to_subplot(brain_obj, use_this_cam=True, rotate='right')

sc.preview()

