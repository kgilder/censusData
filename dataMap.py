import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load the US counties shapefile from an online source or local file
url = "https://www2.census.gov/geo/tiger/TIGER2022/COUNTY/tl_2022_us_county.zip"
counties = gpd.read_file(url)

# Plot the counties
fig, ax = plt.subplots(figsize=(12, 8))
counties.plot(ax=ax, edgecolor="black", facecolor="lightgray", linewidth=0.5)

# Title and axis off
ax.set_title("Map of All US Counties", fontsize=14)
ax.axis("off")

plt.show()

# Select counties for a specific state (e.g., Texas FIPS code = '48')
# state_fips = ['48', '06']  # Texas (48) and California (06)
state_fips = ['48']  # List of FIPS codes for desired states
counties_filtered = counties[counties['STATEFP'].isin(state_fips)]

# Plot counties for selected state(s)
fig, ax = plt.subplots(figsize=(8, 6))
counties_filtered.plot(ax=ax, edgecolor="black", facecolor="lightgray", linewidth=0.5)

ax.set_title("Counties in Texas", fontsize=14)
ax.axis("off")

plt.show()

# Load the MSAs shapefile
msa_url = "https://www2.census.gov/geo/tiger/TIGER2022/METRO/tl_2022_us_cbsa.zip"
msas = gpd.read_file(msa_url)

# Plot MSAs
fig, ax = plt.subplots(figsize=(12, 8))
msas.plot(ax=ax, edgecolor="black", facecolor="lightblue", linewidth=0.5)

ax.set_title("Metropolitan Statistical Areas (MSAs)", fontsize=14)
ax.axis("off")

plt.show()


msa_name = "Dallas-Fort Worth-Arlington, TX"
msa_filtered = msas[msas['NAME'] == msa_name]

fig, ax = plt.subplots(figsize=(8, 6))
msa_filtered.plot(ax=ax, edgecolor="black", facecolor="lightblue", linewidth=0.5)

ax.set_title(f"MSA: {msa_name}", fontsize=14)
ax.axis("off")

plt.show()


# Load US counties shapefile
url = "https://www2.census.gov/geo/tiger/TIGER2022/COUNTY/tl_2022_us_county.zip"
counties = gpd.read_file(url)

# Filter for Texas (FIPS = '48')
texas_counties = counties[counties['STATEFP'] == '48']

# Generate synthetic population data (Replace this with real census data)
np.random.seed(42)
texas_counties["POPULATION"] = np.random.randint(10000, 500000, size=len(texas_counties))

# Plot Texas counties shaded by population
fig, ax = plt.subplots(figsize=(10, 8))
texas_counties.plot(column="POPULATION", cmap="OrRd", linewidth=0.5, edgecolor="black",
                    legend=True, legend_kwds={"label": "Population", "orientation": "horizontal"}, ax=ax)

ax.set_title("Texas Counties Shaded by Population", fontsize=14)
ax.axis("off")

plt.show()
