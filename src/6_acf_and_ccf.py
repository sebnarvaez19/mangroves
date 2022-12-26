# %% Imports
import numpy as np
import pandas as pd 

from statsmodels.tsa.stattools import acf, ccf

# %% Imports for plots and define some paremeters
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MultipleLocator

# Load custom style
plt.style.use("src/style.mplstyle")

# Define the titles of the variables
titles = {
    "Precipitation": "Total Precipitation [mm]",
    "Discharge": "Mean Discharge [m3 s-1]",
    "NDVI": "Mean NDVI",
    "Temperature": "Mean Temperature [°C]"
}

t_labs = [c for c in "abc"]
f_labs = [c for c in "abcd"]

# %% Define paths
data_path = "data/processed/detrended_hydrological_spectral_mean_data.csv"
save_images_path_acf = "images/{}_{}_acf_plot.{}"
save_images_path_ccf = "images/{}_{}_ccf_plot.{}"

# %% Load data
DATA = pd.read_csv(data_path, parse_dates=[1], index_col=0)

# Subset data for plots
mallorquin = DATA[DATA.Lagoon == "mallorquin"].copy()
totumo = DATA[DATA.Lagoon == "totumo"].copy().drop("Discharge", axis=1)
virgen = DATA[DATA.Lagoon == "virgen"].copy().drop("Discharge", axis=1)

# %% Set the confidence interval
N = mallorquin.shape[0]
nlags = 24
conf_interval = 1.96/np.sqrt(N)

# %% Mallorquin
# Get variables
m_vars = mallorquin.columns[2:-3]
h_vars = m_vars[:2]
s_vars = m_vars[2:]

# Calculate autocorrelation
acf_mallorquin = {m_var: acf(mallorquin[m_var], nlags=nlags) for m_var in m_vars}

# Calculate cross correlation
ccf_mallorquin = {
    f"{s_var} ~ {h_var}": ccf(mallorquin[s_var], mallorquin[h_var])[:nlags+1] \
    for h_var in h_vars for s_var in s_vars
}

# Get the correlations titles
tests = [c for c in ccf_mallorquin.keys()]

# Plot autocorrelation
fig, axs = plt.subplots(
    nrows=2, ncols=2, sharex=True, sharey=True
)

# Define the index of the plots
ix = [0, 0, 1, 1]
jy = [0, 1, 0, 1]

# For loop to plot the autocorrelation
for i, j, m_var in zip(ix, jy, m_vars):
    axs[i,j].stem(acf_mallorquin[m_var], markerfmt=" ", basefmt="black")
    axs[i,j].axhline(conf_interval, color="black", linestyle="--")
    axs[i,j].axhline(-conf_interval, color="black", linestyle="--")
    axs[i,j].set_title(titles[m_var], fontsize=8)
    axs[i,j].set_ylim([-1, 1])
    
    # Add ylabel to the axes on first column
    if j == 0:
        axs[i,j].set_ylabel("Correlation")

    # Add xlabel to the axes in last row
    if i == 1:
        axs[i,j].set_xlabel("Lags [months]")
        axs[i,j].xaxis.set_major_locator(MultipleLocator(4))
        axs[i,j].xaxis.set_minor_locator(MultipleLocator(1))

# Show plot
# plt.show()

# Save fig
fig.savefig(save_images_path_acf.format(4, "mallorquin", "svg"))

# Plot cross-correlation
fig, axs = plt.subplots(
    nrows=2, ncols=2, sharex=True, sharey=True
)

