# %% Imports
import numpy as np
import pandas as pd

from statsmodels.tsa.seasonal import seasonal_decompose

# %% Imports for plots and define some paremeters
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator

# Load custom style
plt.style.use("src/style.mplstyle")

# Define the titles of the variables
titles = {
    "Precipitation": "Total Precipitation [mm]",
    "Discharge": "Mean Discharge [m3 s-1]",
    "NDVI": "Mean NDVI",
    "Temperature": "Mean Temperature [°C]"
}

# Scale for limits of ENSO stripes
scale = 0.05

# %% Define constants
data_path = "data/processed/hydrological_spectral_mean_data.csv"
save_path = "data/processed/detrended_hydrological_spectral_mean_data.csv"
save_images_path = "images/{}_{}_time_series_components.{}"

lagoons = ["mallorquin", "totumo", "virgen"]

# %% Load data
DATA = pd.read_csv(data_path, parse_dates=[1], index_col=0)

# %% Decompose variables by lagoon
decomposed = {}

# For loop to iterate throught lagoon
for lagoon in lagoons:
    # Subset data by lagoon and define the time as the index
    subset = DATA[DATA.Lagoon == lagoon].copy().set_index("Time", drop=True)
    subset.index.name = None
    
    # Dictionary to save the decomposed components dataframes
    decomposed_data = {}

    # For loop to iterate throught the dataframes variables
    for variable in subset.columns[1:-3]:
        # Try to decompose the variables to handle the error of the 
        # dataframe variables with NaN
        try:
            components = seasonal_decompose(subset[variable], extrapolate_trend="freq")

        except:
            continue

        # Save the decomposed data as a datafarme
        decomposed_data[variable] = pd.DataFrame({
            "Observed": components.observed,
            "Trend": components.trend,
            "Detrended": components.observed - components.trend,
            "Seasonal": components.seasonal,
            "Anomalies": components.resid
        })

    # Save the dataframes by lagoon
    decomposed[lagoon] = decomposed_data

# %% Plot the TSs components
# Get the enso phases for the stripes
enso_phase = DATA.ENSO[DATA.Lagoon == "mallorquin"].values

# Dictionary to save the figs
figs = {}

# For loop to iterate thorught lagoons to plot de decomposed TSs
for lagoon in lagoons:
    # Get the variables
    variables = decomposed[lagoon].keys()
    
    # Mallorquín has one more varible than Totumo and La Virgen so it need
    # a bigger figure
    if lagoon == "mallorquin":
        fig, axs = plt.subplots(
            figsize=(9, 4), nrows=5, ncols=len(variables), sharex=True
        )
    
    else:
        fig, axs = plt.subplots(
            figsize=(7, 4), nrows=5, ncols=len(variables), sharex=True
        )

    # For loop to iterate throught the variables to plot them one by one
    for i, variable in enumerate(variables):
        # Get the components
        components = decomposed[lagoon][variable].columns

        # For loop to iterrate throught the components
        for j, component in enumerate(components):
            # Get the time and the component data
            x = decomposed[lagoon][variable].index
            y = decomposed[lagoon][variable][component]
            
            # Plot La Niña ENSO Phase stripes
            axs[j,i].fill_between(
                x,
                np.min(y) - scale*np.max(y),
                np.max(y) + scale*np.max(y),
                where=enso_phase == "Nina",
                color="blue",
                alpha=0.2
            )

            # Plot El Niño ENSO Phase stripes
            axs[j,i].fill_between(
                x,
                np.min(y) - scale*np.max(y),
                np.max(y) + scale*np.max(y),
                where=enso_phase == "Nino",
                color="red",
                alpha=0.2
            )

            # Plot data
            axs[j,i].plot(x, y, color="black", lw=0.5)
            
            # In the first row add the variable title
            if j == 0:
                axs[j,i].set_title(titles[variable], fontsize=8)

            # In the first column add the component in the label
            if i == 0:
                axs[j,i].set_ylabel(component)

            # In the last row add the time label
            if j == 4:
                axs[j,i].set_xlabel("Time [Y]")

    
    # Set the x-ticks to multiples of 5 years and the minor ticks to 1 year
    axs[j,i].xaxis.set_major_locator(YearLocator(5))    
    axs[j,i].xaxis.set_minor_locator(YearLocator(1))

    # Align all the y-labels in the first column
    fig.align_ylabels(axs[:,0])

    # Save the figure in the dictionary
    figs[lagoon] = fig


# %% Show figures
plt.show()

# %% Save figures
for i, (lagoon, figure) in enumerate(figs.items()):
    figure.savefig(save_images_path.format(i+1, lagoon, "svg"))
    figure.savefig(save_images_path.format(i+1, lagoon, "png"))

# %% Save detrended data
# List to save the detrended dataframes
DATD = []

# For loop to iterate throught decomposes data to get the detrended
# component of the variable
for lagoon in lagoons:
    # Get the variables
    variables = decomposed[lagoon].keys()
    
    # Create the dataframe with the dentreded components of all variables 
    df = {variable: decomposed[lagoon][variable].Detrended for variable in variables}
    df = pd.DataFrame(df)

    # Restore time column
    df.index.name = "Time"
    df = df.reset_index()
    
    # Define lagoon column
    df["Lagoon"] = lagoon

    # Add the dataframe to the final list
    DATD.append(df)

# Merge all dataframes
DATD = pd.concat(DATD, ignore_index=True)

# Load the unused columns from original data
DATD["PixelPercentage"] = DATA.PixelPercentage
DATD["SOI"] = DATA.SOI
DATD["ENSO"] = DATA.ENSO

# Sort the columns in the same way as the original data
DATD = DATD[DATA.columns]

# Show detrended data
print(DATD)

# Save detrended data
DATD.to_csv(save_path)