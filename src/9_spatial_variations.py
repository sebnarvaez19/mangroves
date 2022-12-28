# %% Imports
import xarray
import rioxarray
import geopandas as gpd

# %% Imports for plots and define some paremeters
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Load custom style
plt.style.use("src/style.mplstyle")

# %% Define paths
data_path = "data/processed/{}_ndvi_temperature.nc"
forests_path = "data/shapefile/mangrove_forests.shp"
save_images_path = "images/{}_{}_{}.{}"

# %% Read data
mallorquin = xarray.open_dataset(data_path.format("mallorquin"), decode_coords="all")
totumo = xarray.open_dataset(data_path.format("totumo"), decode_coords="all")
virgen = xarray.open_dataset(data_path.format("virgen"), decode_coords="all")

forests = gpd.read_file(forests_path)

# %% Get statistics
# Means
m_mean = mallorquin.mean(dim="time")
t_mean = totumo.mean(dim="time")
v_mean = virgen.mean(dim="time")

# Standard deviation
m_std = mallorquin.std(dim="time")
t_std = totumo.std(dim="time")
v_std = virgen.std(dim="time")


# %% Get forests
f_mallorquin = forests[forests.key == "mallorquin"].boundary
f_totumo = forests[forests.key == "totumo"].boundary
f_virgen = forests[forests.key == "virgen"].boundary

# %% Plot mallorquin
# Mean
# Create figure and axes
fig1, (ax1, ax2) = plt.subplots(
    figsize=(5, 4), nrows=2, ncols=1, sharex=True, sharey=True
)

# Add axes for colorbars
cax1 = ax1.inset_axes([1.05, 0.05, 0.03, 0.90])
cax2 = ax2.inset_axes([1.05, 0.05, 0.03, 0.90])

# Plot NDVI
m_mean["NDVI"].plot(
    ax=ax1, cbar_ax=cax1, vmin=0, vmax=1, 
    extend="neither", cmap="RdYlGn"
)

# Plot Temperature
m_mean["Surface Temperature"].plot(
    ax=ax2, cbar_ax=cax2, vmin=28, vmax=42, 
    extend="neither", cmap="Spectral_r"
)

# Hide some labels
ax1.set_title("")
ax2.set_title("")
ax1.set_xlabel("")

# Add the forest
f_mallorquin.plot(ax=ax1, color="black", lw=1)
f_mallorquin.plot(ax=ax2, color="black", lw=1)

# Edit colorbars labels
cax1.set_ylabel("Mean NDVI")
cax2.set_ylabel("Mean Surface Temperature [°C]")

# Align colorbars labels
fig1.align_ylabels([cax1, cax2])

# Set the ticks
ax2.yaxis.set_major_locator(MultipleLocator(0.02))
ax2.yaxis.set_minor_locator(MultipleLocator(0.01))
ax2.xaxis.set_major_locator(MultipleLocator(0.02))
ax2.xaxis.set_minor_locator(MultipleLocator(0.01))

# Standard deviation
# Create figure and axes
fig2, (ax1, ax2) = plt.subplots(
    figsize=(5, 4), nrows=2, ncols=1, sharex=True, sharey=True
)

# Create axes for colorbars
cax1 = ax1.inset_axes([1.05, 0.05, 0.03, 0.90])
cax2 = ax2.inset_axes([1.05, 0.05, 0.03, 0.90])

# Plot NDVI
m_std["NDVI"].plot(
    ax=ax1, cbar_ax=cax1, vmin=0, vmax=0.5, 
    extend="neither", cmap="RdYlGn"
)

# Plot Temperature
m_std["Surface Temperature"].plot(
    ax=ax2, cbar_ax=cax2, vmin=4.0, vmax=8.0, 
    extend="neither", cmap="Spectral_r"
)

# Hide some labels
ax1.set_title("")
ax2.set_title("")
ax1.set_xlabel("")

# Add forest
f_mallorquin.plot(ax=ax1, color="black", lw=1)
f_mallorquin.plot(ax=ax2, color="black", lw=1)

# Edit colorbars labels
cax1.set_ylabel("StD NDVI")
cax2.set_ylabel("StD Surface Temperature [°C]")

# Align colorbars labels
fig2.align_ylabels([cax1, cax2])

# Set ticks
ax2.yaxis.set_major_locator(MultipleLocator(0.02))
ax2.yaxis.set_minor_locator(MultipleLocator(0.01))
ax2.xaxis.set_major_locator(MultipleLocator(0.02))
ax2.xaxis.set_minor_locator(MultipleLocator(0.01))

# %% Plot Totumo
# Mean
# Create figure and axes
fig3, (ax1, ax2) = plt.subplots(
    figsize=(5, 4), nrows=1, ncols=2, sharex=True, sharey=True
)

# Define axes for colorbars
cax1 = ax1.inset_axes([1.05, 0.05, 0.07, 0.90])
cax2 = ax2.inset_axes([1.05, 0.05, 0.07, 0.90])

# Plot NDVI
t_mean["NDVI"].plot(
    ax=ax1, cbar_ax=cax1, vmin=0, vmax=1, 
    extend="neither", cmap="RdYlGn"
)

# Plot Temperature
t_mean["Surface Temperature"].plot(
    ax=ax2, cbar_ax=cax2, vmin=28, vmax=42, 
    extend="neither", cmap="Spectral_r"
)

# Hide some labels
ax1.set_title("")
ax2.set_title("")
ax2.set_ylabel("")

# Add forest
f_totumo.plot(ax=ax1, color="black", lw=1)
f_totumo.plot(ax=ax2, color="black", lw=1)

# Change colorbars labels
cax1.set_ylabel("Mean NDVI")
cax2.set_ylabel("Mean Surface Temperature [°C]")

