import logging
from pathlib import Path as pp
import os.path

class Paths:
    """
    Deriving paths from the provided directory

    Provide as input:
    (a) the main path for all data 
    (b) the directory name for the particular flight 

    It is recommended that (b) be in the format YYYYMMDD of the date that the flight was flown on - in case of the flight covering midnight, the date for take-off should be considered. 
    """
    
    def __init__(self,directory,flightdir):
        self.dir = directory + flightdir + '/'
        self.flightdir = flightdir
        self.l1dir = directory + flightdir + '/Level_1/'

        logging.info(f'Created Path Instance: Main:{directory}; Flight:{flightdir}')

    
    def quickplot_path(self):
        qp_path = f'{self.dir}Quickplots/'
        if pp(qp_path).exists():
            logging.info(f'Path exists: {qp_path}')
        else:    
            pp(qp_path).mkdir(parents=True)
            logging.info(f'Path did not exist. Created directory: {qp_path}')
        return qp_path

    def quickgrid_nc_path(self):
        qg_nc_path = f'{self.dir}HALO-AC3_HALO_Dropsondes_quickgrid_{self.flightdir}.nc'
        if pp(qg_nc_path).is_file():
            logging.info(f'File found: {qg_nc_path}')
            return qg_nc_path 
        else :
            logging.error(f'File Not Found: {qg_nc_path}. Raising exception')
            raise ValueError(f'File Not Found: {qg_nc_path}. Please create the quickgrid file if not already created.')   