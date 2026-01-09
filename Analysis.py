#%%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import geopandas as gpd
import geodatasets
from rapidfuzz import process, fuzz
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl
from matplotlib.colors import LogNorm

def find(df, column, text):
    return df.loc[df[column].str.contains(text, case=False, na=False)]
# %%
file = "WPP2024_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT.xlsx"

df = pd.read_excel(file)
print(df.dtypes)
# %%

df = df.set_axis(df.iloc[15],axis=1)

print(df.dtypes)
#%%
df.drop(axis = 0, index = df.index[:16],inplace = True)

df.reset_index(drop=True)
# %%
df['Type'].unique()
# %%
df_countries = df[df["Type"] == "Country/Area"]
# %%
country_col = "Region, subregion, country or area *"
pop_col = "Total Population, as of 1 July (thousands)"

pop_table = df_countries.pivot(index="Year", columns=country_col, values=pop_col)
# %%
plt.figure(figsize=(12, 6))

for country in pop_table.columns:
    plt.plot(pop_table.index, pop_table[country], alpha=0.3,label=str(country))

plt.xlabel("Year")
plt.ylabel("Population (thousands)")
plt.title("Population of All Countries Over Time")
plt.tight_layout()
plt.legend()
plt.show()
# %%
# %%
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
world = gpd.read_file(url).rename({'ADMIN': 'name'}, axis = "columns")
world.plot(column='name',edgecolor='black')

# %% Create Plot for 2023 Population
year = 2023

pop_year = df_countries[df_countries["Year"] == year][
    [
        "Region, subregion, country or area *",
        "Total Population, as of 1 July (thousands)"
    ]
].copy()

pop_year.columns = ["country", "population"]

#Multiply data by 1e3 to adjust for the scaling in the dataset:
pop_year['population'] = pop_year['population']*1e3

#Manually reasing some of the names which are diffrent between the map and UN data
rename_map = {
    #Scheme: pop_year : world_pop
    "Viet Nam": "Vietnam",
    "Lao People's Democratic Republic": "Laos",
    "Bolivia (Plurinational State of)": "Bolivia",
    "Republic of Moldova": "Moldova",
    "Republic of Korea": "South Korea",
    "Congo": "Republic of the Congo",   # adjust if needed
    "Türkiye": "Turkey",
    "Eswatini": "Eswatini",  # needed if map uses Swaziland
    "Brunei Darussalam" : "Brunei",
    "Timor-Leste" : "East Timor",
    "Iran (Islamic Republic of)" : "Iran",
    "Russian Federation": "Russia",
    "Kosovo (under UNSC res. 1244)" : "Kosovo",
    "Dem. People's Republic of Korea" : "North Korea",
    "State of Palestine" : "Palestine",
    "Syrian Arab Republic" : "Syria",
    "China, Taiwan Province of China" : "Taiwan",
    "Bahamas" : "The Bahamas",
    "United States" : "United States of America",
    "Venezuela (Bolivarian Republic of)" : "Venezuela",
    "Eswatini" : "eSwatini",
    "Serbia" : "Republic of Serbia",
    "Falkland Islands (Malvinas)" : "Falkland Islands",
    "Côte d'Ivoire" : "Ivory Coast"
}

pop_year["country"] = pop_year["country"].replace(rename_map)

world_pop = world.merge(
    pop_year,
    how="left",
    left_on="name",
    right_on="country"
)

# Here we need to copy data as the UN does not distinguish between them: Northern Cyprus → Cyprus
cyprus_pop = world_pop.loc[
    world_pop["name"] == "Cyprus", "population"
].values

if len(cyprus_pop) == 1:
    world_pop.loc[
        world_pop["name"] == "Northern Cyprus", "population"
    ] = cyprus_pop[0]

# Somaliland → Somalia
somalia_pop = world_pop.loc[
    world_pop["name"] == "Somalia", "population"
].values

if len(somalia_pop) == 1:
    world_pop.loc[
        world_pop["name"] == "Somaliland", "population"
    ] = somalia_pop[0]

