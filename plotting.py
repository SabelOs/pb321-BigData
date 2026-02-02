#%%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns
from matplotlib.lines import Line2D
# %%
df = pd.read_parquet("combined2023_df.parquet")

# English → German country names
country_translation = {
    "Germany": "Deutschland",
    "United States of America": "Vereinigte Staaten",
    "Norway": "Norwegen",
    "Iceland": "Island",
    "China": "China",
    "India": "Indien",
    "Mali": "Mali",
    "Afghanistan": "Afghanistan",
    "Japan": "Japan",
    "Finland": "Finnland",
    "Argentina": "Argentinien",
    "Australia": "Australien",
    "Egypt": "Ägypten"
}

# Countries to select (use English names as stored in the data!)
countries = set(country_translation.keys())

# Select countries
df_sel = df[df["country"].isin(countries)].copy()

# Rename to German
df_sel["country"] = df_sel["country"].replace(country_translation)
plt.rcParams['font.family'] = 'Liberation Sans'
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['axes.labelsize'] = 14

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


label_de = {
    "Low income": "Niedriges Einkommen",
    "Lower middle income": "Unteres mittleres Einkommen",
    "Upper middle income": "Oberes mittleres Einkommen",
    "High income": "Hohes Einkommen",
}

legend_handles = [
    Patch(
        facecolor=color_map[key],
        label=label_de[key]
    )
    for key in color_map
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
    df_plot["Life_Expectancy_at_Birth"],
    df_plot["Life evaluation (3-year average)"],
    c=colors,
    edgecolors="k",
    linewidths=0.3
)

plt.ylabel("Happiness Index / a.u.", fontsize=14)
plt.xlabel("Lebenserwartung bei Geburt / Jahre", fontsize=14)

plt.legend(
    handles=legend_handles,
    title="Weltbank-Einkommensklassifikation",
    loc="upper left",
    fontsize=14,
    title_fontsize=15
)
plt.xticks()
plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-Happiness-Lebenserwartung.png")
plt.show()

# %% Happiness vs life expectancy with linear regression
df_plot = df.dropna(subset=[
    "Life evaluation (3-year average)",
    "Life_Expectancy_at_Birth",
    "world_bank_classification"
])

x = df_plot["Life_Expectancy_at_Birth"].values
y = df_plot["Life evaluation (3-year average)"].values

# linear regression
a, b = np.polyfit(x, y, 1)

x_fit = np.linspace(x.min(), x.max(), x.size)
y_fit = a * x_fit + b

# R²
y_pred = a * x + b
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - y.mean())**2)
r2 = 1 - ss_res / ss_tot

colors = df_plot["world_bank_classification"].map(color_map)

plt.figure(figsize=(9, 7))

fit_line, = plt.plot(
    x_fit,
    y_fit,
    color="black",
    linestyle="dashed",
    linewidth=2,
    label=rf"Lineare Regression, $R^2 = {r2:.2f}$"
)

plt.scatter(
    x,
    y,
    c=colors,
    edgecolors="k",
    linewidths=0.3
)

plt.xlabel("Lebenserwartung bei Geburt / Jahre", fontsize=14)
plt.ylabel("Happiness Index / a.u.", fontsize=14)

plt.legend(
    handles=legend_handles + [fit_line],
    title="Weltbank-Einkommensklassifikation",
    loc="upper left",
    fontsize=14,
    title_fontsize=15
)

plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-Happiness-Lebenserwartung-regression.png")
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(x, np.abs(y-y_fit))
plt.axhline(0, color="black", linestyle="dashed", linewidth=1)

plt.xlabel("Lebenserwartung bei Geburt / Jahre")
plt.ylabel("Residuen (Happiness)")
plt.title("Residual plot – zunehmende Streuung bei kleiner Lebenserwartung")

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
    df_plot["expected_years_of_schooling"],
    df_plot["Life evaluation (3-year average)"],
    c=colors
)

plt.ylabel("Happiness Index / a.u.", fontsize=14)
plt.xlabel("Erwartete Schuljahre / Jahre", fontsize=14)

plt.legend(handles=legend_handles, title="Weltbank-Einkommensklassifikation",title_fontsize=15,fontsize=14)
plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-Happiness-Bildung.png")
plt.show()

#%% Hapiness vs education boxplots:
bins = [0, 8, 10, 12, 14, 16, 18, float("inf")]
labels = [
    "≤ 8",
    "8–10",
    "10–12",
    "12–14",
    "14–16",
    "16–18",
    "> 18"
]

