"""
EcoLens - Energy Transition Intelligence
Data Processing and Analytics Module

Provides clean, reusable functions for data loading, validation,
KPI calculations, data-driven insight generation, and Decision Lab scoring.
"""

import os
import pandas as pd
import numpy as np

# Geographic region mapping for all 176 countries in the dataset
REGION_MAP = {
    # Africa
    'Algeria': 'Africa', 'Angola': 'Africa', 'Benin': 'Africa', 'Botswana': 'Africa',
    'Burkina Faso': 'Africa', 'Burundi': 'Africa', 'Cameroon': 'Africa', 'Central African Republic': 'Africa',
    'Chad': 'Africa', 'Comoros': 'Africa', 'Congo': 'Africa', 'Djibouti': 'Africa',
    'Egypt': 'Africa', 'Equatorial Guinea': 'Africa', 'Eritrea': 'Africa', 'Eswatini': 'Africa',
    'Ethiopia': 'Africa', 'Gabon': 'Africa', 'Gambia': 'Africa', 'Ghana': 'Africa',
    'Guinea': 'Africa', 'Guinea-Bissau': 'Africa', 'Kenya': 'Africa', 'Lesotho': 'Africa',
    'Liberia': 'Africa', 'Libya': 'Africa', 'Madagascar': 'Africa', 'Malawi': 'Africa',
    'Mali': 'Africa', 'Mauritania': 'Africa', 'Mauritius': 'Africa', 'Morocco': 'Africa',
    'Mozambique': 'Africa', 'Namibia': 'Africa', 'Niger': 'Africa', 'Nigeria': 'Africa',
    'Rwanda': 'Africa', 'Sao Tome and Principe': 'Africa', 'Senegal': 'Africa', 'Seychelles': 'Africa',
    'Sierra Leone': 'Africa', 'Somalia': 'Africa', 'South Africa': 'Africa', 'South Sudan': 'Africa',
    'Sudan': 'Africa', 'Togo': 'Africa', 'Tunisia': 'Africa', 'Uganda': 'Africa',
    'Zambia': 'Africa', 'Zimbabwe': 'Africa',

    # Asia
    'Afghanistan': 'Asia', 'Armenia': 'Asia', 'Azerbaijan': 'Asia', 'Bahrain': 'Asia',
    'Bangladesh': 'Asia', 'Bhutan': 'Asia', 'Cambodia': 'Asia', 'China': 'Asia',
    'Cyprus': 'Asia', 'Georgia': 'Asia', 'India': 'Asia', 'Indonesia': 'Asia',
    'Iraq': 'Asia', 'Israel': 'Asia', 'Japan': 'Asia', 'Jordan': 'Asia',
    'Kazakhstan': 'Asia', 'Kuwait': 'Asia', 'Kyrgyzstan': 'Asia', 'Lebanon': 'Asia',
    'Malaysia': 'Asia', 'Maldives': 'Asia', 'Mongolia': 'Asia', 'Myanmar': 'Asia',
    'Nepal': 'Asia', 'Oman': 'Asia', 'Pakistan': 'Asia', 'Philippines': 'Asia',
    'Qatar': 'Asia', 'Saudi Arabia': 'Asia', 'Singapore': 'Asia', 'Sri Lanka': 'Asia',
    'Tajikistan': 'Asia', 'Thailand': 'Asia', 'Turkey': 'Asia', 'Turkmenistan': 'Asia',
    'United Arab Emirates': 'Asia', 'Uzbekistan': 'Asia', 'Yemen': 'Asia',

    # Europe
    'Albania': 'Europe', 'Austria': 'Europe', 'Belarus': 'Europe', 'Belgium': 'Europe',
    'Bosnia and Herzegovina': 'Europe', 'Bulgaria': 'Europe', 'Croatia': 'Europe', 'Czechia': 'Europe',
    'Denmark': 'Europe', 'Estonia': 'Europe', 'Finland': 'Europe', 'France': 'Europe',
    'Germany': 'Europe', 'Greece': 'Europe', 'Hungary': 'Europe', 'Iceland': 'Europe',
    'Ireland': 'Europe', 'Italy': 'Europe', 'Latvia': 'Europe', 'Lithuania': 'Europe',
    'Luxembourg': 'Europe', 'Malta': 'Europe', 'Montenegro': 'Europe', 'Netherlands': 'Europe',
    'North Macedonia': 'Europe', 'Norway': 'Europe', 'Poland': 'Europe', 'Portugal': 'Europe',
    'Romania': 'Europe', 'Serbia': 'Europe', 'Slovakia': 'Europe', 'Slovenia': 'Europe',
    'Spain': 'Europe', 'Sweden': 'Europe', 'Switzerland': 'Europe', 'Ukraine': 'Europe',
    'United Kingdom': 'Europe',

    # Latin America & Caribbean
    'Antigua and Barbuda': 'Latin America & Caribbean', 'Argentina': 'Latin America & Caribbean',
    'Aruba': 'Latin America & Caribbean', 'Bahamas': 'Latin America & Caribbean',
    'Barbados': 'Latin America & Caribbean', 'Belize': 'Latin America & Caribbean',
    'Bermuda': 'Latin America & Caribbean', 'Brazil': 'Latin America & Caribbean',
    'Cayman Islands': 'Latin America & Caribbean', 'Chile': 'Latin America & Caribbean',
    'Colombia': 'Latin America & Caribbean', 'Costa Rica': 'Latin America & Caribbean',
    'Cuba': 'Latin America & Caribbean', 'Dominica': 'Latin America & Caribbean',
    'Dominican Republic': 'Latin America & Caribbean', 'Ecuador': 'Latin America & Caribbean',
    'El Salvador': 'Latin America & Caribbean', 'French Guiana': 'Latin America & Caribbean',
    'Grenada': 'Latin America & Caribbean', 'Guatemala': 'Latin America & Caribbean',
    'Guyana': 'Latin America & Caribbean', 'Haiti': 'Latin America & Caribbean',
    'Honduras': 'Latin America & Caribbean', 'Jamaica': 'Latin America & Caribbean',
    'Mexico': 'Latin America & Caribbean', 'Nicaragua': 'Latin America & Caribbean',
    'Panama': 'Latin America & Caribbean', 'Paraguay': 'Latin America & Caribbean',
    'Peru': 'Latin America & Caribbean', 'Puerto Rico': 'Latin America & Caribbean',
    'Saint Kitts and Nevis': 'Latin America & Caribbean', 'Saint Lucia': 'Latin America & Caribbean',
    'Saint Vincent and the Grenadines': 'Latin America & Caribbean', 'Suriname': 'Latin America & Caribbean',
    'Trinidad and Tobago': 'Latin America & Caribbean', 'Uruguay': 'Latin America & Caribbean',

    # Northern America
    'Canada': 'Northern America', 'United States': 'Northern America',

    # Oceania
    'Australia': 'Oceania', 'Fiji': 'Oceania', 'Kiribati': 'Oceania', 'Nauru': 'Oceania',
    'New Caledonia': 'Oceania', 'New Zealand': 'Oceania', 'Papua New Guinea': 'Oceania',
    'Samoa': 'Oceania', 'Solomon Islands': 'Oceania', 'Tonga': 'Oceania', 'Tuvalu': 'Oceania',
    'Vanuatu': 'Oceania'
}