# For loop to plot cross-correlaion
for i, j, test in zip(ix, jy, tests):
    axs[i,j].stem(ccf_mallorquin[test], markerfmt=" ", basefmt="black")
    axs[i,j].axhline(conf_interval, color="black", linestyle="--")
    axs[i,j].axhline(-conf_interval, color="black", linestyle="--")
    axs[i,j].set_title(test, fontsize=8)
    axs[i,j].set_ylim([-0.7, 0.7])

    # Add ylabel to the axes on first column
    if j == 0:
        axs[i,j].set_ylabel("Correlation")

    # Add xlabel to the axes in last row
    if i == 1:
        axs[i,j].set_xlabel("Lags [months]")
        axs[i,j].xaxis.set_major_locator(MultipleLocator(4))
        axs[i,j].xaxis.set_minor_locator(MultipleLocator(1))

# Show plot
# plt.show()

# Save fig
fig.savefig(save_images_path_ccf.format(5, "mallorquin", "svg"))

# %% Totumo and La Virgen
# Because both dataframes has the same variables, the same coe is used to
# plot them
lagoons = ["totumo", "virgen"]
datasets = {"totumo": totumo, "virgen": virgen}

# Get variables
t_vars = totumo.columns[2:-3]
h_vars = t_vars[:1]
s_vars = t_vars[1:]

# Define the index of figure to save
fig_index = 6

# For loop throught lagoons to subset data
for lagoon in lagoons:
    dataset = datasets[lagoon]
    # Calculate autocorrelation
    acf_data = {t_var: acf(dataset[t_var], nlags=nlags) for t_var in t_vars}

    # Calculate cross correlation
    ccf_data = {
        f"{s_var} ~ {h_var}": ccf(dataset[s_var], dataset[h_var])[:nlags+1] \
        for h_var in h_vars for s_var in s_vars
    }

    # Get the correlations titles
    tests = [c for c in ccf_data.keys()]

    # Plot autocorrelation
    fig = plt.figure()
    grs = GridSpec(2, 2)

    # Create axes
    axs = [
        fig.add_subplot(grs[0,0]),
        fig.add_subplot(grs[1,:]),
        fig.add_subplot(grs[0,1]),
    ]

    # Share x and y axis of all axes
    axs[0].get_shared_x_axes().join(*axs)
    axs[0].get_shared_y_axes().join(*axs)

    # For loop plot autocorrelation data
    for i, (t_var, ax) in enumerate(zip(t_vars, axs)):
        ax.stem(acf_data[t_var], markerfmt=" ", basefmt="black")
        ax.axhline(conf_interval, color="black", linestyle="--")
        ax.axhline(-conf_interval, color="black", linestyle="--")
        ax.set_title(titles[t_var], fontsize=8)
        ax.set_ylim([-1, 1])

        ax.xaxis.set_major_locator(MultipleLocator(4))
        ax.xaxis.set_minor_locator(MultipleLocator(1))

        # Add ylabel to the axes on first column
        if i < 2:
            ax.set_ylabel("Correlation")

        # Add xlabel to the axes in last row
        if i == 1:
            ax.set_xlabel("Lags [months]")

    # Show plot
    # plt.show()

    # Save fig
    fig.savefig(save_images_path_acf.format(fig_index, lagoon, "svg"))

    # Plot cross-correlation
    fig, axs = plt.subplots(
        nrows=2, ncols=1, sharex=True, sharey=True
    )

    # For loop to plot cross-correlation data
    for i, (test, ax) in enumerate(zip(tests, axs)):
        ax.stem(ccf_data[test], markerfmt=" ", basefmt="black")
        ax.axhline(conf_interval, color="black", linestyle="--")
        ax.axhline(-conf_interval, color="black", linestyle="--")
        ax.set_title(test, fontsize=8)
        ax.set_ylim([-0.7, 0.7])

        ax.set_ylabel("Correlation")

        if i == 1:
            ax.set_xlabel("Time [Y]")
            ax.xaxis.set_major_locator(MultipleLocator(4))
            ax.xaxis.set_minor_locator(MultipleLocator(1))

    # Show plot
    # plt.show()

    # Save fig
    fig.savefig(save_images_path_ccf.format(fig_index+1, lagoon, "svg"))

    fig_index += 2