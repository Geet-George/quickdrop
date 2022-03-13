import xarray as xr
import numpy as np
import cartopy as cp
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.feature import LAND
import cartopy.feature as cfeature
from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.dates as mdates
import logging

########## Launch Map ##########
def launch_locations_map(ds_flight, flight_dir):

    print("Plotting launch locations with IWV...")

    fig = plt.figure()

    ax = plt.axes(projection=ccrs.AzimuthalEquidistant())
    ax.coastlines(resolution="50m", linewidth=1.5)

    ax.plot(
        ds_flight["lon"].isel(alt=-700),
        ds_flight["lat"].isel(alt=-700),
        c="grey",
        linestyle=':',
        transform=ccrs.PlateCarree(),
    )

    im = ax.scatter(
        ds_flight["lon"].isel(alt=-700),
        ds_flight["lat"].isel(alt=-700),
        marker="o",
        edgecolor="grey",
        s=60,
        transform=ccrs.PlateCarree(),
        c=ds_flight["iwv"],
        cmap="gist_earth_r",
    )

    krn_lat = 67.8207
    krn_lon = 20.3331
    ax.text(krn_lon+0.05,krn_lat+0.05,'KRN',fontsize=10,
            c='red',transform=ccrs.PlateCarree())
    ax.scatter(krn_lon,krn_lat,marker='*',s=40,c='salmon',edgecolor='k',linewidth=0.5,
    transform=ccrs.PlateCarree())

    lyr_lat = 78.2461
    lyr_lon = 15.4656

    ax.text(lyr_lon+0.05,lyr_lat+0.05,'LYR',fontsize=10,
            c='red',transform=ccrs.PlateCarree())
    ax.scatter(lyr_lon,lyr_lat,marker='*',s=40,c='salmon',edgecolor='k',linewidth=0.5,
    transform=ccrs.PlateCarree())


    # Defining boundaries of the plot
    lon_w = -25
    lon_e = 25
    lat_s = 65
    lat_n = 83

    ax.set_extent([lon_w, lon_e, lat_s, lat_n], crs=ccrs.PlateCarree())

    # Assigning axes ticks

    xticks = np.arange(-180, 180, 4)
    yticks = np.arange(-90, 90, 4)

    # Setting up the gridlines

    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        linewidth=1,
        color="gray",
        alpha=0.2,
        linestyle="--",
    )
    gl.xlocator = mticker.FixedLocator(xticks)
    gl.ylocator = mticker.FixedLocator(yticks)
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {"size": 12, "color": "k"}
    gl.ylabel_style = {"size": 12, "color": "k"}

    cax = fig.add_axes([0.08, -0.05, 0.85, 0.02])
    g = fig.colorbar(
        im,
        cax=cax,
        orientation="horizontal",
        shrink=0.5,
    )  # ,fraction=0.2)

    g.set_label("Integrated Water Vapour (kg m$^{-2}$)", fontsize=12)
    plt.tick_params(labelsize=15)

    save_filepath = f"{flight_dir.quickplot_path()}HALO-AC3_HALO_Dropsondes_launch-locations-iwv__{flight_dir.flightdir}.png"

    plt.savefig(save_filepath, dpi=300, bbox_inches="tight")

    logging.info(f"Saved:{save_filepath}")


# Lat-time plot
def lat_time_plot(ds_flight, flight_dir):
    
    print("Plotting spatio-temporal variation (lat v/s time) with IWV...")

    ax = plt.figure(figsize=(15, 5))
    plt.scatter(
        ds_flight["launch_time"].values,
        ds_flight["lat"].isel(alt=-700).values,
        s=90,
        c=ds_flight["iwv"],edgecolor='grey',
        cmap="gist_earth_r",
    )
    plt.xlim(
        np.min(ds_flight["launch_time"].values) - np.timedelta64(4, "m"),
        np.max(ds_flight["launch_time"].values) + np.timedelta64(4, "m"),
    )
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    g = plt.colorbar()
    g.set_label("IWV / kg m$^{-2}$", fontsize=12)

    myFmt = mdates.DateFormatter("%H:%M")
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.xlabel("Time / UTC", fontsize=24)
    plt.ylabel("Latitude / $\degree$N", fontsize=24)

    save_filepath = f"{flight_dir.quickplot_path()}HALO-AC3_HALO_Dropsondes_spatiotemporal-variation-iwv_{flight_dir.flightdir}.png"

    plt.savefig(
        save_filepath,
        dpi=300,
        bbox_inches="tight",
    )

    logging.info(f"Plot Saved:{save_filepath}")


