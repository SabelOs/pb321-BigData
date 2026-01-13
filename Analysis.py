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
#plt.legend()
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
        "Total Population, as of 1 July (thousands)",
        "Life Expectancy at Birth, both sexes (years)",
        "Male Life Expectancy at Birth (years)",
        "Female Life Expectancy at Birth (years)"
    ]
].copy()

pop_year.columns = ["country", "population","Life_Expectancy_at_Birth","Male_Life_Expectancy_at_Birth","Female_Life_Expectancy_at_Birth"]

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
    cmap="RdYlBu",
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

sm = mpl.cm.ScalarMappable(norm=norm, cmap="RdYlBu")
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
#%% Import GDP Data:
df_GDP = pd.read_excel("Download-GDPcurrent-USD-countries.xlsx")
df_GDP = df_GDP.set_axis(df_GDP.iloc[1],axis=1)
df_GDP.drop(axis = 0, index = df_GDP.index[:1],inplace = True)
df_GDP.reset_index(drop=True)

gdp_indicator = "Total Value Added"
df_gdp_filtered = df_GDP[
    df_GDP["IndicatorName"] == gdp_indicator
].copy()

df_gdp_2023 = df_gdp_filtered[["Country", 2023.0]].copy()

df_gdp_2023.columns = ["country", "gdp"]

#Manually reasing some of the names which are diffrent between the map and UN data
rename_map = {
    #Scheme: pop_year : world_pop
    "Viet Nam": "Vietnam",
    "Bolivia (Plurinational State of)": "Bolivia",
    "Republic of Moldova": "Moldova",
    "Republic of Korea": "South Korea",
    "Congo": "Republic of the Congo",   # adjust if needed
    "D.R. of the Congo" : "Democratic Republic of the Congo",
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
    "Côte d'Ivoire" : "Ivory Coast",
    "U.R. of Tanzania: Mainland" : "United Republic of Tanzania",
    "D.P.R of Korea" : "North Korea",
    "Laos People's DR" : "Laos"
}

df_gdp_2023["country"] = df_gdp_2023["country"].replace(rename_map)
try:
    combined_df_2023 = combined_df_2023.merge(
        df_gdp_2023,
        how="left",
        left_on="country",    # or "country" — use whatever column combined_df_2023 has
        right_on="country"
    )
    #Calculate the normalized gdp per capita
    combined_df_2023.insert(15,"gdp_per_capita",combined_df_2023["gdp"]/combined_df_2023["population"])
except:
    print("Did not match GDP again")


#%% Now insert developement of the countries (World Bank classification for 2023):
high_income_thresh = 14005
upper_middle_income_thresh = 4516
df_GNI = pd.read_excel("API_NY.GNP.PCAP.CD_DS2_en_excel_v2_875.xls")
df_GNI = df_GNI.set_axis(df_GNI.iloc[2],axis=1)
df_GNI.drop(axis = 0, index = df_GNI.index[:3],inplace = True)
df_GNI.reset_index(drop=True)

df_gni_2023 = df_GNI[["Country Name", 2023.0]].copy()

df_gni_2023.columns = ["country", "gni"]



#%%
rename_map = {
    "Hong Kong SAR, China" : "China, Hong Kong SAR",
    "Macao SAR, China" : "China, Macao SAR",
    "Curacao" : "Curaçao",
    "Congo, Dem. Rep." : "Democratic Republic of the Congo",
    "Egypt, Arab Rep." : "Egypt",
    "Gambia, The" : "Gambia",
    "Iran, Islamic Rep." : "Iran",
    "Cote d'Ivoire" : "Ivory Coast",
    "Kyrgyz Republic" : "Kyrgyzstan",
    "Lao PDR" : "Laos",
    "St. Martin (French part)" : "Martinique",
    "Micronesia (Federated State of)" : "Micronesia (Fed. State of)",
    "Yemen, Rep." : "Yemen",
    "Eswatini" : "eSwatini",
    "Korea, Dem. People's Rep." : "North Korea",
    "Puerto Rico (US)" : "Puerto Rico",
    "Serbia" : "Republic of Serbia",
    "Congo, Rep." : "Republic of the Congo",
    "Russian Federation" : "Russia",
    "Slovak Republic" : "Slovakia",
    "Somalia, Fed. Rep." : "Somalia",
    "Korea, Rep." : "South Korea",
    "Syrian Arab Republic" : "Syria",
    "Bahamas, The" : "The Bahamas",
    "Turkiye" : "Turkey",
    "Tanzania" : "United Republic of Tanzania",
    "Virgin Islands (U.S.)" : "United States Virgin Islands",
    "United States" : "United States of America",
    "Venezuela, RB" : "Venezuela",
    "Viet Nam" : "Vietnam",
    "Palestine, State of" : "Palestine"
}
df_gni_2023["country"] = df_gni_2023["country"].replace(rename_map)
try:
    combined_df_2023 = combined_df_2023.merge(
        df_gni_2023,
        how="left",
        left_on="country",    # or "country" — use whatever column combined_df_2023 has
        right_on="country"
    )
