import numpy as np

from visbrain.objects import BrainObj, ColorbarObj, SceneObj, SourceObj
from visbrain.utils import generate_eeg, convert_meshdata, vispy_array

from visbrain.config import CONFIG

from vispy.app import Timer

scene = SceneObj(bgcolor='white', size=(1400, 1000))

# Colorbar default arguments. See `visbrain.objects.ColorbarObj`
CBAR_STATE = dict(cbtxtsz=12, txtsz=10., width=.1, cbtxtsh=3.,
                  rect=(-.3, -2., 1., 4.))

KW = dict(title_size=14., zoom=2)

colormap = 'inferno'

# load brain model
verts = np.load('bnd4_pos1.npy')
faces = np.load('bnd4_tri1.npy')

verts *= 1000

verts, faces, normals = convert_meshdata(verts, faces, invert_normals=True)


# generate random toy data
n_channels = 40
sampling_frequency = 512
data, time = generate_eeg(n_channels=n_channels, sf=sampling_frequency)

print(data.shape)

NSources = 200
index = np.random.choice(verts.shape[0], n_channels, replace=False)
xyz = verts[index]



brain_obj = BrainObj('Custom',
                     vertices=verts, faces=faces, normals=normals,
                     translucent=False)



source_object = SourceObj('iEEG', xyz, data=data[:, 0], cmap=colormap)

# Project source's activity
source_object.project_sources(brain_obj)
source_object.color_sources(data=data[:, 0])


# Finally, add the source and brain objects to the subplot
scene.add_to_subplot(source_object, row=0, col=0, title='Project iEEG data', **KW)
scene.add_to_subplot(brain_obj, row=0, col=0, rotate='left', use_this_cam=True)

# Finally, add the colorbar :
colorbar = ColorbarObj(source_object, cblabel='Projection of niEEG data', **CBAR_STATE)
scene.add_to_subplot(colorbar, row=0, col=1, width_max=200, rotate='up')

# Animation

app_timer = Timer(app=CONFIG['VISPY_APP'], interval='auto', iterations=-1)

def on_timer(*args, **kwargs):
    if hasattr(brain_obj, 'camera'):
        brain_obj.camera.azimuth += 1
        t = app_timer.elapsed
        frame = int(np.floor(t * sampling_frequency))

        new_data = data[:, frame % data.shape[1]].ravel()
        source_object._data = vispy_array(new_data)
        source_object.update()
        source_object.project_sources(brain_obj)
        source_object.color_sources()

app_timer.connect(on_timer)
app_timer.start()


scene.preview()
