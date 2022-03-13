import xarray as xr
import numpy as np
import glob
import logging

from tqdm import tqdm
from tqdm import trange

from metpy.future import precipitable_water
import metpy.calc as mpcalc
from metpy.units import units


def grid_together(flight_dir, max_alt=14000, vertical_spacing=10):

    l1_dir = flight_dir.l1dir

    allfiles = sorted(glob.glob(l1_dir + "*QC.nc"))

    ori_list = [None] * len(allfiles)

    check_vars = ["alt", "pres", "u_wind", "v_wind", "lat", "lon", "mr"]

    g = 0
    for i in tqdm(allfiles):

        sonde = i.replace(f"{l1_dir}", "").replace("QC.nc", "")

        check_vars = ["pres", "u_wind", "v_wind", "lat", "lon", "mr"]
        ds = xr.open_dataset(i)
        sum_list = np.array([ds[var].sum().values for var in check_vars])

        if len(np.where(sum_list == 0)[0]) != 0:

            print_msg = f"For sonde {sonde}, variable/s {check_vars[np.where(sum_list==0)[0][0]]} found to have zero sum. Ignoring this sonde now for quicklooks purposes. Check later during final QC."

            logging.info(print_msg)
            print(print_msg)

        else:

            ori_list[g] = (
                xr.open_dataset(i)
                .drop("alt")
                .dropna(dim="time", subset=["time"])
                .isel(obs=0)
                .swap_dims({"time": "gpsalt"})
                .reset_coords()
                .dropna(
                    dim="gpsalt",
                    subset=["pres", "u_wind", "v_wind", "lat", "lon", "mr"],
                    how="any",
                )
                .rename({"gpsalt": "alt"})
                .interp(alt=np.arange(0, max_alt + vertical_spacing, vertical_spacing))
            )

        g = g + 1

    ds_list = list(filter(None, ori_list))
    ds_flight = xr.concat(ds_list, dim="launch_time")

    logging.info(
        f"Gridded all individual sondes for {l1_dir} at {vertical_spacing} m vertical resolution to {max_alt} m"
    )

    return ds_flight


def derived_products(ds_flight):

    ds_flight["T"] = ds_flight["tdry"] + 273.15

    ds_flight["q"] = (
        ["launch_time", "alt"],
        mpcalc.specific_humidity_from_mixing_ratio(ds_flight["mr"]).magnitude,
    )

    iwv = [None] * len(ds_flight["launch_time"])

    for i in range(len(ds_flight["launch_time"])):

        iwv[i] = precipitable_water(
            ds_flight["pres"].isel(launch_time=i).values * units.mbar,
            ds_flight["dp"].isel(launch_time=i).values * units.degC,
        ).magnitude

    ds_flight["iwv"] = (["launch_time"], iwv)

    logging.info(f"Added derived variables: T, q and iwv to ds_flight")

    return ds_flight


def save_ds(ds_flight, flight_dir):
    save_filepath = f"{flight_dir.dir}HALO-AC3_HALO_Dropsondes_quickgrid_{flight_dir.flightdir}.nc"
    ds_flight.to_netcdf(save_filepath)

    logging.info(f"File Saved:{save_filepath}")
