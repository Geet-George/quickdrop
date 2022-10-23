import xarray as xr
import numpy as np

from pathlib import Path as pp
import logging
import os.path
import os
import helper
import plots
import quickgrid
import argparse
import sys
import logging.config

FORMAT = (
    "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
)

filename="logs/paths.log"
os.makedirs(os.path.dirname(filename), exist_ok=True)

logging.basicConfig(filename=filename, level=logging.INFO, format=FORMAT)
logging.info(f"{os.path.basename(__file__)} run as {__name__} ...")

logging.config.dictConfig({
    'version': 1,
    # Other configs ...
    'disable_existing_loggers': True
})

parser = argparse.ArgumentParser(
    description="This script will process Level-1 files from ASPEN, provide a gridded file for the whole flight, and generate some quicklooks."
)

parser.add_argument(
    "main_dir",
    type=str,
    help="directory where all data are stored; parent directory of folder with YYYYMMDD format",
)
parser.add_argument(
    "flightdate",
    type=int,
    help="the flight date in YYYYMMD",
)

parser.add_argument("-p", "--plot", action="store_true",
                    help="only create plots from the available gridded file")

parser.add_argument("-g", "--grid", action="store_true",
                    help="only create gridded file from individual sondes (no plots)")

args = parser.parse_args()

logging.info(sys.argv)


# logging.info(
#     f"Arguments provided: main_dir: {args.main_dir}; flightdate: {args.flightdate}"
# )

flight_dir = helper.Paths(args.main_dir, str(args.flightdate))

if args.grid and args.plot :

    print("Both 'grid' and 'plot' option provided as True. Either remove both options and the script will run both. Otherwise, provide just one option.")

elif args.grid :

    ds_flight = quickgrid.grid_together(flight_dir)
    ds_flight = quickgrid.derived_products(ds_flight)
    quickgrid.save_ds(ds_flight, flight_dir)

elif args.plot :

    ds_flight = xr.open_dataset(flight_dir.quickgrid_nc_path())

    plots.all_quicklook_plots(ds_flight, flight_dir)

else :

    ds_flight = quickgrid.grid_together(flight_dir)
    ds_flight = quickgrid.derived_products(ds_flight)
    quickgrid.save_ds(ds_flight, flight_dir)

    ds_flight = xr.open_dataset(flight_dir.quickgrid_nc_path())

    plots.all_quicklook_plots(ds_flight, flight_dir)

logging.info(f'################## Run completed successfully for {flight_dir.flightdir} ##################')
