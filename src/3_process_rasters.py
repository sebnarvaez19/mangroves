# %% Imports
import os 
import numpy as np

import xarray
import rioxarray
import rasterio

# %% Define the paths to get and save the images
path = "data/raster/{}/"
save_path = "data/processed/{}_{}"

# %% Define the keys to get the images
lagoons = ["mallorquin", "totumo", "virgen"]

# %% For loop throught the keys to get the images
for lagoon in lagoons:
    path_images = path.format(lagoon)       # Define the path of the images
    images = os.listdir(path_images)        # Search all images in the earlier defined path

    # For loop throught the images
    for image in images:
        path_image = path_images + image    # Define the image path

        # Open the image with rasterio
        with rasterio.open(path_image, "r") as src:
            # Get the limits of the images to define the coordinates
            lims = src.bounds

            # If the images if the first of all, define a new array with
            # the Surface temperature and another with the NDVI
            if image == images[0]:
                temp = src.read(5)
                ndvi = src.read(6)

            # Else, concat the new array to the previously created
            else:
                temp = np.dstack([temp, src.read(5)])
                ndvi = np.dstack([ndvi, src.read(6)])

    # With the date in the path of the image define the time dimension
    t = np.array([ti[:-4] for ti in images], dtype="datetime64")
    
    # With the boinds of the imiages define the longitude and the 
    # latitude dimensions
    x = np.linspace(lims[0], lims[2], ndvi.shape[1])
    y = np.flip(np.linspace(lims[1], lims[3], ndvi.shape[0]))

    # Scale all temperature from Kelvin to Celsius
    temp -= 273.15

    # Mask NDVI data using the value chosen to nan (-300000) and all
    # outliers from NDVI
    ndvi_mask = ((ndvi == -3e5) | (ndvi > 1.5) | (ndvi < -1.5))
    
    # Mask temperature based on hide al temperature lowers than 10°C
    temp_mask = (temp < 10.0)

    ndvi[ndvi_mask] = np.nan
    temp[temp_mask] = np.nan

    # Create NDVI DataArray
    ndvi = xarray.DataArray(
        data=ndvi,
        dims=("latitude", "longitude", "time"),
        coords={"longitude": x, "latitude": y, "time": t},
        name="NDVI",
    )

    # Create Surface Temperature DataArray
    temp = xarray.DataArray(
        data=temp,
        dims=("latitude", "longitude", "time"),
        coords={"longitude": x, "latitude": y, "time": t},
        name="Surface Temperature",
    )

    # Merge NDVI and Temperature DataArrays to save on one Dataset
    data = xarray.merge([ndvi, temp])

    # Transpose and define the CRS and the spatial dims to save it
    data = data.transpose("time", "latitude", "longitude")
    data = data.rio.write_crs("EPSG:4326")
    data = data.rio.set_spatial_dims(x_dim="longitude", y_dim="latitude")

    # Define some attributes
    data.attrs["description"] = "NDVI and Surface Temperature extracted from LANDSAT SR images from 1996 to 2021"
    data.attrs["Surface Temperature units"] = "°C"

    # Save data as a NetCDF file
    data.to_netcdf(save_path.format(lagoon, "ndvi_temperature.nc"))
