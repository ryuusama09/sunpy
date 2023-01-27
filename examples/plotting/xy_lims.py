"""
==================================
Set Axis Range When Plotting a Map
==================================

In this example we are going to look at how to set the axes
range using Matplotlib's ``set_xlim`` and ``set_ylim`` when plotting a
Map with WCSAxes.
"""
import matplotlib.pyplot as plt

import astropy.units as u
from astropy.coordinates import SkyCoord

import sunpy.data.sample
import sunpy.map
from sunpy.map import PixelPair
###############################################################################
# Lets start by creating a Map from the sample data.

aia_map = sunpy.map.Map(sunpy.data.sample.AIA_171_IMAGE)

###############################################################################
# Now lets say for example we are only interested in plotting a certain region
# of this Map. One way this could be done is to create a submap over the region
# of interest and then plotting that. Another useful way is to set the axes
# range over which to plot using Matplotlib's
# `~matplotlib.axes.Axes.set_xlim` and `~matplotlib.axes.Axes.set_ylim` functionality.
# The axes that Matplotlib uses is in pixel coordinates (e.g. of image data array)
# rather than world coordinates (e.g. in arcsecs) so we need to define our limits that
# are passed to `~matplotlib.axes.Axes.set_xlim`, `~matplotlib.axes.Axes.set_ylim` to pixel coordinates.
# We can define our limits we want to use in world coordinates and then work out what pixel
# coordinates these correspond to.
# Lets choose x-limits and y-limits in arcsecs that we are interested in.

xlims_world = [500, 1100]*u.arcsec
ylims_world = [-800, 0]*u.arcsec

###############################################################################
# We can then convert these into a SkyCoord which can be passed to :func:`~sunpy.map.GenericMap.world_to_pixel` to
# determine which pixel coordinates these represent on the Map.

world_coords = SkyCoord(Tx=xlims_world, Ty=ylims_world, frame=aia_map.coordinate_frame)
pixel_coords_x , pixel_coords_y = aia_map.wcs.world_to_pixel(world_coords)
pixel_coords = PixelPair(pixel_coords_x*u.pixel,pixel_coords_y*u.pixel)


#pixel_coords = PixelPair(pixel_coords_x,pixel_coords_y)

ylims_pixel = pixel_coords.y.value

###############################################################################
# We can now plot this Map and then use the x_lims_pixel and y_lims_pixel to set
# the range of the axes for which to plot.

fig = plt.figure()
ax = fig.add_subplot(projection=aia_map)
aia_map.plot(axes=ax, clip_interval=(1, 99.9)*u.percent)
ax.set_xlim(xlims_pixel)
ax.set_ylim(ylims_pixel)

plt.show()
