# %% Imports
import numpy as np
import pandas as pd 

import matplotlib.pyplot as plt

# %% Define plot options and color palettes
plt.style.use("src/style.mplstyle")

colors = plt.cm.get_cmap("Set3", 3)
colors = [colors.colors[i,:] for i in range(3)]
binary_cmap = plt.cm.get_cmap("bwr_r", 2)

# %% Load final dataframe
data = pd.read_csv(
    "data/processed/hydrological_spectral_mean_data.csv",
    parse_dates=[1],
    index_col=0
)

# %% Define constants
save_path = "appendix/gaps/{}.svg"

lagoons = data.Lagoon.unique()
years = np.arange(data.Time.min().year, data.Time.max().year+1)
months = np.arange(data.Time.min().month, data.Time.max().month+1)

# %% Plot available image per month
fig, axs = plt.subplots(
    figsize=(4, 5), nrows=3, ncols=1, sharex=True, sharey=True
)

# Find pixel percentage per lagoon
for i, (ax, lagoon) in enumerate(zip(axs, lagoons)):
    percentage = data.PixelPercentage[data.Lagoon == lagoon].copy().values
    
    # Based on pixel percentage determines which months have valid and which haven't
    valids = np.ones_like(percentage)
    valids[percentage < 10] = 0

    # Reshape valids to plot like like an image
    valids = valids.reshape([years.shape[0], months.shape[0]]).T

    im = ax.pcolormesh(years, months, valids, cmap=binary_cmap, edgecolors="w")
    ax.set_title(lagoon.capitalize())

    # Add colorbar
    if i == 1:
        ax.set_ylabel("Months")

        # Create append axes
        cax = ax.inset_axes([1.05, 0.05, 0.05, 0.9])

        # Create colorbar
        bar = plt.colorbar(im, cax=cax, label="Availabel images")
        bar.set_ticks([0.25, 0.75], labels=["No data", "Data"])
        bar.minorticks_off()

    if i == 2:
        ax.set_xlabel("Years")

ax.set_yticks(np.arange(4, 13, 4))
ax.set_xticks(np.arange(2001, 2022, 5))
ax.invert_yaxis()

plt.savefig(save_path.format("images_available_per_month"))

# %% Plot histogram of frequency of pixel percentage
fig, axs = plt.subplots(
    figsize=(6, 3), nrows=1, ncols=3, sharex=True, sharey=True
)

# Find pixel percentage per lagoon
for i, (ax, lagoon, color) in enumerate(zip(axs, lagoons, colors)):
    percentage = data.PixelPercentage[data.Lagoon == lagoon].copy().values

    # Define weight to get relative freq.
    weights = np.ones_like(percentage)/percentage.shape[0]

    # Plot histogram
    ax.hist(percentage, weights=weights, color=color, bins=np.linspace(0, 100, 51))
    ax.set_title(lagoon.capitalize())

    if i == 0:
        ax.set_ylabel("Relative frequency")

    if i == 1:
        ax.set_xlabel("Percentage of valid pixels")

ax.set_xticks(np.linspace(0, 100, 6))

plt.savefig(save_path.format("pixel_percentage_distribution"))

# %% Report the percentage of available data
report = "{}: has {:0.2f} of total ({:0.0f} from {:0.0f})"

# Find pixel percentage per lagoon
for lagoon in lagoons:
    percentage = data.PixelPercentage[data.Lagoon == lagoon].copy().values

    # Based on pixel percentage determines which months have valid and which haven't
    valids = np.ones_like(percentage)
    valids[percentage < 10] = 0

    # Calculate de sum to get the number of good images
    ti = valids.shape[0]
    gi = valids.sum()
    gp = gi/ti * 100

    print(report.format(lagoon, gp, gi, ti))