# %% Imports
import numpy as np
import pandas as pd 

from statsmodels.tsa.stattools import acf, ccf
from functions.stat_utils import plot_acf_ccf

# %% Imports for plots and define some paremeters
import matplotlib.pyplot as plt

# Load custom style
plt.style.use("src/style.mplstyle")

# Define the titles of the variables
titles = {
    "Precipitation": "Total Precipitation [mm]",
    "Discharge": "Mean Discharge [m3 s-1]",
    "NDVI": "Mean NDVI",
    "Temperature": "Mean Temperature [°C]"
}

# Lagoons to subset data
lagoons = ["mallorquin", "totumo", "virgen"]

# %% Define paths
data_path = "data/processed/detrended_hydrological_spectral_mean_data.csv"
save_images_path = "images/{}_{}_{}cf_plot.{}"
save_images_path = "images/{}_{}_{}cf_plot.{}"

# %% Load data
DATA = pd.read_csv(data_path, parse_dates=[1], index_col=0)

# %% Lists and dictionary to store date
acf_figs = []                               # To save the acf plots
ccf_figs = []                               # To save the ccf plots
ccfs = {}                                   # To save the CCF data

# %% Plot the ACF and CCF of all variables by lagoon
# For loop to plot and calculate ACF and CCF by lagoon
for lagoon in lagoons:
    # Subset data based on lagoon
    subset = DATA[DATA.Lagoon == lagoon].copy()
    
    # Calculate some parameters for the plots
    N = subset.shape[0]
    nlags = 24
    confi = 1.96/np.sqrt(N)

    # Get the variables names
    all_vars = subset.columns[2:-3]

    # If lagoon is Totumo and La Virgen we have to remove discharge from
    # the variables
    if lagoon in ("totumo", "virgen"):
        # Slice to remove discharge
        all_vars = all_vars[[0, 2, 3]]
        
        i_vars = all_vars[[0, 2]]           # Get independant variables
        d_vars = all_vars[[1]]              # Get dependant variables 
    
    else:
        i_vars = all_vars[[0, 1, 3]]        # Get independant variables
        d_vars = all_vars[[2]]              # Get dependant variables 

    # Dictionary to save ACF data by variable
    acf_data = {
        var: acf(subset[var], nlags=nlags) \
        for var in all_vars
    }

    # Dictionary to save CCF data by variable
    ccf_data = {
        f"{d} ~ {i}": ccf(subset[d], subset[i])[:nlags+1] \
        for d in d_vars for i in i_vars
    }
    
    # Also save the CCF data in another dictionary
    ccfs[lagoon] = ccf_data

    # Save the plots in their respective list
    acf_figs.append(plot_acf_ccf(acf_data, confi, [-1.2, 1.2], titles))
    ccf_figs.append(plot_acf_ccf(ccf_data, confi, [-0.7, 0.7]))
    
# %% Show figures
# plt.show()

# %% Save figures
i = 4
for lagoon, afig, cfig in zip(lagoons, acf_figs, ccf_figs):
    afig.savefig(save_images_path.format(i, lagoon, "a", "svg"))
    cfig.savefig(save_images_path.format(i+1, lagoon, "c", "svg"))
    i += 2

# %% Show where is the maximum correlation by lagoon
for lagoon in lagoons:
    data = ccfs[lagoon]
    keys = [t for t in data.keys()]

    for k in keys:
        x = data[k]
        m = np.max(np.abs(x))
        p = np.where(np.abs(x) == m)[0][0]

        print(f"{lagoon.capitalize()}: {k} maximum correlation in lag={p} {m:0.3f}")