df_plot["schooling_bin"] = pd.cut(
    df_plot["expected_years_of_schooling"],
    bins=bins,
    labels=labels,
    right=True
)

box_data = [
    df_plot.loc[df_plot["schooling_bin"] == label,
                "Life evaluation (3-year average)"].dropna()
    for label in labels
]

plt.figure(figsize=(9, 7))

bp = plt.boxplot(
    box_data,
    labels=labels,
    whis=[0, 100],        # whiskers go to min/max (extreme values)
    showmeans=True,      # show mean
    meanline=True,       # mean as line (not point)
    patch_artist=True    # allows box coloring
)

# Box appearance
for box in bp["boxes"]:
    box.set(facecolor="lightgray", alpha=0.7)

# Median line
for median in bp["medians"]:
    median.set(color="black", linewidth=2)

# Mean line
for mean in bp["means"]:
    mean.set(color="red", linewidth=2)

# Whiskers
for whisker in bp["whiskers"]:
    whisker.set(color="black", linewidth=1.5)

# Caps
for cap in bp["caps"]:
    cap.set(color="black", linewidth=1.5)

legend_elements = [
    Line2D([0], [0], color="red", lw=2, label="Mittelwert"),
    Line2D([0], [0], color="black", lw=2, label="Median"),
]

plt.legend(
    handles=legend_elements,
    loc="upper left",
    frameon=True,
    fontsize=14
)
plt.xlabel("Erwartete Bildungsdauer / Jahre")
plt.ylabel("Happiness Index / a.u.")

plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/boxplot-Happiness-Bildung.png")
plt.show()


# %% log(GDP) over Happiness
df_plot = df.dropna(subset=[
    "Life evaluation (3-year average)",
    "gdp",
    "world_bank_classification"
])

colors = df_plot["world_bank_classification"].map(color_map)

plt.figure(figsize=(9, 7))
plt.scatter(
    df_plot["gdp"],
    df_plot["Life evaluation (3-year average)"],
    c=colors
)

plt.ylabel("Happiness Index / a.u.", fontsize=14)
plt.xlabel("BIP / USD", fontsize=14)
#plt.xscale("log")

plt.legend(handles=legend_handles, title="Weltbank-Einkommensklassifikation",title_fontsize=15,fontsize=14)
plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-Happiness-BIP.png")
plt.show()

# %% Happiness vs HDI with linear regression
df_plot = df.dropna(subset=[
    "Life evaluation (3-year average)",
    "HDI",
    "world_bank_classification"
])

x = df_plot["HDI"].values
y = df_plot["Life evaluation (3-year average)"].values

# linear regression
a, b = np.polyfit(x, y, 1)

x_fit = np.linspace(x.min(), x.max(), x.size)
y_fit = a * x_fit + b

# R²
y_pred = a * x + b
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - y.mean())**2)
r2 = 1 - ss_res / ss_tot

colors = df_plot["world_bank_classification"].map(color_map)

plt.figure(figsize=(9, 7))

fit_line, = plt.plot(
    x_fit,
    y_fit,
    color="black",
    linestyle="dashed",
    linewidth=2,
    label=rf"Lineare Regression, $R^2 = {r2:.2f}$"
)

plt.scatter(
    x,
    y,
    c=colors,
    edgecolors="k",
    linewidths=0.3
)

plt.xlabel("HDI / a.u.", fontsize=14)
plt.ylabel("Happiness Index / a.u.", fontsize=14)

plt.legend(
    handles=legend_handles + [fit_line],
    title="Weltbank-Einkommensklassifikation",
    loc="upper left",
    fontsize=14,
    title_fontsize=15
)

plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-Happiness-HDI-regression.png")
plt.show()



# %% GDP_per_Cap over Happiness
df_plot = df.dropna(subset=[
    "Life evaluation (3-year average)",
    "gdp_per_capita",
    "world_bank_classification"
])
#regression:
x = df_plot["Life evaluation (3-year average)"].values
y = df_plot["gdp_per_capita"].values

# log regression

log_y = np.log(y)

a, b = np.polyfit(x, log_y, 1)


x_fit = np.linspace(x.min(), x.max(), 300)
y_fit = np.exp(b) * np.exp(a * x_fit)

#r² Wert:
log_y_fit = a * x + b
ss_res = np.sum((log_y - log_y_fit)**2)
ss_tot = np.sum((log_y - log_y.mean())**2)
r2 = 1 - ss_res / ss_tot

colors = df_plot["world_bank_classification"].map(color_map)

