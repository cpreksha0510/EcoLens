# EcoLens — Energy Transition Intelligence

**EcoLens** is an interactive sustainability analytics and decision-support dashboard built with **Python**, **Streamlit**, **Pandas**, and **Plotly**. It provides an editorial-grade interface to explore how 176 countries balance clean energy adoption, electricity access, clean cooking access, and economic development using historical global observations from **2000 to 2020**.

---

## 1. Project Overview

The global energy transition is characterized by a dual imperative: achieving universal energy access as a cornerstone of human development, while rapidly decarbonizing electricity generation to avert climate catastrophe.

EcoLens allows policymakers, researchers, and students to:
* **Unpack the Transition Matrix:** Explore unweighted country-level access rates against low-carbon generation across two decades.
* **Inspect Country Trajectories:** Deep dive into individual national profiles, compare country pairs side-by-side, and inspect generation breakdowns.
* **Test Policy Priorities in the Decision Lab:** Assign user-defined weights across electricity access, low-carbon electricity, and clean cooking access to evaluate how differing sustainability philosophies reshape global rankings.

---

## 2. Dataset Description

EcoLens uses the historical global dataset `global-data-on-sustainable-energy (1).csv` (also accessible via `data.csv`), covering **176 countries and territories from 2000 to 2020** (3,649 records).

### Core Indicators Used:
* **`Entity`**: Country or territory name.
* **`Year`**: Observation year (2000–2020).
* **`Access to electricity (% of population)`**: Percentage of population with access to electricity.
* **`Access to clean fuels for cooking`**: Percentage of population with primary reliance on clean fuels and technologies for cooking.
* **`Low-carbon electricity (% electricity)`**: Share of total electricity generation derived from nuclear and renewable energy sources.
* **`Electricity from fossil fuels (TWh)`**: Annual electricity generated from coal, oil, and gas.
* **`Electricity from nuclear (TWh)`**: Annual electricity generated from nuclear power.
* **`Electricity from renewables (TWh)`**: Annual electricity generated from hydro, solar, wind, geothermal, and biomass.
* **`Renewable energy share in the total final energy consumption (%)`**: Percentage of total final energy consumption derived from renewables (recorded 2000–2019).
* **`Value_co2_emissions_kt_by_country`**: Annual territorial CO2 emissions in kilotons (recorded 2000–2019).
* **`gdp_per_capita`**: Gross Domestic Product per capita in constant international dollars.

### Data Handling Principles:
* **No Artificial Zeros:** Missing observations are never silently filled with zeros.
* **Explicit Disclosures:** When an indicator is unavailable (e.g., CO2 emissions in 2020, or clean cooking in certain island territories), it is transparently reported as *"Not Recorded"*.
* **Country Averages vs. Global Aggregates:** KPI averages represent unweighted country means, clearly distinguishing them from population-weighted global statistics.

---

## 3. Installation Instructions

### Prerequisites
* Python 3.9 or higher

### Setup
1. Clone or extract the project directory:
   ```bash
   cd "path/to/mini project"
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 4. How to Run the Dashboard

Launch the Streamlit application using:
```bash
streamlit run app.py
```

The application will launch in your default web browser at `http://localhost:8501`.

---

## 5. KPI Definitions (Overview Page)

1. **Countries Tracked**:
   * *Definition*: The number of distinct sovereign nations and territories represented in the filtered dataset for the selected observation year and region.
2. **Electricity Access**:
   * *Definition*: The unweighted arithmetic mean of electricity access (% of population) across countries with valid records in the selected year.
   * *Formula*: $\frac{1}{N} \sum_{i=1}^{N} \text{Access}_i$
3. **Low-Carbon Electricity**:
   * *Definition*: The unweighted arithmetic mean of low-carbon electricity (% of total electricity generation) across countries with valid records in the selected year.
   * *Definition in Dataset*: $\frac{\text{Renewables (TWh)} + \text{Nuclear (TWh)}}{\text{Fossil (TWh)} + \text{Renewables (TWh)} + \text{Nuclear (TWh)}} \times 100$
4. **Electricity Access Gap**:
   * *Definition*: The absolute difference (in percentage points) between the highest and lowest country-level electricity access values recorded in the selected year.
   * *Formula*: $\max(\text{Access}) - \min(\text{Access})$

---

## 6. Sustainability Score Methodology (Decision Lab)

The **Decision Lab** implements a transparent, multi-criteria decision-support index allowing users to explore how varying sustainability priorities affect country rankings.

### Dimensions & Indicator Scale
Three fundamental dimensions are integrated:
1. **Electricity Access** ($I_1$): Natural 0–100% scale.
2. **Low-Carbon Electricity** ($I_2$): Natural 0–100% scale (renewables + nuclear share).
3. **Clean Cooking Access** ($I_3$): Natural 0–100% scale.

### Formula
$$S = w_1 \cdot I_1 + w_2 \cdot I_2 + w_3 \cdot I_3$$
Where weights $w_1, w_2, w_3 \in [0, 1]$ and satisfy:
$$w_1 + w_2 + w_3 = 1.0$$

### Handling Missing Indicators
Countries lacking verified observations for any of the three dimensions in the selected year are **excluded from the composite leaderboard** rather than artificially penalized with zeros. The exact count and names of excluded countries are reported transparently in an interactive disclosure panel.

### Policy Scenarios
* **Equal Priorities**: $w_1 = 33.3\%, w_2 = 33.3\%, w_3 = 33.4\%$ (Balanced baseline).
* **Access First**: $w_1 = 60.0\%, w_2 = 20.0\%, w_3 = 20.0\%$ (Human development focus).
* **Clean Energy Pioneer**: $w_1 = 15.0\%, w_2 = 70.0\%, w_3 = 15.0\%$ (Grid decarbonization focus).
* **Health & Cooking Focus**: $w_1 = 20.0\%, w_2 = 20.0\%, w_3 = 60.0\%$ (Indoor air quality and household energy focus).
* **Custom Weights**: Interactive slider inputs with automated proportional normalization.

---

## 7. Methodological Disclaimer

> **Methodological Notice:**
> The EcoLens composite sustainability score is an exploratory, user-defined decision-support model based on selected historical indicators and weights. It is not an official United Nations or World Bank sustainability index, nor is it a predictive forecast of future performance. Country scores reflect mathematical weights applied to historical records and do not label nations as objectively sustainable or unsustainable.

---

## 8. Known Limitations & Data Quality Notes

1. **Reporting Horizon**:
   * Carbon emissions (`Value_co2_emissions_kt_by_country`) and total final renewable energy share (`Renewable energy share in the total final energy consumption (%)`) are available through 2019 in the source records. Observations for 2020 are labeled *"Not Recorded"*.
2. **Small Island Developing States (SIDS)**:
   * Certain small island territories (e.g., Bermuda, Cayman Islands, Aruba) lack historical clean cooking surveys and are accordingly excluded from composite ranking in the Decision Lab.
3. **Hydro-Dominant Grids**:
   * Several developing nations possess almost 100% low-carbon electricity due to single river-basin hydroelectric plants, yet have low transmission infrastructure access. The Decision Lab's scenario comparison directly illuminates this structural tension.

---

## 9. Technology Stack

* **Language**: Python 3.9+
* **Framework**: Streamlit
* **Data Processing**: Pandas, NumPy
* **Visualizations**: Plotly Express, Plotly Graph Objects
* **Styling**: Custom editorial CSS (`assets/style.css`)