# Align colorbars labels
fig3.align_ylabels([cax1, cax2])

# Set ticks
ax2.yaxis.set_major_locator(MultipleLocator(0.02))
ax2.yaxis.set_minor_locator(MultipleLocator(0.01))
ax2.xaxis.set_major_locator(MultipleLocator(0.02))
ax2.xaxis.set_minor_locator(MultipleLocator(0.01))

# Standard deviation
# Create figure and axes
fig4, (ax1, ax2) = plt.subplots(
    figsize=(5, 4), nrows=1, ncols=2, sharex=True, sharey=True
)

# Create axes for colorbars
cax1 = ax1.inset_axes([1.05, 0.05, 0.07, 0.90])
cax2 = ax2.inset_axes([1.05, 0.05, 0.07, 0.90])

# Plot NDVI
t_std["NDVI"].plot(
    ax=ax1, cbar_ax=cax1, vmin=0, vmax=0.5, 
    extend="neither", cmap="RdYlGn"
)

# Plot Temperature
t_std["Surface Temperature"].plot(
    ax=ax2, cbar_ax=cax2, vmin=4.0, vmax=8.0, 
    extend="neither", cmap="Spectral_r"
)

# Hide some labels
ax1.set_title("")
ax2.set_title("")
ax2.set_ylabel("")

# Add forest
f_totumo.plot(ax=ax1, color="black", lw=1)
f_totumo.plot(ax=ax2, color="black", lw=1)

# Edit colorbars labels
cax1.set_ylabel("StD NDVI")
cax2.set_ylabel("StD Surface Temperature [°C]")

# Align colorbars labels
fig4.align_ylabels([cax1, cax2])

# Set ticks
ax2.yaxis.set_major_locator(MultipleLocator(0.02))
ax2.yaxis.set_minor_locator(MultipleLocator(0.01))
ax2.xaxis.set_major_locator(MultipleLocator(0.02))
ax2.xaxis.set_minor_locator(MultipleLocator(0.01))

# %% Plot La Virgen
# Mean
# Create figure and axes
fig5, (ax1, ax2) = plt.subplots(
    figsize=(5, 4), nrows=1, ncols=2, sharex=True, sharey=True
)

# Create axes for colorbars
cax1 = ax1.inset_axes([1.05, 0.05, 0.07, 0.90])
cax2 = ax2.inset_axes([1.05, 0.05, 0.07, 0.90])

# Plot NDVI
v_mean["NDVI"].plot(
    ax=ax1, cbar_ax=cax1, vmin=0, vmax=1, 
    extend="neither", cmap="RdYlGn"
)

# Plot Temperature
v_mean["Surface Temperature"].plot(
    ax=ax2, cbar_ax=cax2, vmin=28, vmax=42, 
    extend="neither", cmap="Spectral_r"
)

# Hide some labels
ax1.set_title("")
ax2.set_title("")
ax2.set_ylabel("")

# Add forest
f_virgen.plot(ax=ax1, color="black", lw=1)
f_virgen.plot(ax=ax2, color="black", lw=1)

# Edit colorbars labels
cax1.set_ylabel("Mean NDVI")
cax2.set_ylabel("Mean Surface Temperature [°C]")

# Align colorbars labels
fig5.align_ylabels([cax1, cax2])

# Set ticks
ax2.yaxis.set_major_locator(MultipleLocator(0.02))
ax2.yaxis.set_minor_locator(MultipleLocator(0.01))
ax2.xaxis.set_major_locator(MultipleLocator(0.02))
ax2.xaxis.set_minor_locator(MultipleLocator(0.01))

# Standard deviation
# Create figure and axes
fig6, (ax1, ax2) = plt.subplots(
    figsize=(5, 4), nrows=1, ncols=2, sharex=True, sharey=True
)

# Create axes for colorbars
cax1 = ax1.inset_axes([1.05, 0.05, 0.07, 0.90])
cax2 = ax2.inset_axes([1.05, 0.05, 0.07, 0.90])

# Plot NDVI
v_std["NDVI"].plot(
    ax=ax1, cbar_ax=cax1, vmin=0, vmax=0.5, 
    extend="neither", cmap="RdYlGn"
)

# Plot Temperature
v_std["Surface Temperature"].plot(
    ax=ax2, cbar_ax=cax2, vmin=4.0, vmax=8.0, 
    extend="neither", cmap="Spectral_r"
)

# Hide some labels
ax1.set_title("")
ax2.set_title("")
ax2.set_ylabel("")

# Add forest
f_virgen.plot(ax=ax1, color="black", lw=1)
f_virgen.plot(ax=ax2, color="black", lw=1)

# Edit colorbars labels
cax1.set_ylabel("StD NDVI")
cax2.set_ylabel("StD Surface Temperature [°C]")

# Align colorbars labels
fig6.align_ylabels([cax1, cax2])

# Set ticks
ax2.yaxis.set_major_locator(MultipleLocator(0.02))
ax2.yaxis.set_minor_locator(MultipleLocator(0.01))
ax2.xaxis.set_major_locator(MultipleLocator(0.02))
ax2.xaxis.set_minor_locator(MultipleLocator(0.01))

# %% Show all plots
# plt.show()

# Saves all figures
fig1.savefig(save_images_path.format(14, "mallorquin", "mean", "svg"))
fig2.savefig(save_images_path.format(15, "mallorquin", "std", "svg"))
fig3.savefig(save_images_path.format(16, "totumo", "mean", "svg"))
fig4.savefig(save_images_path.format(17, "totumo", "std", "svg"))
fig5.savefig(save_images_path.format(18, "virgen", "mean", "svg"))
fig6.savefig(save_images_path.format(19, "virgen", "std", "svg"))