plt.figure(figsize=(9, 7))
fit_line, = plt.plot(
    y_fit,
    x_fit,
    color="black",
    linewidth=2,
    linestyle ='dashed',
    label=rf"Logarithmische Regression, $R^2 = {r2:.2f}$"
)
plt.scatter(
    df_plot["gdp_per_capita"],
    df_plot["Life evaluation (3-year average)"],
    c=colors
)


plt.ylabel("Happiness Index / a.u.", fontsize=14)
plt.xlabel("BIP pro Einwohner / USD", fontsize=14)
#plt.xscale("log")

plt.legend(
    handles=legend_handles + [fit_line],
    title="Weltbank-Einkommensklassifikation",
    title_fontsize=15,
    fontsize=14
)
plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-Happiness-BIP_pro_Einwohner.png")
plt.show()

# %% GDP_per_Cap over Happiness (High income only)

df_hi = df.dropna(subset=[
    "Life evaluation (3-year average)",
    "gdp_per_capita",
    "world_bank_classification"
])

df_hi = df_hi[df_hi["world_bank_classification"] == "High income"]

plt.figure(figsize=(9, 7))
plt.scatter(
    df_hi["gdp_per_capita"],
    df_hi["Life evaluation (3-year average)"],
    c=color_map["High income"],
    label="Hohes Einkommen"
)

plt.ylabel("Happiness Index / a.u.", fontsize=14)
plt.xlabel("BIP pro Einwohner / USD", fontsize=14)
#plt.xscale("log")

plt.legend(title="Weltbank-Einkommensklassifikation",title_fontsize=15,fontsize=14)
plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-Happiness-BIP_pro_Einwohner-HighIncome.png")
plt.show()

#%% Life expectancy vs gdp
df_plot = df.dropna(subset=[
    "Life_Expectancy_at_Birth",
    "Male_Life_Expectancy_at_Birth",
    "Female_Life_Expectancy_at_Birth",
    "gdp_per_capita",
    "world_bank_classification"
])

color_map = {
    "Low income": "red",
    "Lower middle income": "orange",
    "Upper middle income": "gold",
    "High income": "blue",
}

# Drop rows with unknown classifications
df_plot = df_plot[df_plot["world_bank_classification"].isin(color_map)]

colors = df_plot["world_bank_classification"].map(color_map)

plt.figure(figsize=(9, 7))
plt.scatter(
    df_plot["gdp_per_capita"],
    df_plot["Life_Expectancy_at_Birth"],
    c=colors
)

plt.xlabel("BIP pro Einwohner / USD")
plt.ylabel("Lebenserwartung / Jahre")
plt.xscale("log")

plt.legend(
    handles=legend_handles,
    title="Weltbank-Einkommensklassifikation",
    loc="upper left",
    title_fontsize=15,
    fontsize=14
)
plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-BIP_pro_Einwohner-Lebenserwartung.png")
plt.show()

plt.figure(figsize=(9, 7))

plt.scatter(
    df_plot["gdp_per_capita"],
    df_plot["Male_Life_Expectancy_at_Birth"],
    color="blue",
    label="Männliche Lebenserwartung"
)

plt.scatter(
    df_plot["gdp_per_capita"],
    df_plot["Female_Life_Expectancy_at_Birth"],
    color="pink",
    label="Weibliche Lebenserwartung"
)

plt.xlabel("BIP pro Einwohner / USD")
plt.ylabel("Lebenserwartung / Jahre")
plt.xscale("log")

plt.legend(loc="upper left",fontsize=14)
plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-BIP_pro_Einwohner-Lebenserwartung-MannFrau.png")
plt.show()

gender_gap = (
    df_plot["Female_Life_Expectancy_at_Birth"]
    - df_plot["Male_Life_Expectancy_at_Birth"]
)

plt.figure(figsize=(9, 7))
plt.scatter(
    df_plot["gdp_per_capita"],
    gender_gap,
    c=colors,
)

plt.xlabel("GDP per capita (USD)")
plt.ylabel("Differenz Lebenserwartung (Weiblich - Männlich) / Jahre")
plt.xscale("log")

plt.legend(
    handles=legend_handles,
    title="Weltbank-Einkommensklassifikation",
    loc="upper left",
    title_fontsize=15,
    fontsize=14
)
plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-BIP_pro_Einwohner-Lebenserwartung-Differenz.png")
plt.show()


#%% Correlation heatmap
columns_of_interest = [
    "population",
    "Life_Expectancy_at_Birth",
    "Life evaluation (3-year average)",
    "gdp_per_capita",
    "gdp",
    "gni",
    "HDI",
    "expected_years_of_schooling"
]