def profiles(ds_flight, flight_dir):

    

    row = 1
    col = 4

    f, ax = plt.subplots(row, col, sharey=True, figsize=(12, 6))

    r = ["tdry", "theta", "rh", "wspd", "wdir"]
    r_titles = [
        "T / $\degree$C",
        "$\\theta$ / K",
        "RH / %",
        "Wind speed / ms$^{-1}$",
        "Wind direction / $\degree$",
    ]

    print(f"Plotting vertical profiles of {r}...")

    for j in range(col):
        d = ds_flight[r[j]]
        for i in range(1, len(ds_flight["launch_time"]) - 1):
            #     if i != 11
            ax[j].plot(
                d.isel(launch_time=i),
                ds_flight["alt"] / 1000,
                c="grey",
                alpha=0.25,
                linewidth=0.5,
            )

        ax[j].plot(
            np.nanmean(d, axis=0),
            ds_flight["alt"] / 1000,
            linewidth=3,
            c="k",
        )
        ax[j].set_xlabel(r_titles[j], fontsize=14)
        ax[j].spines["right"].set_visible(False)
        ax[j].spines["top"].set_visible(False)
        if j == 0:
            ax[j].set_ylabel("Altitude (km)", fontsize=14)

    save_filepath = f"{flight_dir.quickplot_path()}HALO-AC3_HALO_Dropsondes_vertical-profiles-measured-quantities_{flight_dir.flightdir}.png"

    plt.savefig(save_filepath, dpi=300, bbox_inches="tight")

    logging.info(f"Plot Saved:{save_filepath}")


def drift_plots(ds_flight, flight_dir):
    
    print("Plotting drift in lat and lon...")

    f, ax = plt.subplots(1, 2, sharey=True, figsize=(10, 5))

    for i in range(len(ds_flight["launch_time"])):

        max_id = np.max(np.where(~np.isnan(ds_flight["lon"].isel(launch_time=i))))

        ax[0].plot(
            ds_flight["lat"].isel(launch_time=i)
            - ds_flight["lat"].isel(launch_time=i).isel(alt=max_id),
            ds_flight["alt"],
            linewidth=1.5,
            c="grey",
            alpha=0.75,
        )
        # ax[0].plot(
        #     np.mean(ds_flight["lat"] - ds_flight["lat"].isel(alt=max_id), axis=1),
        #     ds_flight["alt"],
        #     linewidth=2,
        #     c="k",
        #     alpha=1,
        # )
        ax[0].set_xlabel("Drift in Latitude ($\degree$)", fontsize=14)
        ax[0].set_ylabel("Altitude", fontsize=14)
        ax[0].spines["right"].set_visible(False)
        ax[0].spines["top"].set_visible(False)

        ax[1].plot(
            ds_flight["lon"].isel(launch_time=i)
            - ds_flight["lon"].isel(launch_time=i).isel(alt=max_id),
            ds_flight["alt"],
            linewidth=1.5,
            c="grey",
            alpha=0.75,
        )
        # ax[1].plot(
        #     np.mean(ds_flight["lon"] - ds_flight["lon"].isel(alt=max_id), axis=1),
        #     ds_flight["alt"],
        #     linewidth=2,
        #     c="k",
        #     alpha=1,
        # )
        ax[1].set_xlabel("Drift in Longitude ($\degree$)", fontsize=14)
        #     ax[1].set_ylabel('Altitude')
        ax[1].spines["right"].set_visible(False)
        ax[1].spines["top"].set_visible(False)
        ax[1].spines["left"].set_visible(False)

    save_filepath = (
        f"{flight_dir.quickplot_path()}HALO-AC3_HALO_Dropsondes_drift-in-lat-lon_{flight_dir.flightdir}.png"
    )

    plt.savefig(save_filepath, dpi=300, bbox_inches="tight")
    logging.info(f"Plot Saved:{save_filepath}")


def all_quicklook_plots(ds_flight, flight_dir):

    launch_locations_map(ds_flight, flight_dir)
    lat_time_plot(ds_flight, flight_dir)
    profiles(ds_flight, flight_dir)
    drift_plots(ds_flight, flight_dir)
