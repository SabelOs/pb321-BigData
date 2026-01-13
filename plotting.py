#%%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
# %%
df = pd.read_parquet("combined2023_df.parquet")
countries = {"Germany", "United States of America", "Norway", "Iceland", "China", "India", "Mali", "Afghanistan", "Japan", "Finnland", "Argentina", "Austrailia","Egypt"}
#Selected Countries DF
df_sel = df[df["country"].isin(countries)]

color_map = {
    "Low income": "red",
    "Lower middle income": "orange",
    "Upper middle income": "yellow",
    "High income": "blue",
}

colors = df["world_bank_classification"].map(color_map)

legend_handles = [
    Patch(facecolor=color, label=label)
    for label, color in color_map.items()
]
# %% Happiness vs life expectancy
df_plot = df.dropna(subset=[
    "Life evaluation (3-year average)",
    "Life_Expectancy_at_Birth",
    "world_bank_classification"
])

colors = df_plot["world_bank_classification"].map(color_map)

plt.figure(figsize=(9, 7))
plt.scatter(
    df_plot["Life evaluation (3-year average)"],
    df_plot["Life_Expectancy_at_Birth"],
    c=colors,
    alpha=0.8,
    edgecolors="k",
    linewidths=0.3
)

plt.xlabel("Happinesscore / a.u.", fontsize=12)
plt.ylabel("Lebenserwartung bei Geburt / Jahre", fontsize=12)

plt.legend(
    handles=legend_handles,
    title="World Bank classification",
    loc="lower right"
)

plt.tight_layout()
plt.show()

# %% Happiness vs education
df_plot = df.dropna(subset=[
    "Life evaluation (3-year average)",
    "expected_years_of_schooling",
    "world_bank_classification"
])

colors = df_plot["world_bank_classification"].map(color_map)

plt.figure(figsize=(9, 7))
plt.scatter(
    df_plot["Life evaluation (3-year average)"],
    df_plot["expected_years_of_schooling"],
    c=colors,
    alpha=0.8
)

plt.xlabel("Happinesscore / a.u.", fontsize=12)
plt.ylabel("Erwartete Schuljahre / Jahre", fontsize=12)

plt.legend(handles=legend_handles, title="World Bank classification")
plt.tight_layout()
plt.show()


# %% Hapiness vs health


# %% log(GDP) over Happiness
df_plot = df.dropna(subset=[
    "Life evaluation (3-year average)",
    "gdp",
    "world_bank_classification"
])

colors = df_plot["world_bank_classification"].map(color_map)

plt.figure(figsize=(9, 7))
plt.scatter(
    df_plot["Life evaluation (3-year average)"],
    df_plot["gdp"],
    c=colors,
    alpha=0.8
)

plt.xlabel("Happinesscore / a.u.", fontsize=12)
plt.ylabel("log(BIP) / USD", fontsize=12)
plt.yscale("log")

plt.legend(handles=legend_handles, title="World Bank classification")
plt.tight_layout()
plt.show()


# %% GDP_per_Cap over Happiness
df_plot = df.dropna(subset=[
    "Life evaluation (3-year average)",
    "gdp_per_capita",
    "world_bank_classification"
])

colors = df_plot["world_bank_classification"].map(color_map)

plt.figure(figsize=(9, 7))
plt.scatter(
    df_plot["Life evaluation (3-year average)"],
    df_plot["gdp_per_capita"],
    c=colors,
    alpha=0.8
)

plt.xlabel("Happinesscore / a.u.", fontsize=12)
plt.ylabel("log(BIP pro Einwohner) / USD", fontsize=12)
plt.yscale("log")

plt.legend(handles=legend_handles, title="World Bank classification")
plt.tight_layout()
plt.show()

#%% Individual countries: Happiness score
df_plot = df_sel.sort_values("Life evaluation (3-year average)")

color_map = {
    "Low income": "red",
    "Lower middle income": "orange",
    "Upper middle income": "yellow",
    "High income": "blue",
}

colors = df_plot["world_bank_classification"].map(color_map)

plt.figure(figsize=(9, 5))
plt.barh(
    df_plot["country"],
    df_plot["Life evaluation (3-year average)"],
    color=colors
)

plt.xlabel("Happinesscore / a.u.", fontsize=12)
legend_handles = [
    Patch(facecolor=color, label=label)
    for label, color in color_map.items()
]

plt.legend(
    handles=legend_handles,
    title="World Bank classification",
    loc="lower right"
)

plt.tight_layout()
plt.show()


#%% Individual countries: Happiness score
df_plot = df_sel.sort_values("gdp_per_capita")

color_map = {
    "Low income": "red",
    "Lower middle income": "orange",
    "Upper middle income": "yellow",
    "High income": "blue",
}

colors = df_plot["world_bank_classification"].map(color_map)

plt.figure(figsize=(9, 5))
plt.barh(
    df_plot["country"],
    df_plot["gdp_per_capita"],
    color=colors
)

plt.xlabel("BIP pro EInwohner / USD", fontsize=12)
legend_handles = [
    Patch(facecolor=color, label=label)
    for label, color in color_map.items()
]

plt.legend(
    handles=legend_handles,
    title="World Bank classification",
    loc="lower right"
)

plt.tight_layout()
plt.show()

#%% Individual countries: HDI
df_plot = df_sel.sort_values("HDI")

color_map = {
    "Low income": "red",
    "Lower middle income": "orange",
    "Upper middle income": "yellow",
    "High income": "blue",
}

colors = df_plot["world_bank_classification"].map(color_map)

plt.figure(figsize=(9, 5))
plt.barh(
    df_plot["country"],
    df_plot["HDI"],
    color=colors
)

plt.xlabel("HDI / a.u.", fontsize=12)
legend_handles = [
    Patch(facecolor=color, label=label)
    for label, color in color_map.items()
]

plt.legend(
    handles=legend_handles,
    title="World Bank classification",
    loc="lower right"
)

plt.tight_layout()
plt.show()

#%% Individual countries: GNI
df_plot = df_sel.sort_values("GNI_2023")

color_map = {
    "Low income": "red",
    "Lower middle income": "orange",
    "Upper middle income": "yellow",
    "High income": "blue",
}

colors = df_plot["world_bank_classification"].map(color_map)

plt.figure(figsize=(9, 5))
plt.barh(
    df_plot["country"],
    df_plot["GNI_2023"],
    color=colors
)

plt.xlabel("GNI (2023) / USD", fontsize=12)
legend_handles = [
    Patch(facecolor=color, label=label)
    for label, color in color_map.items()
]

plt.legend(
    handles=legend_handles,
    title="World Bank classification",
    loc="lower right"
)

plt.tight_layout()
plt.show()

#%% Individual countries: Poppulation
df_plot = df_sel.sort_values("population")

color_map = {
    "Low income": "red",
    "Lower middle income": "orange",
    "Upper middle income": "yellow",
    "High income": "blue",
}

colors = df_plot["world_bank_classification"].map(color_map)

plt.figure(figsize=(9, 5))
plt.barh(
    df_plot["country"],
    df_plot["population"],
    color=colors
)

plt.xlabel("Einwohnerzahl", fontsize=12)
legend_handles = [
    Patch(facecolor=color, label=label)
    for label, color in color_map.items()
]

plt.legend(
    handles=legend_handles,
    title="World Bank classification",
    loc="lower right"
)

plt.tight_layout()
plt.show()

# %%
