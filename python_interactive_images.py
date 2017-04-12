import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import astropy.io.fits as pyfits
import pylab
import img_scale
from matplotlib.widgets import Slider, Button, RadioButtons


plt.clf()
plt.cla()
plt.close()

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)

g_image = pyfits.getdata('Sombrero_SDSS_g-band.fits.gz')
r_image = pyfits.getdata('Sombrero_SDSS_r-band.fits.gz')
u_image = pyfits.getdata('Sombrero_SDSS_u-band.fits.gz')

data = img_scale.asinh(g_image)


#data = mpimg.imread('stinkbug.png')[:,:,0] # pick one channel of a PNG

l = pylab.imshow(data, cmap='Greys_r')

# Add scale slider
axcolor = 'lightgoldenrodyellow'

ax_scaling = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
s_scale = Slider(ax_scaling, 'Scale', np.nanmin(data), np.nanmax(data), valinit=(np.nanmax(data)-np.nanmin(data)/2.))


def update(val):
    scale = s_scale.val
    l.set_clim(scale)
    fig.canvas.draw_idle()

s_scale.on_changed(update)



# Add color buttons
rax = plt.axes([0.025, 0.5, 0.15, 0.15], axisbg=axcolor)
radio = RadioButtons(rax, ('Greys_r', 'Reds_r', 'Greens_r','Blues_r'), active=0)


def colorfunc(label):
    l.set_cmap(label)
    fig.canvas.draw_idle()

radio.on_clicked(colorfunc)



# Add a reset button
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
resetbutton = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    #s_scale.reset()
    l.set_cmap('Greys_r')
    radio.set_active(0)
resetbutton.on_clicked(reset)


# Make a combined image from your best scaled values
img_rgb = np.zeros((g_image.shape[0], g_image.shape[1], 3), dtype=float)
img_rgb[:,:,0] = img_scale.asinh(g_image)
img_rgb[:,:,1] = img_scale.asinh(r_image)
img_rgb[:,:,2] = img_scale.asinh(u_image)


# Add a combine button

combo_ax = plt.axes([0.5, 0.025, 0.1, 0.04])
combobutton = Button(combo_ax, 'Combine', color=axcolor, hovercolor='0.975')

def combine(event):
    l.set_data(img_rgb)
    s_scale.reset()
combobutton.on_clicked(combine)


plt.show()