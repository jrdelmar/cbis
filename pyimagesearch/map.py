# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 02:25:37 2019
@author: user
Description:
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import cartopy.feature as cfeature

from pyimagesearch.utils import log


# create the map only when the file is not yet created
def create_map(img_name, map_path, lat, lon):
    fig = plt.figure(figsize=(15, 5))
    # ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.LambertCylindrical())

    # make the map global rather than have it zoom in to
    # the extents of any plotted data
    ax.set_global()

    # add feature
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # ax.coastlines(resolution='110m')
    ax.coastlines()
    ax.gridlines()

    ax.set_title("GPS Coordinates for {}\nLat:{} Lon:{}".format(img_name, lat, lon))

    ax.plot(lon, lat,
            marker='o',
            markersize=5.0,  # markeredgewidth=1.0,
            markeredgecolor='red', markerfacecolor='red',
            linestyle='None', transform=ccrs.LambertCylindrical())
    lonr, latr = ccrs.LambertCylindrical().transform_point(lon, lat, ccrs.PlateCarree())

    ax_sub = inset_axes(ax, width=2, height=2,
                        bbox_to_anchor=(-110, 10),
                        bbox_transform=ax.transData,
                        borderpad=0)

    ax_sub.axis('Off')
    ax_sub.set_aspect("equal")

    plt.savefig(map_path, bbox_inches='tight', pad_inches=.2, dpi=300)

    log("[INFO] Map created and saved {}".format(map_path), True)  # always verbose