# Real dataset column constants
COL_ENTITY = "Entity"
COL_YEAR = "Year"
COL_ELEC_ACCESS = "Access to electricity (% of population)"
COL_CLEAN_COOKING = "Access to clean fuels for cooking"
COL_RENEWABLE_CAPACITY = "Renewable-electricity-generating-capacity-per-capita"
COL_FINANCIAL_FLOWS = "Financial flows to developing countries (US $)"
COL_RENEWABLE_SHARE_TOTAL = "Renewable energy share in the total final energy consumption (%)"
COL_FOSSIL_ELEC = "Electricity from fossil fuels (TWh)"
COL_NUCLEAR_ELEC = "Electricity from nuclear (TWh)"
COL_RENEWABLES_ELEC = "Electricity from renewables (TWh)"
COL_LOW_CARBON_ELEC = "Low-carbon electricity (% electricity)"
COL_PRIMARY_ENERGY_PC = "Primary energy consumption per capita (kWh/person)"
COL_ENERGY_INTENSITY = "Energy intensity level of primary energy (MJ/$2017 PPP GDP)"
COL_CO2_EMISSIONS = "Value_co2_emissions_kt_by_country"
COL_RENEWABLES_PRIMARY = "Renewables (% equivalent primary energy)"
COL_GDP_GROWTH = "gdp_growth"
COL_GDP_PER_CAPITA = "gdp_per_capita"