except:
    print("Did not match GNI again")

#%% Code for merging country data:
combined_countries = set(
    combined_df_2023["country"].dropna().unique()
)

gni_countries = set(
    df_gni_2023["country"].dropna().unique()
)
#%%
not_merged = sorted(combined_countries - gni_countries)

print("\nCountries in combined_df_2023 NOT found in df_gni_2023:\n")
i=0
for c in not_merged:
    i+=1
    print(c)

print(f"\nTotal missing: {len(not_merged)}")

#%% Finally, merge the HDR df into the combined df:
df_HDR = pd.read_excel("HDR25_Statistical_Annex_HDI_Table.xlsx")
#%%
#df_HDR = df_HDR.set_axis(df_HDR.iloc[3],axis=1)
df_HDR = df_HDR.rename(columns={
    df_HDR.columns[0]: "HDI_rank_2023",
    df_HDR.columns[1]: "country",
    df_HDR.columns[2]: "HDI",
    df_HDR.columns[3]: "a",
    df_HDR.columns[4]: "life_expectancy_at_birth",
    df_HDR.columns[5]: "b",
    df_HDR.columns[6]: "expected_years_of_schooling",
    df_HDR.columns[7]: "d",
    df_HDR.columns[8]: "mean_years_of_schooling",
    df_HDR.columns[9]: "e",
    df_HDR.columns[10]: "GNI_2023",
    df_HDR.columns[11]: "g",
    df_HDR.columns[12]: "GNI_per_capita-HDI_rank",
    df_HDR.columns[13]: "h",
    df_HDR.columns[14]: "HDI_rank_2022",
})
df_HDR.drop(axis = 0, index = df_HDR.index[:7],inplace = True)
df_HDR.reset_index(drop=True)

df_hdr_2023 = df_HDR[["country", "HDI", "life_expectancy_at_birth", "expected_years_of_schooling", "GNI_2023", "GNI_per_capita-HDI_rank", "HDI_rank_2022"]].copy()


rename_map = {
    "Samoa" : "American Samoa",
    "Bolivia (Plurinational State of)" : "Bolivia",
    "Brunei Darussalam" : "Brunei",
    "Hong Kong, China (SAR)" : "China, Hong Kong SAR",
    "Congo (Democratic Republic of the)" : "Democratic Republic of the Congo",
    "Eswatini (Kingdom of)" : "eSwatini",
    "Iran (Islamic Republic of)": "Iran",
    "Côte d'Ivoire" : "Ivory Coast",
    "Lao People's Democratic Republic" : "Laos",
    "Micronesia (Federated State of)" : "Micronesia (Fed. State of)",
    "Moldova (Republic of)" : "Moldova",
    "Korea (Democratic People's Rep. of)" : "North Korea",
    "Palestine, State of" : "Palestine",
    "Serbia" : "Republic of Serbia",
    "Congo" : "Republic of the Congo",
    "Russian Federation" : "Russia",
    "Korea (Republic of)" : "South Korea",
    "Syria Arab Republic" : "Syria",
    "Bahamas" : "The Bahamas",
    "Türkiye" : "Turkey",
    "Tanzania (United Republic of)" : "United Republic of Tanzania",
    "United States" : "United States of America",
    "Venezuela (Bolivarian Republic of)" : "Venezuela",
    "Viet Nam" : "Vietnam"
}
df_hdr_2023["country"] = df_hdr_2023["country"].replace(rename_map)


try:
    combined_df_2023 = combined_df_2023.merge(
        df_hdr_2023,
        how="left",
        left_on="country",    # or "country" — use whatever column combined_df_2023 has
        right_on="country"
    )
except:
    print("Did not match GNI again")

combined_countries = set(
    combined_df_2023["country"].dropna().unique()
)

hdr_countries = set(
    df_hdr_2023["country"].dropna().unique()
)

not_merged = sorted(combined_countries - hdr_countries)
#%%
print("\nCountries in combined_df_2023 NOT found in df_hdr_2023:\n")
i=0
for c in not_merged:
    i+=1
    if i<45:
        continue
    print(c)

print(f"\nTotal missing: {len(not_merged)}")

#%%
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

world_happiness_2023["HDI"] = pd.to_numeric(
    world_happiness_2023["HDI"],
    errors="coerce"
)

fig, ax = plt.subplots(1, 1, figsize=(14, 8))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

