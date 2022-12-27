# %% Imports
import numpy as np 
import pandas as pd

from functions.stat_utils import plot_corr_matrix

# %% Imports for plots and define some parameters
import matplotlib.pyplot as plt

# Load custom style
plt.style.use("src/style.mplstyle")

# Keys to iterate
lagoons = ["mallorquin", "totumo", "virgen"]
variables = ["Precipitation", "Discharge", "Temperature", "NDVI"]
save_keys = ["original", "rolled", "interpolated_removed"]

# %% Define paths
data_path = "data/processed/detrended_hydrological_spectral_mean_data.csv"
save_path = "data/processed/lm_data_{}_interpolations.csv"

save_images_path = "images/{}_corr_matrix_{}.{}"

# %% Read data
DATA = pd.read_csv(data_path, parse_dates=[1], index_col=0)

# %% Roll variables based on CCFs plots
# List to save the dataframes
DAT2 = []

# Shift to roll data, based on CCF
shift_p = 2
shift_q = 1

# Iterate throught lagoons to subset data
for lagoon in lagoons: 
    # Subset by lagoon
    subset = DATA[DATA.Lagoon == lagoon].copy()
    # Roll Precipitation and discharge
    subset.Precipitation = np.roll(subset.Precipitation, shift_p)
    subset.Discharge = np.roll(subset.Discharge, shift_q)

    # Remove the last columns due to their values don't have sense
    subset = subset.iloc[shift_p:]

    # Store the subsets dataframes
    DAT2.append(subset)

# Merge all dataframes
DAT2 = pd.concat(DAT2)

# %% New dataframes removing interpolated data
# Copy the rolled data
DAT3 = DAT2.copy()

# Mask to get the values that Pixel Percentage is greater than 10%
mask = DAT3.PixelPercentage >= 10.0

# Remove values that don't accomplish the condition
DAT3 = DAT3[mask]

# %% Compare the size of all dataframes
print("original", DATA.shape)
print("rolled", DAT2.shape)
print("Interpolated removed", DAT3.shape)

# %% Correlation plot
# List to store all figures
figs = []

# Iterate over the dataframes to plot the correlation matrix
for data in [DATA, DAT2, DAT3]:
    # Subset data for plot
    subset = data[data.Lagoon == "mallorquin"].copy()
    
    # Plot corr matrix
    fig = plot_corr_matrix(
        data=subset,
        variables=variables,
        half=True,
        hide_insignificants=False,
        show_labels=True,
        show_colorbar=False,
    )

    # Store the figs
    figs.append(fig)

# %% Show figure
# plt.show()

# %% Save figures
for i, (fig, key) in enumerate(zip(figs, save_keys)):
    fig.savefig(save_images_path.format(i+10, key, "svg"))

# %% Save dataframes
for key, data in zip(["with", "without"], [DAT2, DAT3]):
    data.to_csv(save_path.format(key))