def find_data_file():
    """Locates the dataset in common paths without altering the original file."""
    candidates = [
        "data.csv",
        "global-data-on-sustainable-energy (1).csv",
        os.path.join("ecolens", "data.csv"),
        os.path.join(os.path.dirname(__file__), "data.csv"),
        os.path.join(os.path.dirname(__file__), "global-data-on-sustainable-energy (1).csv"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Could not find dataset file in project directory.")


def load_dataset():
    """
    Loads and validates the sustainable energy dataset.
    Preserves original columns and data integrity without overwriting the CSV.
    """
    path = find_data_file()
    df = pd.read_csv(path)
    
    # Ensure Year is int
    df[COL_YEAR] = pd.to_numeric(df[COL_YEAR], errors="coerce").astype("Int64")
    
    # Add Region column based on standard geographic mapping
    df["Region"] = df[COL_ENTITY].map(lambda c: REGION_MAP.get(c, "Other"))
    
    return df


def get_available_years(df):
    """Returns sorted list of available integer years in the dataset."""
    return sorted(df[COL_YEAR].dropna().unique().tolist())


def get_available_regions(df):
    """Returns list of distinct regions."""
    regions = sorted([r for r in df["Region"].unique() if r != "Other"])
    return ["All Regions"] + regions


def get_available_countries(df, region=None):
    """Returns sorted list of countries, optionally filtered by region."""
    if region and region != "All Regions":
        sub = df[df["Region"] == region]
        return sorted(sub[COL_ENTITY].unique().tolist())
    return sorted(df[COL_ENTITY].unique().tolist())


def filter_by_year_and_region(df, year, region="All Regions"):
    """
    Filters dataset for a given year and optional region.
    Returns filtered DataFrame copy.
    """
    filtered = df[df[COL_YEAR] == year].copy()
    if region and region != "All Regions":
        filtered = filtered[filtered["Region"] == region]
    return filtered


def compute_overview_kpis(filtered_df):
    """
    Calculates the 4 required Page 1 KPI metrics:
    1. Countries Tracked
    2. Mean Electricity Access (% of population) - unweighted country mean
    3. Mean Low-Carbon Electricity (% electricity) - unweighted country mean
    4. Electricity Access Gap (Max - Min country-level access %)
    
    Returns a dict with formatted values, raw values, and observation counts.
    """
    if filtered_df.empty:
        return {
            "countries_tracked": 0,
            "mean_elec_access": None,
            "mean_low_carbon": None,
            "access_gap": None,
            "min_elec_country": None,
            "max_elec_country": None,
            "n_elec_valid": 0,
            "n_low_carbon_valid": 0
        }

    # 1. Countries Tracked
    countries_count = filtered_df[COL_ENTITY].nunique()

    # 2. Electricity Access (mean of valid country observations)
    valid_elec = filtered_df.dropna(subset=[COL_ELEC_ACCESS])
    mean_elec = valid_elec[COL_ELEC_ACCESS].mean() if not valid_elec.empty else None

    # 3. Low-Carbon Electricity (mean of valid country observations)
    valid_lowc = filtered_df.dropna(subset=[COL_LOW_CARBON_ELEC])
    mean_lowc = valid_lowc[COL_LOW_CARBON_ELEC].mean() if not valid_lowc.empty else None

    # 4. Electricity Access Gap (highest - lowest valid)
    if not valid_elec.empty:
        min_row = valid_elec.loc[valid_elec[COL_ELEC_ACCESS].idxmin()]
        max_row = valid_elec.loc[valid_elec[COL_ELEC_ACCESS].idxmax()]
        gap = max_row[COL_ELEC_ACCESS] - min_row[COL_ELEC_ACCESS]
        min_country = f"{min_row[COL_ENTITY]} ({min_row[COL_ELEC_ACCESS]:.1f}%)"
        max_country = f"{max_row[COL_ENTITY]} ({max_row[COL_ELEC_ACCESS]:.1f}%)"
    else:
        gap = None
        min_country = None
        max_country = None

    return {
        "countries_tracked": countries_count,
        "mean_elec_access": mean_elec,
        "mean_low_carbon": mean_lowc,
        "access_gap": gap,
        "min_elec_country": min_country,
        "max_elec_country": max_country,
        "n_elec_valid": len(valid_elec),
        "n_low_carbon_valid": len(valid_lowc)
    }


def generate_overview_insights(df, selected_year):
    """
    Generates rule-based, data-driven analytical observations
    supported strictly by the actual records in the dataset.
    """
    insights = []
    
    # Current year slice
    cur = df[df[COL_YEAR] == selected_year]
    
    # 1. Countries with high electricity access (>95%) but low low-carbon electricity (<20%)
    fossil_heavy = cur[(cur[COL_ELEC_ACCESS] >= 95.0) & (cur[COL_LOW_CARBON_ELEC] < 20.0)]
    if not fossil_heavy.empty:
        names = fossil_heavy.sort_values(COL_LOW_CARBON_ELEC)[COL_ENTITY].head(4).tolist()
        names_str = ", ".join(names)
        insights.append({
            "type": "warning",
            "title": "Fossil-Reliant Electrification",
            "text": f"In {selected_year}, {len(fossil_heavy)} countries maintained near-universal electricity access (95% or higher) while relying primarily on fossil generation (under 20% low-carbon electricity), including {names_str}."
        })

    # 2. Countries facing a double deficit (<50% electricity access and <20% low-carbon electricity)
    double_deficit = cur[(cur[COL_ELEC_ACCESS] < 50.0) & (cur[COL_LOW_CARBON_ELEC] < 20.0)]
    if not double_deficit.empty:
        names = double_deficit.sort_values(COL_ELEC_ACCESS)[COL_ENTITY].head(4).tolist()
        names_str = ", ".join(names)
        insights.append({
            "type": "alert",
            "title": "Double Energy Deficit",
            "text": f"{len(double_deficit)} countries in {selected_year} experienced both low electrification (under 50% access) and high fossil dependence (under 20% low-carbon electricity), including {names_str}."
        })

    # 3. Off-grid / Clean potential (low access <60% but high low-carbon >=70% e.g. hydro)
    clean_developing = cur[(cur[COL_ELEC_ACCESS] < 60.0) & (cur[COL_LOW_CARBON_ELEC] >= 70.0)]
    if not clean_developing.empty and len(insights) < 3:
        names = clean_developing.sort_values(COL_LOW_CARBON_ELEC, ascending=False)[COL_ENTITY].head(4).tolist()
        names_str = ", ".join(names)
        insights.append({
            "type": "info",
            "title": "Clean Generation with Distribution Deficits",
            "text": f"{len(clean_developing)} countries generated over 70% of electricity from clean sources (primarily hydropower) while reaching fewer than 60% of their population with grid electricity, including {names_str}."
        })

    # 4. Long-term progression (2000 vs selected_year) - only add if fewer than 3 insights
    if selected_year > 2000 and len(insights) < 3:
        base = df[df[COL_YEAR] == 2000].set_index(COL_ENTITY)
        now = cur.set_index(COL_ENTITY)
        common = base.index.intersection(now.index)
        
        diff_elec = (now.loc[common, COL_ELEC_ACCESS] - base.loc[common, COL_ELEC_ACCESS]).dropna()
        if not diff_elec.empty:
            top_improver = diff_elec.idxmax()
            top_gain = diff_elec.max()
            insights.append({
                "type": "success",
                "title": f"Electrification Expansion (2000 to {selected_year})",
                "text": f"{top_improver} recorded the largest absolute electrification gain between 2000 and {selected_year}, expanding national coverage by {top_gain:.1f} percentage points."
            })
            
    return insights[:3]


def get_country_summary(df, country, year):
    """
    Extracts key sustainability indicators for a specific country and year.
    Returns structured dict with indicator values and status flags.
    """
    row = df[(df[COL_ENTITY] == country) & (df[COL_YEAR] == year)]
    if row.empty:
        return None
    
    r = row.iloc[0]
    
    # Helper to format float or return unavailable message
    def fmt(val, unit="%", decimals=1):
        if pd.isna(val):
            return {"val_str": "Not available", "is_available": False, "raw": None}
        return {"val_str": f"{val:.{decimals}f}{unit}", "is_available": True, "raw": float(val)}

    return {
        "entity": country,
        "year": year,
        "region": r["Region"],
        "electricity_access": fmt(r.get(COL_ELEC_ACCESS), "%"),
        "clean_cooking": fmt(r.get(COL_CLEAN_COOKING), "%"),
        "low_carbon_elec": fmt(r.get(COL_LOW_CARBON_ELEC), "%"),
        "renewable_share": fmt(r.get(COL_RENEWABLE_SHARE_TOTAL), "%"),
        "co2_emissions": fmt(r.get(COL_CO2_EMISSIONS), " kt", decimals=0),
        "gdp_per_capita": fmt(r.get(COL_GDP_PER_CAPITA), " USD", decimals=0),
        "fossil_twh": fmt(r.get(COL_FOSSIL_ELEC), " TWh", decimals=2),
        "nuclear_twh": fmt(r.get(COL_NUCLEAR_ELEC), " TWh", decimals=2),
        "renewables_twh": fmt(r.get(COL_RENEWABLES_ELEC), " TWh", decimals=2),
    }


def compute_country_changes(df, country, start_year, end_year):
    """
    Computes real historical changes for a country between two years.
    Returns dynamic observations strictly based on data differences.
    """
    sub = df[df[COL_ENTITY] == country].set_index(COL_YEAR)
    if start_year not in sub.index or end_year not in sub.index:
        return ["Insufficient data for the selected start and end years."]
    
    r_start = sub.loc[start_year]
    r_end = sub.loc[end_year]
    observations = []
    
    # Electricity Access
    e_start = r_start.get(COL_ELEC_ACCESS)
    e_end = r_end.get(COL_ELEC_ACCESS)
    if pd.notna(e_start) and pd.notna(e_end):
        diff = e_end - e_start
        direction = "increased" if diff > 0.05 else ("decreased" if diff < -0.05 else "remained steady")
        observations.append(
            f"Electricity access {direction} by {abs(diff):.1f} percentage points "
            f"(from {e_start:.1f}% in {start_year} to {e_end:.1f}% in {end_year})."
        )
    else:
        observations.append(f"Electricity access records are incomplete for {start_year} or {end_year}.")

    # Clean Cooking
    c_start = r_start.get(COL_CLEAN_COOKING)
    c_end = r_end.get(COL_CLEAN_COOKING)
    if pd.notna(c_start) and pd.notna(c_end):
        diff = c_end - c_start
        direction = "improved" if diff > 0.05 else ("declined" if diff < -0.05 else "remained flat")
        observations.append(
            f"Clean cooking access {direction} by {abs(diff):.1f} percentage points "
            f"(from {c_start:.1f}% in {start_year} to {c_end:.1f}% in {end_year})."
        )

    # Low-Carbon Electricity
    lc_start = r_start.get(COL_LOW_CARBON_ELEC)
    lc_end = r_end.get(COL_LOW_CARBON_ELEC)
    if pd.notna(lc_start) and pd.notna(lc_end):
        diff = lc_end - lc_start
        direction = "expanded" if diff > 0.1 else ("contracted" if diff < -0.1 else "remained stable")
        observations.append(
            f"Low-carbon electricity share {direction} by {abs(diff):.1f} percentage points "
            f"(from {lc_start:.1f}% in {start_year} to {lc_end:.1f}% in {end_year})."
        )

    # GDP per capita
    gdp_start = r_start.get(COL_GDP_PER_CAPITA)
    gdp_end = r_end.get(COL_GDP_PER_CAPITA)
    if pd.notna(gdp_start) and pd.notna(gdp_end) and gdp_start > 0:
        pct_growth = ((gdp_end - gdp_start) / gdp_start) * 100
        growth_dir = "grew" if pct_growth > 0 else "shrank"
        observations.append(
            f"GDP per capita {growth_dir} by {abs(pct_growth):.1f}% "
            f"(from ${gdp_start:,.0f} to ${gdp_end:,.0f})."
        )

    return observations


def calculate_decision_lab_scores(df, year, w_elec, w_lowc, w_cook):
    """
    Calculates weighted sustainability decision scores for all countries in a given year.
    Formula: S = (w1 * Elec) + (w2 * LowCarbon) + (w3 * CleanCooking)
    Weights w1, w2, w3 sum to 1.0 (normalized automatically).
    
    Missing Value Handling:
    - Excludes countries lacking any of the 3 indicators from the main ranking.
    - Transparently returns the count and list of excluded countries.
    """
    d_year = df[df[COL_YEAR] == year].copy()
    
    needed_cols = [COL_ELEC_ACCESS, COL_LOW_CARBON_ELEC, COL_CLEAN_COOKING]
    
    # Identify complete and incomplete records
    is_complete = d_year[needed_cols].notna().all(axis=1)
    complete_df = d_year[is_complete].copy()
    incomplete_df = d_year[~is_complete].copy()
    
    # Normalize weights so sum is 1.0
    total_w = w_elec + w_lowc + w_cook
    if total_w <= 0:
        w1, w2, w3 = 1/3, 1/3, 1/3
    else:
        w1 = w_elec / total_w
        w2 = w_lowc / total_w
        w3 = w_cook / total_w
        
    # Calculate score (all 3 indicators are naturally 0 to 100 percentage values)
    complete_df["Sustainability_Score"] = (
        w1 * complete_df[COL_ELEC_ACCESS] +
        w2 * complete_df[COL_LOW_CARBON_ELEC] +
        w3 * complete_df[COL_CLEAN_COOKING]
    )
    
    # Calculate ranks (rank 1 = highest score)
    complete_df["Rank"] = complete_df["Sustainability_Score"].rank(ascending=False, method="min").astype(int)
    ranked_df = complete_df.sort_values(by="Rank", ascending=True)
    
    # Excluded countries summary
    excluded_list = []
    for _, row in incomplete_df.iterrows():
        missing_indicators = [col for col in needed_cols if pd.isna(row[col])]
        excluded_list.append({
            "country": row[COL_ENTITY],
            "missing": ", ".join(missing_indicators)
        })
        
    return {
        "ranked_df": ranked_df,
        "total_countries": len(d_year),
        "ranked_count": len(ranked_df),
        "excluded_count": len(incomplete_df),
        "excluded_countries": excluded_list,
        "weights": {"electricity": w1, "low_carbon": w2, "clean_cooking": w3}
    }


def compare_scenarios(df, year, weights_a, weights_b):
    """
    Compares two weighting scenarios A and B for the same year.
    Returns merged DataFrame with Rank_A, Rank_B, Delta_Rank (Rank_A - Rank_B).
    Positive Delta means country ranked HIGHER in Scenario B than in Scenario A.
    """
    res_a = calculate_decision_lab_scores(df, year, **weights_a)
    res_b = calculate_decision_lab_scores(df, year, **weights_b)
    
    df_a = res_a["ranked_df"][[COL_ENTITY, "Sustainability_Score", "Rank", "Region"]].rename(
        columns={"Sustainability_Score": "Score_A", "Rank": "Rank_A"}
    )
    df_b = res_b["ranked_df"][[COL_ENTITY, "Sustainability_Score", "Rank"]].rename(
        columns={"Sustainability_Score": "Score_B", "Rank": "Rank_B"}
    )
    
    merged = pd.merge(df_a, df_b, on=COL_ENTITY)
    merged["Delta_Rank"] = merged["Rank_A"] - merged["Rank_B"]
    return merged, res_a, res_b
