# Working with quickdrop

1. Clone this repository to run your script (with the instructions below)

2. The data should be stored in the following structure

- Main data directory
  - YYYYMMDD
    - Level_0 : contains all raw files from the flight
    - Level_1 : contains ASPEN-processed files (keep only QC files, not _PQC)


3. Run the script as below:

```
python quickdrop.py /Absolute/path/to/your/main/data/directory/ YYYYMMDD
```
Note the space between the directory path and YYYYMMDD - these are two different arguments.


An example (when running this on a Mac would be):

```
python quickdrop.py /Users/geet/Documents/AC3/Dropsondes/Data/ 20220225
```

If you only want the gridded file, add the `-g` command at the end

```
python quickdrop.py /Absolute/path/to/your/main/data/directory/ YYYYMMDD -g
```

Or if you already have the gridded file and only want the quicklook plots, then add `-p` at the end

```
python quickdrop.py /Absolute/path/to/your/main/data/directory/ YYYYMMDD -p
```
:warning: Adding both `-g` and `-p` will not work. For gridding and plotting, just execute without the optional commands.

4. After the script is run, if everything has run well, you should find:

(a) a NC file in the `/Absolute/path/to/your/main/data/directory/YYYYMMDD` which includes all sondes from the flight in a uniform, vertical grid (default is 10 m vertical spacing up to 14 km altitude)

(b) Following quicklooks in the `/Absolute/path/to/your/main/data/directory/YYYYMMDD/Quickplots`:

- A map of launch locations colored by IWV
- A spatio-temporal plot of launch-latitude v/s launch-time, also colored by IWV
- Mean profiles of temperature, potential temperature, relative humidity and wind speed (with individual sonde profiles lightly plotted)
- Drift profiles in latitude and longitude

If there are any questions or things don't work for some reason, write up an issue on Github or contact Geet George (geet.george@mpimet.mpg.de)