world_happiness_2023.plot(
    column="Life evaluation (3-year average)",
    cmap="RdYlBu",
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

sm = mpl.cm.ScalarMappable(norm=norm, cmap="RdYlBu")
sm._A = []

cbar = fig.colorbar(sm, cax=cax)
cbar.set_label("Life evaluation (3-year average)")

ax.set_title("World Happiness Index (2023)", fontsize=14)
ax.axis("off")

plt.show()



# %%
fig, ax = plt.subplots(1, 1, figsize=(14, 8))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

world_happiness_2023.plot(
    column="gdp",
    cmap="RdYlBu",
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
    vmin=world_happiness_2023["gdp"].min(),
    vmax=world_happiness_2023["gdp"].max()
)

sm = mpl.cm.ScalarMappable(norm=norm, cmap="RdYlBu")
sm._A = []

cbar = fig.colorbar(sm, cax=cax)
cbar.set_label("gdp")

ax.set_title("GDP (2023)", fontsize=14)
ax.axis("off")

plt.show()
# %% Plot gdp per capita


fig, ax = plt.subplots(1, 1, figsize=(14, 8))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

world_happiness_2023.plot(
    column="gdp_per_capita",
    cmap="RdYlBu",
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
    vmin=world_happiness_2023["gdp_per_capita"].min(),
    vmax=world_happiness_2023["gdp_per_capita"].max()
)

sm = mpl.cm.ScalarMappable(norm=norm, cmap="RdYlBu")
sm._A = []

cbar = fig.colorbar(sm, cax=cax)
cbar.set_label("gdp_per_capita")

ax.set_title("GDP per Capita (2023)", fontsize=14)
ax.axis("off")

plt.show()



# %% Plot gni per capita
fig, ax = plt.subplots(1, 1, figsize=(14, 8))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

world_happiness_2023.plot(
    column="gni",
    cmap="RdYlBu",
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
    vmin=world_happiness_2023["gni"].min(),
    vmax=world_happiness_2023["gni"].max()
)

sm = mpl.cm.ScalarMappable(norm=norm, cmap="RdYlBu")
sm._A = []

cbar = fig.colorbar(sm, cax=cax)
cbar.set_label("gni")

ax.set_title("GNI (2023)", fontsize=14)
ax.axis("off")

plt.show()

# %% Create happiness barplot per country
df_sorted = combined_df_2023.dropna(subset=["Life evaluation (3-year average)"]).sort_values("Life evaluation (3-year average)")

plt.figure(figsize=(6, 10))
plt.barh(
    df_sorted["country"],
    df_sorted["Life evaluation (3-year average)"]
)
plt.xlabel("Life evaluation (3-year average)")
plt.ylabel("Country")
plt.tight_layout()
plt.show()


#%% Put the developement status as col:
high_income_thresh = 13845
upper_middle_income_thresh = 4466
lower_middle_income_thresh = 1136
low_income_thresh = 1135

bins = [-np.inf, 1135, 4465, 13845, np.inf]
labels = [
    "Low income",
    "Lower middle income",
    "Upper middle income",
    "High income"
]

combined_df_2023["world_bank_classification"] = pd.cut(
    combined_df_2023["gni"],
    bins=bins,
    labels=labels
)

#%%
from pandas.api.types import CategoricalDtype

income_order = CategoricalDtype(
    categories=[
        "Low income",
        "Lower middle income",
        "Upper middle income",
        "High income"
    ],
    ordered=True
)

combined_df_2023["world_bank_classification"] = (
    combined_df_2023["world_bank_classification"]
    .astype(income_order)
)

import matplotlib.patches as mpatches
import numpy as np

# Create World Bank classification in world_happiness_2023 based on GNI
bins = [-np.inf, 1135, 4465, 13845, np.inf]
labels = ["Low income", "Lower middle income", "Upper middle income", "High income"]

world_happiness_2023["world_bank_classification"] = pd.cut(
    world_happiness_2023["gni"],
    bins=bins,
    labels=labels
)

#Add a category for missing values
world_happiness_2023["world_bank_classification"] = (
    world_happiness_2023["world_bank_classification"]
    .cat.add_categories("No data")
    .fillna("No data")
)

# Manual color mapping
income_colors = {
    "Low income": "red",
    "Lower middle income": "orange",
    "Upper middle income": "yellow",
    "High income": "blue",
    "No data": "lightgrey"
}

# Map column to colors
colors = world_happiness_2023["world_bank_classification"].map(income_colors)

# Plot
fig, ax = plt.subplots(1, 1, figsize=(14, 8))

world_happiness_2023.plot(
    color=colors,
    linewidth=0.4,
    ax=ax,
    edgecolor="black"
)

ax.set_title("World Bank Income Classification (2023)", fontsize=14)
ax.axis("off")

# Manual legend
legend_handles = [mpatches.Patch(color=c, label=l) for l, c in income_colors.items()]
ax.legend(
    handles=legend_handles,
    title="World Bank income group",
    loc="lower left",
    frameon=True
)

plt.show()


# %% Plot hdi 
fig, ax = plt.subplots(1, 1, figsize=(14, 8))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

world_happiness_2023.plot(
    column="HDI",
    cmap="RdYlBu",
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
    vmin=world_happiness_2023["HDI"].min(),
    vmax=world_happiness_2023["HDI"].max()
)

sm = mpl.cm.ScalarMappable(norm=norm, cmap="RdYlBu")
sm._A = []

cbar = fig.colorbar(sm, cax=cax)
cbar.set_label("hdi")

ax.set_title("HDI (2023)", fontsize=14)
ax.axis("off")

plt.show()


# %%Save 2023 DF as parquet
combined_df_2023 = combined_df_2023.replace("..", np.nan)
combined_df_2023.to_parquet(
    "combined2023_df.parquet",
    engine="pyarrow"
)
