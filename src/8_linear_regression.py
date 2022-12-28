# %% Imports
import pandas as pd
import statsmodels.formula.api as smf

# %% Imports for plots and define some paremeters
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Load custom style
plt.style.use("src/style.mplstyle")

# Colormap for plots
d_cmap = plt.cm.get_cmap("Set3", 3)
colors = [d_cmap.colors[i,:] for i in range(3)]

# Lagoons to subset the data
lagoons = ["mallorquin", "totumo", "virgen"]

# Define the titles of the variables
titles = {
    "Precipitation": "Total Precipitation [mm]",
    "Discharge": "Mean Discharge [m3 s-1]",
    "NDVI": "Mean NDVI",
    "Temperature": "Mean Temperature [°C]",
    "SOI": "Southern Oscillation Index (SOI)"
}

# Variables for Mallorquin model
variables = ["Precipitation", "Discharge", "Temperature", "SOI"]

# %% Define paths
data_path = "data/processed/lm_data_without_interpolations.csv"
save_images_path = "images/{}_linear_model_scatterplots.{}"
save_models_path = "models/{}_model.{}"

# %% load data 
DATA = pd.read_csv(data_path, parse_dates=[1], index_col=0)

# %% Explor variables
# Create figure and axes
fig, axs = plt.subplots(figsize=(6, 6), nrows=2, ncols=2, sharey=True)

# Index for plot
xx = [0, 1, 0, 1]
yy = [0, 0, 1, 1]

# Iterate throught variables and axes to plot one variable by axes
for ix, iy, variable in zip(xx, yy, variables):
    handles = []                            # Save handles for legend

    # Iterate throught lagoons and color to plot data by lagoon
    for lagoon, color in zip(lagoons, colors):

        # If there is data in the variable, plot it
        try:
            l = axs[iy,ix].scatter(
                DATA[variable][DATA.Lagoon == lagoon],
                DATA["NDVI"][DATA.Lagoon == lagoon],
                label=lagoon.capitalize(),
                color=color,
                alpha=0.5
            )

        except:
            continue

        else:
            handles.append(l)               # Save handle

            # Add x-label
            axs[iy,ix].set_xlabel(titles[variable])
    
    # If the axes is in the first column add the y-label
    if ix == 0:
        axs[iy,ix].set_ylabel(titles["NDVI"])

# Add the legend to one axes
axs[0,1].legend(handles=handles, title="Forest")

# Show correlation between NDVI and the independant variables
# plt.show()

# Save plot
fig.savefig(save_images_path.format(13, "svg"))

# %% Exploratory model
# Formula with all variables and possible interactions
f = "NDVI ~ Lagoon*Precipitation + Lagoon*Temperature \
     + Lagoon*SOI + Precipitation:Temperature + Precipitation:SOI \
     + Temperature:SOI"

# Run model
exploratory_model = smf.ols(f, DATA).fit()

# Show results
print("\nExploratory model:", exploratory_model.summary(), sep="\n")

# The exploratory model show that only precipitation, temperature and the 
# interaction of precipitation with SOI has an effect on NDVI

# %% General model
# General formula
f = "NDVI ~ Precipitation + Temperature + Precipitation:SOI"

# Run model
general_model = smf.ols(f, DATA).fit()

# Show results
print("\nGeneral model:", general_model.summary(), sep="\n")

# %% Mallorquin model
# Due to in mallorquin we have Discharge we can create another model that
# include it

# Subset data
mallorquin = DATA[DATA.Lagoon == "mallorquin"].copy()

# Formula
f = "NDVI ~ Precipitation + Discharge + Temperature + Precipitation:Discharge"

# Run model
mallorquin_model = smf.ols(f, mallorquin).fit()

# Show results
print("\nMallorquín model:", mallorquin_model.summary(), sep="\n")

# %% Save models
models = [exploratory_model, general_model, mallorquin_model]
names = ["exploratory", "general", "mallorquin"]

for name, model in zip(names, models):
    model.save(save_models_path.format(name, "pkl"))

    with open(save_models_path.format(name, "txt"), "w") as tf:
        tf.write(model.summary().as_text())