uncolored = world_pop[world_pop["population"].isna()] 

print("\nRegions in map WITHOUT population data:\n")
for name in sorted(uncolored["name"].unique()):
    print(name)

print(f"\nTotal uncolored regions: {uncolored['name'].nunique()}")

world_pop["population"] = pd.to_numeric(
    world_pop["population"],
    errors="coerce"
)

fig, ax = plt.subplots(1, 1, figsize=(14, 8))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

# Plot WITHOUT legend
world_pop.plot(
    column="population",
    cmap="turbo",
    linewidth=0.4,
    ax=ax,
    edgecolor="black",
    missing_kwds={
        "color": "lightgrey",
        "label": "No data"
    },
    legend=False
)

# Create proper colorbar
norm = mpl.colors.Normalize(
    vmin=world_pop["population"].min(),
    vmax=world_pop["population"].max()
)

sm = mpl.cm.ScalarMappable(norm=norm, cmap="turbo")
sm._A = []  # required for older matplotlib

cbar = fig.colorbar(sm, cax=cax)
cbar.set_label("Population (thousands)")

ax.set_title(f"World Population by Country ({year})", fontsize=14)
ax.axis("off")

plt.show()
# %%

df_happiness_report = pd.read_excel("WHR25_Data_Figure_2.1v3.xlsx")
df_happiness_report.columns

df_hap_2023 = df_happiness_report[
    df_happiness_report["Year"] == year
].copy()


# %%
rename_happiness = {
    "Viet Nam" : "Vietnam",
    "Türkiye" : "Turkey",
    "Côte d’Ivoire" : "Ivory Coast",
    "DR Congo" : "Democratic Republic of the Congo",
    "Congo" : "Republic of the Congo",
    "Eswatini" : "eSwatini",
    "Hong Kong SAR of China" : "",
    "Lao PDR" : "Laos",
    "Republic of Korea" : "South Korea",
    "Republic of Moldova" : "Moldova",
    "Russian Federation" : "Russia",
    "Serbia" : "Republic of Serbia",
    "State of Palestine" : "Palestine",
    "Taiwan Province of China" : "Taiwan",
    "Tanzania" : "United Republic of Tanzania",
    "United States" : "United States of America"
}

df_hap_2023["Country name"] = df_hap_2023["Country name"].replace(rename_happiness)
df_hap_2023 = df_hap_2023.rename(columns={'Country name': 'country'})


pop_countries = set(pop_year["country"].dropna().unique())
hap_countries = set(df_hap_2023["country"].dropna().unique())
missing_in_pop = sorted(hap_countries - pop_countries)
print("\nCountries in WHR but NOT in population data:\n")
for c in missing_in_pop:
    print(c)

print(f"\nTotal missing: {len(missing_in_pop)}")
# %%
combined_df_2023 = pop_year.merge(
    df_hap_2023,
    on="country",
    how="left"
)
world_happiness_2023 = world.merge(
    combined_df_2023,
    how="left",
    left_on="name",
    right_on="country"
)
world_happiness_2023["Life evaluation (3-year average)"] = pd.to_numeric(
    world_happiness_2023["Life evaluation (3-year average)"],
    errors="coerce"
)
fig, ax = plt.subplots(1, 1, figsize=(14, 8))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

world_happiness_2023.plot(
    column="Life evaluation (3-year average)",
    cmap="viridis",
    linewidth=0.4,
    ax=ax,
    edgecolor="black",
    missing_kwds={
        "color": "lightgrey",
        "label": "No data"
    },
    legend=False
)

# Colorbar
norm = mpl.colors.Normalize(
    vmin=world_happiness_2023["Life evaluation (3-year average)"].min(),
    vmax=world_happiness_2023["Life evaluation (3-year average)"].max()
)

sm = mpl.cm.ScalarMappable(norm=norm, cmap="viridis")
sm._A = []

cbar = fig.colorbar(sm, cax=cax)
cbar.set_label("Life evaluation (3-year average)")

ax.set_title("World Happiness Index (2023)", fontsize=14)
ax.axis("off")

plt.show()
# %%


