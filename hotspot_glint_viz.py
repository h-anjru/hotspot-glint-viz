import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d.art3d import Line3DCollection

from givens3D import givens3D


### CAMERA PARAMETERS ###
f = 3652  # pixels
x_format = 5472  # pixels
y_format = 3648  # pixels

# shorthand to make plotting image lines easier
xx = x_format / 2
yy = y_format / 2


### INPUT ###
# sun paramters [deg]
az, elev = input('Sun: azimuth and elevation [deg]: ').split()
az_elev = [az, elev]

# convert user input
for idx, value in enumerate(az_elev):
    az_elev[idx] = math.radians(float(value))

# camera rotation [degrees]
o, p, k = input('Image: omega phi kappa [deg]: ').split()
opk = [o, p, k]

# convert user input
for idx, value in enumerate(opk):
    opk[idx] = math.radians(float(value))


### SUN ###
# begin with a default sun pointed azimuth 0, elevation 0
sun_north_horizon = (0, 1.5 * f, 0)

def sun_rotmat(azimuth, elevation):
    """Build a direct rotation matrix based on CW azimuth and elevation."""
    rotmat_azimuth = givens3D('z', azimuth, inverse=True)
    rotmat_elevation = givens3D('x', elevation)

    rotmat = rotmat_azimuth @ rotmat_elevation

    return rotmat


# rotate the sun...
sun_rotmat = sun_rotmat(az_elev[0], az_elev[1])
sun_rotated = sun_rotmat @ sun_north_horizon

# ...then make the sun vector antiparllel (not where it's from but where it's going)...
sun_rotated = -sun_rotated

# ...and flip the rotation in the XY-plane
reflection_rotated = -sun_rotated
reflection_rotated[-1] = sun_rotated[-1]


### CAMERA ###
# these vectors form the camera
camera_ENU = {
    'origin': (0, 0, 0),
    'x_axis': (xx, 0, -f),
    'y_axis': (0, yy, -f),
    'focal': (0, 0, -f),
    'ne': (xx, yy, -f),
    'nw': (-xx, yy, -f),
    'sw': (-xx, -yy, -f),
    'se': (xx, -yy, -f),
}

def direct_rotmat(omega, phi, kappa):
    """Build a *direct* rotation matrix."""
    rotmat_o = givens3D('x', omega)
    rotmat_p = givens3D('y', phi)
    rotmat_k = givens3D('z', kappa)

    rotmat = rotmat_k @ rotmat_p @ rotmat_o

    return rotmat


# rotate the camera parallel to ENU, store as new camera
rotmat = direct_rotmat(opk[0], opk[1], opk[2])

camera = camera_ENU

for key, vector in camera_ENU.items():
    camera[key] = rotmat @ vector


### SUN & CAMERA INTERSECTIONS ###
# where does the sun intersect the image plane?
x = camera['focal']  # shorten name for ease of typing
hotspot = np.dot(x, x) / np.dot(sun_rotated, x) * sun_rotated
glint = np.dot(x, x) / np.dot(reflection_rotated, x) * reflection_rotated


### LINES TO DRAW ###
# lines to be drawn from camera vectors
lines = [
    [camera['focal'], camera['x_axis']],
    [camera['focal'], camera['y_axis']],
    [camera['origin'], camera['focal']],
    [camera['ne'], camera['nw']],
    [camera['nw'], camera['sw']],
    [camera['sw'], camera['se']],
    [camera['se'], camera['ne']],
    [camera['origin'], hotspot],
    [camera['origin'], glint],
]

colors = np.array(
    [
        (1, 0, 0, 1),  # image x-axis
        (0, 1, 0, 1),  # image y-axis
        (0, 0, 1, 1),  # focal axis
        (0, 0, 0, 1),  # camera edges
        (0, 0, 0, 1),
        (0, 0, 0, 1),
        (0, 0, 0, 1),
        (1, 0.6, 0, 1),  # hotspot
        (1, 0.9, 0, 1),  # glint
    ]
)

legend = [
    'test'
]



lines_colors = Line3DCollection(lines, colors=colors, linewidths=2)


### PLOT ###
# plot parameters
fig = plt.figure(figsize=(4, 4))
ax = plt.axes(projection='3d')
ax.grid()
ax.set_title('Sun glint & hotspot visualizer')

# aet axes labels
ax.set_xlabel('E [pix]', labelpad=20)
ax.set_ylabel('N [pix]', labelpad=20)
ax.set_zlabel('U [pix]', labelpad=20)

# set axis limits
buffer = 500  # pixels
ax.set_xlim(-(xx + buffer), xx + buffer)
ax.set_ylim(-(yy + buffer), yy + buffer)
ax.set_zlim(-(f + buffer), 0 + buffer)

# set aspect (https://stackoverflow.com/a/65181861)
world_limits = ax.get_w_lims()
ax.set_box_aspect(
    (
        world_limits[1] - world_limits[0],
        world_limits[3] - world_limits[2],
        world_limits[5] - world_limits[4]
    )
)

# add the lines...
ax.add_collection(lines_colors)

# ...fke some data to create a legend... (https://stackoverflow.com/a/27449483)
fake_hotspot = mpl.lines.Line2D([0], [0], linestyle="none", c=(1, 0.6, 0), marker = 'o')
fake_glint = mpl.lines.Line2D([0], [0], linestyle="none", c=(1, 0.9, 0), marker = 'o')
ax.legend([fake_hotspot, fake_glint], ['hotspot', 'glint'], numpoints = 1)

# ...add some text about user input...
ax.text(50, 50, 50, f'az = {az} // elev = {elev}', fontsize=10)
ax.text(300, 300, -f, f'opk = ({o}, {p}, {k})', fontsize=10)

# ...and voila
plt.show()