df_corr = df_plot[columns_of_interest].copy()

# Add gender life expectancy difference for correlation
df_corr["Gender_Life_Expectancy_Difference"] = (
    df_plot["Female_Life_Expectancy_at_Birth"]
    - df_plot["Male_Life_Expectancy_at_Birth"]
)

df_corr["log_gdp_per_capita"] = np.log(df_corr["gdp_per_capita"])

correlation_matrix = df_corr.corr()

german_labels = {
    "population": "Bevölkerung",
    "Life_Expectancy_at_Birth": "Lebenserwartung",
    "Life evaluation (3-year average)": "Happiness Index",
    "gdp_per_capita": "BIP pro Einwohner",
    "gdp": "BIP",
    "gni": "GNI",
    "HDI": "HDI",
    "expected_years_of_schooling": "Erwartete Schuljahre",
    "log_gdp_per_capita": "log(BIP pro Einwohner)",
    "Gender_Life_Expectancy_Difference": "Geschlechterdifferenz-\nLebenserwartung"
}

correlation_matrix.rename(
    index=german_labels,
    columns=german_labels,
    inplace=True
)

plt.figure(figsize=(10, 8))
vmin = correlation_matrix.min().min()
sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    square=True,
    vmin=vmin,
    center=0.25,
    cbar_kws={"shrink": 0.8}
)

plt.tight_layout()
plt.xticks(rotation=45, ha="right", fontsize=14)
plt.yticks(fontsize=14)
plt.savefig("/home/soeke/pb321-BigData/figures/plot-correlation-Heatmap.png")
plt.show()



#%% Individual countries: Happiness Index
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

plt.xlabel("Happiness Index / a.u.", fontsize=14)

plt.legend(
    handles=legend_handles,
    title="Weltbank-Einkommensklassifikation",
    loc="upper left",
    title_fontsize=15,
    fontsize=14
)

plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-Happiness-individual-Countries.png")
plt.show()


#%% Individual countries: Happiness Index
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

plt.xlabel("BIP pro Einwohner / USD", fontsize=14)
"""
legend_handles = [
    Patch(facecolor=color, label=label)
    for label, color in color_map.items()
]
"""

plt.legend(
    handles=legend_handles,
    title="Weltbank-Einkommensklassifikation",
    loc="lower right",
    title_fontsize=15,
    fontsize=14
)

plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-BIP_pro_Einwohner-individual-Countries.png")
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

plt.xlabel("HDI / a.u.", fontsize=14)
"""
legend_handles = [
    Patch(facecolor=color, label=label)
    for label, color in color_map.items()
]
"""

plt.legend(
    handles=legend_handles,
    title="Weltbank-Einkommensklassifikation",
    loc="upper left",
    title_fontsize=15,
    fontsize=14
)

plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-HDI-individual-Countries.png")
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

plt.xlabel("GNI (2023) / USD", fontsize=14)


plt.legend(
    handles=legend_handles,
    title="Weltbank-Einkommensklassifikation",
    loc="lower right",
    title_fontsize=15,
    fontsize=14
)

plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-GNI-individual-Countries.png")
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

plt.xlabel("Einwohnerzahl", fontsize=14)


plt.legend(
    handles=legend_handles,
    title="Weltbank-Einkommensklassifikation",
    loc="lower right",
    title_fontsize=15,
    fontsize=14
)

plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-Einwohnerzahl-individual-Countries.png")
plt.show()


#%% Individual countries: Life expectancy (male vs female)

df_plot = df_sel.sort_values("Female_Life_Expectancy_at_Birth")

x = np.arange(len(df_plot["country"]))
bar_width = 0.4  # touching bars

plt.figure(figsize=(10, 5))

plt.bar(
    x - bar_width / 2,
    df_plot["Male_Life_Expectancy_at_Birth"],
    width=bar_width,
    color="blue",
    label="Männliche Lebenserwartung"
)

plt.bar(
    x + bar_width / 2,
    df_plot["Female_Life_Expectancy_at_Birth"],
    width=bar_width,
    color="pink",
    label="Weibliche Lebenserwartung"
)

plt.xticks(x, df_plot["country"], rotation=45)
plt.ylabel("Lebenserwartung / Jahre", fontsize=14)

plt.legend(loc="upper left",fontsize=14)
plt.tight_layout()
plt.savefig("/home/soeke/pb321-BigData/figures/plot-Lebenserwartung-MannFrau-individual-Countries.png")
plt.show()

# %%
