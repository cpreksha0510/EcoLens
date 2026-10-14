"""
EcoLens: Energy Transition Intelligence
Main Streamlit Application

A modern sustainability analytics and decision-support dashboard exploring the
relationship between clean energy adoption, electricity access, clean cooking,
and economic development across 176 countries (2000-2020).
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import data_processing as dp

# ==============================================================================
# Page Configuration & Styling
# ==============================================================================

st.set_page_config(
    page_title="EcoLens: Energy Transition Intelligence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Cohesive Editorial Palette
PALETTE = {
    "bg": "#F7F6F0",
    "surface": "#FFFFFF",
    "primary": "#244A3A",
    "secondary": "#91A58B",
    "accent": "#C5A66A",
    "charcoal": "#292D2A",
    "muted_text": "#6B716B",
    "border": "#E5E4DC",
    "subtle_green": "#EDF2EC",
    "fossil_grey": "#5A605B"
}

# Restrained chart colorway
REGION_COLORWAY = {
    "Africa": "#91A58B",
    "Asia": "#C5A66A",
    "Europe": "#244A3A",
    "Latin America & Caribbean": "#B07D5A",
    "Northern America": "#4A6B82",
    "Oceania": "#6B8E23",
    "Other": "#8A928A"
}

SERIES_COLORS = ["#244A3A", "#91A58B", "#C5A66A", "#B07D5A", "#4A6B82", "#6B8E23"]

def apply_editorial_theme(fig, height=400):
    """Applies a clean, minimal editorial Plotly theme."""
    fig.update_layout(
        height=height,
        font=dict(family="Plus Jakarta Sans, sans-serif", color=PALETTE["charcoal"], size=11),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=35, b=35),
        xaxis=dict(
            gridcolor=PALETTE["border"],
            zerolinecolor=PALETTE["border"],
            tickfont=dict(size=10, color=PALETTE["muted_text"]),
            title_font=dict(size=11, color=PALETTE["charcoal"])
        ),
        yaxis=dict(
            gridcolor=PALETTE["border"],
            zerolinecolor=PALETTE["border"],
            tickfont=dict(size=10, color=PALETTE["muted_text"]),
            title_font=dict(size=11, color=PALETTE["charcoal"])
        ),
        legend=dict(
            font=dict(size=10, color=PALETTE["charcoal"]),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor=PALETTE["border"],
            borderwidth=1,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_size=11,
            font_family="Plus Jakarta Sans, sans-serif",
            bordercolor=PALETTE["border"]
        )
    )
    return fig


# ==============================================================================
# Data Loading (Cached)
# ==============================================================================

@st.cache_data
def get_data():
    return dp.load_dataset()

try:
    df = get_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

available_years = dp.get_available_years(df)
available_regions = dp.get_available_regions(df)


# ==============================================================================
# Compact Header & Navigation Bar
# ==============================================================================

header_col1, header_col2 = st.columns([1.5, 2])

with header_col1:
    st.markdown("""
    <div class="ecolens-brand-group">
        <span class="ecolens-brand-name">EcoLens</span>
        <span class="ecolens-brand-tagline">Sustainability Intelligence</span>
    </div>
    """, unsafe_allow_html=True)

with header_col2:
    nav_options = ["Overview", "Country Explorer", "Decision Lab"]
    if hasattr(st, "segmented_control"):
        current_page = st.segmented_control(
            "Navigation",
            options=nav_options,
            default="Overview",
            required=True,
            label_visibility="collapsed",
            key="main_nav_segment"
        )
    else:
        current_page = st.radio(
            "Navigation",
            options=nav_options,
            index=0,
            horizontal=True,
            label_visibility="collapsed",
            key="main_nav_radio"
        )

if not current_page:
    current_page = "Overview"

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)


# ==============================================================================
# PAGE 1: OVERVIEW
# ==============================================================================

if current_page == "Overview":
    # Section Heading
    f_col_yr, f_col_reg, f_col_cty = st.columns([1.2, 1.4, 1.8])
    
    with f_col_yr:
        selected_year = st.selectbox(
            "Observation Year",
            options=available_years,
            index=len(available_years) - 1, # Default: 2020 (latest)
            key="overview_year"
        )
    
    with f_col_reg:
        selected_region = st.selectbox(
            "Geographic Region",
            options=available_regions,
            index=0,
            key="overview_region"
        )

    filtered_df = dp.filter_by_year_and_region(df, selected_year, selected_region)

    with f_col_cty:
        country_options = ["All Countries"] + sorted(filtered_df[dp.COL_ENTITY].unique().tolist())
        highlight_country = st.selectbox(
            "Highlight Country",
            options=country_options,
            index=0,
            key="overview_highlight"
        )

    # Page Title with small historical indicator
    st.markdown(f"""
    <div class="ecolens-page-header">
        <h1 class="ecolens-page-title">
            Energy Transition Overview
            <span class="ecolens-status-pill">Historical Data: {selected_year}</span>
        </h1>
        <p class="ecolens-page-subtitle">
            Explore the relationship between electricity access, clean energy, and sustainable development.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 4 Compact KPI Cards
    kpis = dp.compute_overview_kpis(filtered_df)
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Countries Tracked</div>
            <div class="kpi-value">{kpis['countries_tracked']}<span class="kpi-unit">nations</span></div>
            <div class="kpi-caption">Entities in {selected_region} with valid records in {selected_year}.</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        val_str = f"{kpis['mean_elec_access']:.1f}" if kpis['mean_elec_access'] is not None else "N/A"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Average Electricity Access</div>
            <div class="kpi-value">{val_str}<span class="kpi-unit">%</span></div>
            <div class="kpi-caption">Unweighted country mean across {kpis['n_elec_valid']} observations.</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        val_str = f"{kpis['mean_low_carbon']:.1f}" if kpis['mean_low_carbon'] is not None else "N/A"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Average Low-Carbon Share</div>
            <div class="kpi-value">{val_str}<span class="kpi-unit">%</span></div>
            <div class="kpi-caption">Unweighted country mean ({kpis['n_low_carbon_valid']} valid; renewables + nuclear).</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        val_str = f"{kpis['access_gap']:.1f}" if kpis['access_gap'] is not None else "N/A"
        caption = f"Min: {kpis['min_elec_country']} | Max: {kpis['max_elec_country']}" if kpis['min_elec_country'] else "No records available."
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Electricity Access Gap</div>
            <div class="kpi-value">{val_str}<span class="kpi-unit">% pts</span></div>
            <div class="kpi-caption">{caption}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 0.65rem;'></div>", unsafe_allow_html=True)

    # Main Visualisation: Scatter Plot in White Container
    st.markdown("""
    <div class="chart-surface-card">
        <div class="chart-card-header">
            <div class="chart-card-title">Electricity Access vs. Low-Carbon Electricity Generation</div>
            <div class="chart-card-subtitle">
                Country-level distribution across access and generation decarbonization for the selected period.
            </div>
        </div>
    """, unsafe_allow_html=True)

    scatter_df = filtered_df.dropna(subset=[dp.COL_ELEC_ACCESS, dp.COL_LOW_CARBON_ELEC]).copy()
    
    # Clean hover strings
    scatter_df["Clean Cooking"] = scatter_df[dp.COL_CLEAN_COOKING].map(
        lambda x: f"{x:.1f}%" if pd.notna(x) else "Not available"
    )
    scatter_df["GDP per capita"] = scatter_df[dp.COL_GDP_PER_CAPITA].map(
        lambda x: f"${x:,.0f}" if pd.notna(x) else "Not available"
    )

    if highlight_country != "All Countries":
        scatter_df["Highlight"] = scatter_df[dp.COL_ENTITY].map(
            lambda c: "Selected Country" if c == highlight_country else "Other Countries"
        )
        color_column = "Highlight"
        color_map = {"Selected Country": "#A34E36", "Other Countries": "#91A58B"}
    else:
        color_column = "Region" if selected_region == "All Regions" else None
        color_map = REGION_COLORWAY if selected_region == "All Regions" else None

    fig_scatter = px.scatter(
        scatter_df,
        x=dp.COL_ELEC_ACCESS,
        y=dp.COL_LOW_CARBON_ELEC,
        color=color_column,
        color_discrete_map=color_map,
        hover_name=dp.COL_ENTITY,
        hover_data={
            dp.COL_ELEC_ACCESS: ":.1f%",
            dp.COL_LOW_CARBON_ELEC: ":.1f%",
            "Clean Cooking": True,
            "GDP per capita": True,
            "Region": True
        },
        labels={
            dp.COL_ELEC_ACCESS: "Electricity Access (% of population)",
            dp.COL_LOW_CARBON_ELEC: "Low-Carbon Share (% of generation)"
        }
    )

    # Quadrant dividing lines at 50%
    fig_scatter.add_vline(x=50, line_dash="dash", line_color=PALETTE["border"], opacity=0.9, line_width=1)
    fig_scatter.add_hline(y=50, line_dash="dash", line_color=PALETTE["border"], opacity=0.9, line_width=1)

    fig_scatter.update_traces(
        marker=dict(size=8, opacity=0.85, line=dict(width=0.7, color="#FFFFFF"))
    )
    apply_editorial_theme(fig_scatter, height=430)
    fig_scatter.update_layout(xaxis_range=[-2, 102], yaxis_range=[-2, 102])
    st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

    # Compact Quadrant Interpretation Strip
    st.markdown("""
        <div class="quadrant-strip">
            <div class="quadrant-cell">
                <div class="quadrant-cell-title">Advanced Transition</div>
                <div class="quadrant-cell-desc">High access (>=50%) and high low-carbon generation (>=50%). Decarbonised grids.</div>
            </div>
            <div class="quadrant-cell">
                <div class="quadrant-cell-title">Fossil Electrification</div>
                <div class="quadrant-cell-desc">High access (>=50%) but low low-carbon generation (<50%). Grids built on fossil fuels.</div>
            </div>
            <div class="quadrant-cell">
                <div class="quadrant-cell-title">Clean Off-Grid / Hydro</div>
                <div class="quadrant-cell-desc">Low access (<50%) and high low-carbon generation (>=50%). Rich hydro/renewables with distribution deficits.</div>
            </div>
            <div class="quadrant-cell">
                <div class="quadrant-cell-title">Double Energy Deficit</div>
                <div class="quadrant-cell-desc">Low access (<50%) and low low-carbon generation (<50%). Severe grid and generation shortfalls.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Concise Data-Driven Insights (Max 3)
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 0.825rem; font-weight: 700; color: #244A3A; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem;">
        Data-Driven Observations
    </div>
    """, unsafe_allow_html=True)

    insights = dp.generate_overview_insights(df, selected_year)
    ins_cols = st.columns(len(insights)) if insights else [st.container()]
    
    for idx, ins in enumerate(insights):
        with ins_cols[idx]:
            st.markdown(f"""
            <div class="insight-card {ins['type']}">
                <div class="insight-card-title">{ins['title']}</div>
                <div class="insight-card-text">{ins['text']}</div>
            </div>
            """, unsafe_allow_html=True)


# ==============================================================================
# PAGE 2: COUNTRY EXPLORER
# ==============================================================================

elif current_page == "Country Explorer":
    all_countries = dp.get_available_countries(df)
    
    # Top Control Row
    ctrl_c1, ctrl_c2, ctrl_c3 = st.columns([1.5, 1.3, 1.8])
    
    with ctrl_c1:
        default_idx = all_countries.index("India") if "India" in all_countries else 0
        primary_country = st.selectbox("Primary Country", options=all_countries, index=default_idx, key="exp_c1")
    
    with ctrl_c2:
        compare_mode = st.checkbox("Compare with Second Country", value=False)
        if compare_mode:
            compare_options = [c for c in all_countries if c != primary_country]
            default_c2_idx = compare_options.index("Brazil") if "Brazil" in compare_options else 0
            secondary_country = st.selectbox("Comparison Country", options=compare_options, index=default_c2_idx, key="exp_c2")
        else:
            secondary_country = None

    with ctrl_c3:
        year_range = st.slider("Timeframe Range", min_value=2000, max_value=2020, value=(2000, 2020))

    # Page Header
    st.markdown(f"""
    <div class="ecolens-page-header">
        <h1 class="ecolens-page-title">
            Country Analytics Explorer: {primary_country}
            <span class="ecolens-status-pill">Evaluation Year: {year_range[1]}</span>
        </h1>
        <p class="ecolens-page-subtitle">
            Longitudinal indicator trajectories, generation mixes, and national comparisons.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1_summary = dp.get_country_summary(df, primary_country, year_range[1])

    def render_metric_cards(summary, is_cmp=False):
        metrics = [
            ("Electricity Access", summary["electricity_access"]["val_str"]),
            ("Low-Carbon Share", summary["low_carbon_elec"]["val_str"]),
            ("Clean Cooking", summary["clean_cooking"]["val_str"]),
            ("Renewable Share", summary["renewable_share"]["val_str"]),
            ("GDP Per Capita", summary["gdp_per_capita"]["val_str"]),
            ("CO2 Emissions", summary["co2_emissions"]["val_str"]),
        ]
        cards = []
        for label, val in metrics:
            font_size = "0.92rem" if "Not available" in val else "1.25rem"
            val_color = PALETTE["muted_text"] if "Not available" in val else PALETTE["primary"]
            card = (
                f"<div class='country-metric-card'>"
                f"<div class='country-metric-label'>{label}</div>"
                f"<div class='country-metric-value' style='font-size: {font_size}; color: {val_color};'>{val}</div>"
                f"</div>"
            )
            cards.append(card)
        css_class = "country-metrics-grid-cmp" if is_cmp else "country-metrics-grid"
        full_html = f"<div class='{css_class}'>{''.join(cards)}</div>"
        if hasattr(st, "html"):
            st.html(full_html)
        else:
            st.markdown(full_html, unsafe_allow_html=True)

    if compare_mode and secondary_country:
        c2_summary = dp.get_country_summary(df, secondary_country, year_range[1])
        col_c1_m, col_c2_m = st.columns(2)
        
        with col_c1_m:
            st.markdown(f"<div style='font-size: 0.85rem; font-weight: 700; color: #244A3A; margin-bottom: 0.35rem;'>{primary_country} ({c1_summary['region']})</div>", unsafe_allow_html=True)
            render_metric_cards(c1_summary, is_cmp=True)

        with col_c2_m:
            st.markdown(f"<div style='font-size: 0.85rem; font-weight: 700; color: #244A3A; margin-bottom: 0.35rem;'>{secondary_country} ({c2_summary['region']})</div>", unsafe_allow_html=True)
            render_metric_cards(c2_summary, is_cmp=True)

    else:
        render_metric_cards(c1_summary, is_cmp=False)

    # Small unobtrusive data continuity notice
    if year_range[1] == 2020 and (not c1_summary["co2_emissions"]["is_available"] or not c1_summary["renewable_share"]["is_available"]):
        st.markdown("""
        <div class="info-callout">
            <strong>Data Continuity Note:</strong> In the global historical records, CO2 emissions and total final renewable energy shares
            were recorded through 2019. Consequently, 2020 displays <em>Not available</em> rather than an inaccurate zero.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Historical Trajectory Charts
    c1_hist = df[(df[dp.COL_ENTITY] == primary_country) & 
                 (df[dp.COL_YEAR] >= year_range[0]) & 
                 (df[dp.COL_YEAR] <= year_range[1])].sort_values(dp.COL_YEAR)
    
    if compare_mode and secondary_country:
        c2_hist = df[(df[dp.COL_ENTITY] == secondary_country) & 
                     (df[dp.COL_YEAR] >= year_range[0]) & 
                     (df[dp.COL_YEAR] <= year_range[1])].sort_values(dp.COL_YEAR)

    t_col1, t_col2 = st.columns(2)

    with t_col1:
        st.markdown("""
        <div class="chart-surface-card" style="margin-bottom: 0.75rem;">
            <div class="chart-card-title">Electricity Access and Clean Cooking Access (%)</div>
        """, unsafe_allow_html=True)
        
        fig_elec = go.Figure()
        fig_elec.add_trace(go.Scatter(
            x=c1_hist[dp.COL_YEAR], y=c1_hist[dp.COL_ELEC_ACCESS],
            mode="lines+markers", name=f"{primary_country}: Electricity Access",
            line=dict(color=PALETTE["primary"], width=2.5)
        ))
        fig_elec.add_trace(go.Scatter(
            x=c1_hist[dp.COL_YEAR], y=c1_hist[dp.COL_CLEAN_COOKING],
            mode="lines+markers", name=f"{primary_country}: Clean Cooking",
            line=dict(color=PALETTE["secondary"], width=2, dash="dash")
        ))
        
        if compare_mode and secondary_country:
            fig_elec.add_trace(go.Scatter(
                x=c2_hist[dp.COL_YEAR], y=c2_hist[dp.COL_ELEC_ACCESS],
                mode="lines+markers", name=f"{secondary_country}: Electricity Access",
                line=dict(color=PALETTE["accent"], width=2.5)
            ))
            fig_elec.add_trace(go.Scatter(
                x=c2_hist[dp.COL_YEAR], y=c2_hist[dp.COL_CLEAN_COOKING],
                mode="lines+markers", name=f"{secondary_country}: Clean Cooking",
                line=dict(color="#B07D5A", width=2, dash="dash")
            ))
            
        fig_elec.update_layout(
            yaxis_title="Access (% of population)",
            yaxis_range=[0, 105],
            xaxis=dict(tickmode="linear", dtick=4)
        )
        apply_editorial_theme(fig_elec, height=320)
        st.plotly_chart(fig_elec, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with t_col2:
        st.markdown("""
        <div class="chart-surface-card" style="margin-bottom: 0.75rem;">
            <div class="chart-card-title">Low-Carbon Electricity Generation Share (%)</div>
        """, unsafe_allow_html=True)

        fig_lowc = go.Figure()
        fig_lowc.add_trace(go.Scatter(
            x=c1_hist[dp.COL_YEAR], y=c1_hist[dp.COL_LOW_CARBON_ELEC],
            mode="lines+markers", name=f"{primary_country}: Low-Carbon Share",
            line=dict(color=PALETTE["primary"], width=2.5)
        ))
        if compare_mode and secondary_country:
            fig_lowc.add_trace(go.Scatter(
                x=c2_hist[dp.COL_YEAR], y=c2_hist[dp.COL_LOW_CARBON_ELEC],
                mode="lines+markers", name=f"{secondary_country}: Low-Carbon Share",
                line=dict(color=PALETTE["accent"], width=2.5)
            ))
            
        fig_lowc.update_layout(
            yaxis_title="Low-Carbon (% of generation)",
            yaxis_range=[0, 105],
            xaxis=dict(tickmode="linear", dtick=4)
        )
        apply_editorial_theme(fig_lowc, height=320)
        st.plotly_chart(fig_lowc, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Generation Mix Bar Chart
    gen_df = c1_hist[[dp.COL_YEAR, dp.COL_FOSSIL_ELEC, dp.COL_NUCLEAR_ELEC, dp.COL_RENEWABLES_ELEC]].dropna()
    if not gen_df.empty:
        st.markdown(f"""
        <div class="chart-surface-card" style="margin-bottom: 0.75rem;">
            <div class="chart-card-title">Electricity Generation Mix in {primary_country} (TWh)</div>
        """, unsafe_allow_html=True)
        
        fig_gen = go.Figure()
        fig_gen.add_trace(go.Bar(
            x=gen_df[dp.COL_YEAR], y=gen_df[dp.COL_FOSSIL_ELEC],
            name="Fossil Fuels", marker_color=PALETTE["fossil_grey"]
        ))
        fig_gen.add_trace(go.Bar(
            x=gen_df[dp.COL_YEAR], y=gen_df[dp.COL_NUCLEAR_ELEC],
            name="Nuclear", marker_color=PALETTE["accent"]
        ))
        fig_gen.add_trace(go.Bar(
            x=gen_df[dp.COL_YEAR], y=gen_df[dp.COL_RENEWABLES_ELEC],
            name="Renewables", marker_color=PALETTE["primary"]
        ))
        fig_gen.update_layout(barmode="stack", yaxis_title="Generation (TWh)")
        apply_editorial_theme(fig_gen, height=270)
        st.plotly_chart(fig_gen, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Clean Observations
    st.markdown("""
    <div style="font-size: 0.825rem; font-weight: 700; color: #244A3A; text-transform: uppercase; letter-spacing: 0.05em; margin: 0.5rem 0 0.3rem 0;">
        Historical Summary
    </div>
    """, unsafe_allow_html=True)
    
    obs_primary = dp.compute_country_changes(df, primary_country, year_range[0], year_range[1])
    for obs in obs_primary:
        st.markdown(f"<div style='font-size: 0.8rem; color: #292D2A; margin-bottom: 0.2rem;'>• {obs}</div>", unsafe_allow_html=True)

    if compare_mode and secondary_country:
        st.markdown(f"<div style='font-size: 0.825rem; font-weight: 700; color: #244A3A; text-transform: uppercase; letter-spacing: 0.05em; margin: 0.75rem 0 0.3rem 0;'>Historical Summary: {secondary_country}</div>", unsafe_allow_html=True)
        obs_sec = dp.compute_country_changes(df, secondary_country, year_range[0], year_range[1])
        for obs in obs_sec:
            st.markdown(f"<div style='font-size: 0.8rem; color: #292D2A; margin-bottom: 0.2rem;'>• {obs}</div>", unsafe_allow_html=True)


# ==============================================================================
# PAGE 3: DECISION LAB
# ==============================================================================

elif current_page == "Decision Lab":
    # Page Header
    st.markdown("""
    <div class="ecolens-page-header">
        <h1 class="ecolens-page-title">Sustainability Decision Lab</h1>
        <p class="ecolens-page-subtitle">
            Explore how different sustainability priorities change country rankings.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Methodological Disclaimer in unobtrusive panel (No emojis)
    st.markdown("""
    <div class="info-callout">
        <strong>Methodological Notice:</strong> This is an exploratory, user-defined sustainability decision model based on selected historical indicators.
        It is not an official sustainability index or predictive forecast. Rankings reflect mathematical weights applied to historical records.
    </div>
    """, unsafe_allow_html=True)

    # Compact Input Area
    ctrl_col1, ctrl_col2 = st.columns([1.5, 2.5])

    with ctrl_col1:
        scenario_preset = st.radio(
            "Priority Preset",
            options=[
                "Equal Priorities (33.3% / 33.3% / 33.4%)",
                "Access First (60% Access / 20% Clean / 20% Cooking)",
                "Clean Energy Pioneer (15% Access / 70% Clean / 15% Cooking)",
                "Health & Cooking Transition (20% Access / 20% Clean / 60% Cooking)",
                "Custom Weights"
            ],
            index=0
        )

        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            lab_year = st.selectbox(
                "Evaluation Year",
                options=available_years,
                index=len(available_years) - 1,
                key="lab_eval_year"
            )
        with sub_c2:
            lab_region = st.selectbox(
                "Filter Region",
                options=available_regions,
                index=0,
                key="lab_filter_region"
            )

    with ctrl_col2:
        if scenario_preset == "Equal Priorities (33.3% / 33.3% / 33.4%)":
            w_elec, w_lowc, w_cook = 33.3, 33.3, 33.4
            st.markdown("""
            <div style="font-size: 0.8rem; color: #6B716B; margin-top: 1.5rem;">
                Balanced allocation across basic access (33.3%), generation decarbonization (33.3%), and domestic clean cooking (33.4%).
            </div>
            """, unsafe_allow_html=True)
        elif scenario_preset == "Access First (60% Access / 20% Clean / 20% Cooking)":
            w_elec, w_lowc, w_cook = 60.0, 20.0, 20.0
            st.markdown("""
            <div style="font-size: 0.8rem; color: #6B716B; margin-top: 1.5rem;">
                Prioritizes universal grid connectivity (60%) as a foundational baseline for economic development.
            </div>
            """, unsafe_allow_html=True)
        elif scenario_preset == "Clean Energy Pioneer (15% Access / 70% Clean / 15% Cooking)":
            w_elec, w_lowc, w_cook = 15.0, 70.0, 15.0
            st.markdown("""
            <div style="font-size: 0.8rem; color: #6B716B; margin-top: 1.5rem;">
                Prioritizes low-carbon generation (70%) to evaluate rapid power sector decarbonization.
            </div>
            """, unsafe_allow_html=True)
        elif scenario_preset == "Health & Cooking Transition (20% Access / 20% Clean / 60% Cooking)":
            w_elec, w_lowc, w_cook = 20.0, 20.0, 60.0
            st.markdown("""
            <div style="font-size: 0.8rem; color: #6B716B; margin-top: 1.5rem;">
                Prioritizes eradicating indoor household biomass air pollution (60%) for public health.
            </div>
            """, unsafe_allow_html=True)
        else:
            w_elec = st.slider("Electricity Access Weight (%)", 0, 100, 40, step=5)
            w_lowc = st.slider("Low-Carbon Electricity Weight (%)", 0, 100, 30, step=5)
            w_cook = st.slider("Clean Cooking Access Weight (%)", 0, 100, 30, step=5)
            raw_sum = w_elec + w_lowc + w_cook
            if raw_sum != 100:
                st.caption(f"Weights sum to {raw_sum}%. Scores are automatically normalized to 100%.")

    # Score Calculation
    results = dp.calculate_decision_lab_scores(df, lab_year, w_elec, w_lowc, w_cook)
    ranked_df = results["ranked_df"]
    
    if lab_region != "All Regions":
        display_df = ranked_df[ranked_df["Region"] == lab_region].copy()
    else:
        display_df = ranked_df.copy()

    display_df["Display_Rank"] = range(1, len(display_df) + 1)

    # Coverage summary
    st.markdown(f"""
    <div style="font-size: 0.78rem; color: #6B716B; margin: 0.75rem 0 0.85rem 0;">
        Ranked <strong>{results['ranked_count']}</strong> of <strong>{results['total_countries']}</strong> countries in {lab_year} 
        with complete observations for all 3 dimensions. Applied weights: 
        <strong>{results['weights']['electricity']*100:.1f}%</strong> Electricity Access, 
        <strong>{results['weights']['low_carbon']*100:.1f}%</strong> Low-Carbon Share, 
        <strong>{results['weights']['clean_cooking']*100:.1f}%</strong> Clean Cooking.
    </div>
    """, unsafe_allow_html=True)

    # Top 15 Chart & Light-Themed Leaderboard Table
    bar_col, table_col = st.columns([1.5, 2.5])

    with bar_col:
        st.markdown(f"""
        <div class="chart-surface-card">
            <div class="chart-card-title">Top 15 Leading Nations</div>
            <div class="chart-card-subtitle">Composite sustainability score (0-100)</div>
        """, unsafe_allow_html=True)
        
        top_15 = display_df.head(15).copy()
        fig_bar = px.bar(
            top_15.sort_values(by="Sustainability_Score", ascending=True),
            x="Sustainability_Score",
            y=dp.COL_ENTITY,
            orientation="h",
            color="Sustainability_Score",
            color_continuous_scale=[[0, PALETTE["secondary"]], [1, PALETTE["primary"]]],
            labels={"Sustainability_Score": "Score", dp.COL_ENTITY: "Country"}
        )
        fig_bar.update_layout(xaxis_range=[0, 102], coloraxis_showscale=False)
        apply_editorial_theme(fig_bar, height=420)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with table_col:
        st.markdown("""
        <div style="font-size: 0.85rem; font-weight: 700; color: #244A3A; margin-bottom: 0.4rem;">
            Composite Score Leaderboard
        </div>
        """, unsafe_allow_html=True)

        # Generate clean HTML Table: Zero black background, No index column, Sticky header
        table_rows_html = []
        for _, r in display_df.iterrows():
            c_score = f"{r['Sustainability_Score']:.2f}"
            e_acc = f"{r[dp.COL_ELEC_ACCESS]:.1f}%" if pd.notna(r[dp.COL_ELEC_ACCESS]) else "N/A"
            l_carb = f"{r[dp.COL_LOW_CARBON_ELEC]:.1f}%" if pd.notna(r[dp.COL_LOW_CARBON_ELEC]) else "N/A"
            c_cook = f"{r[dp.COL_CLEAN_COOKING]:.1f}%" if pd.notna(r[dp.COL_CLEAN_COOKING]) else "N/A"
            
            row_html = (
                f"<tr>"
                f"<td style='font-weight: 600; width: 8%;'>{r['Display_Rank']}</td>"
                f"<td style='font-weight: 600; width: 26%;'>{r[dp.COL_ENTITY]}</td>"
                f"<td style='color: #6B716B; width: 22%;'>{r['Region']}</td>"
                f"<td class='score-cell' style='text-align: right; width: 14%;'>{c_score}</td>"
                f"<td style='text-align: right; width: 10%;'>{e_acc}</td>"
                f"<td style='text-align: right; width: 10%;'>{l_carb}</td>"
                f"<td style='text-align: right; width: 10%;'>{c_cook}</td>"
                f"</tr>"
            )
            table_rows_html.append(row_html)

        header_html = (
            "<div class='leaderboard-table-container'>"
            "<table class='leaderboard-table'>"
            "<thead><tr>"
            "<th style='width: 8%;'>Rank</th>"
            "<th style='width: 26%;'>Country</th>"
            "<th style='width: 22%;'>Region</th>"
            "<th style='text-align: right; width: 14%;'>Composite Score</th>"
            "<th style='text-align: right; width: 10%;'>Electricity</th>"
            "<th style='text-align: right; width: 10%;'>Low-Carbon</th>"
            "<th style='text-align: right; width: 10%;'>Cooking</th>"
            "</tr></thead><tbody>"
        )
        full_table_html = header_html + "".join(table_rows_html) + "</tbody></table></div>"
        
        if hasattr(st, "html"):
            st.html(full_table_html)
        else:
            st.markdown(full_table_html, unsafe_allow_html=True)

    # Excluded countries disclosure (No emojis)
    if results["excluded_count"] > 0:
        with st.expander(f"Data Disclosure: {results['excluded_count']} Countries Excluded Due to Incomplete Records"):
            st.markdown("""
            <div style="font-size: 0.78rem; color: #6B716B; margin-bottom: 0.5rem;">
                Countries lacking observations for any of the 3 dimensions are excluded from composite ranking to prevent artificial penalization.
            </div>
            """, unsafe_allow_html=True)
            ex_items = [f"• <strong>{item['country']}</strong>: Missing {item['missing']}" for item in results["excluded_countries"]]
            st.markdown("<div style='font-size: 0.78rem; color: #292D2A;'>" + "<br>".join(ex_items) + "</div>", unsafe_allow_html=True)

    # Scenario Comparison Section
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 1rem; font-weight: 700; color: #244A3A; margin-bottom: 0.15rem;">
        Scenario Sensitivity Analysis
    </div>
    <div style="font-size: 0.8rem; color: #6B716B; margin-bottom: 0.85rem;">
        Comparing country ranking movements between balanced priorities and aggressive grid decarbonization.
    </div>
    """, unsafe_allow_html=True)

    weights_a = {"w_elec": 33.3, "w_lowc": 33.3, "w_cook": 33.4}
    weights_b = {"w_elec": 15.0, "w_lowc": 70.0, "w_cook": 15.0}

    merged_cmp, r_a, r_b = dp.compare_scenarios(df, lab_year, weights_a, weights_b)

    gainers = merged_cmp.sort_values(by="Delta_Rank", ascending=False).head(5)
    decliners = merged_cmp.sort_values(by="Delta_Rank", ascending=True).head(5)

    sc_col1, sc_col2 = st.columns(2)
    with sc_col1:
        st.markdown("""
        <div class="chart-surface-card" style="margin-bottom: 0.5rem;">
            <div class="chart-card-title" style="font-size: 0.85rem; color: #244A3A;">Top Rank Climbers under Clean Energy Focus</div>
            <div class="chart-card-subtitle" style="margin-bottom: 0.4rem;">Gained most ranks when moving from Equal (33%) to Clean Pioneer (70%)</div>
        """, unsafe_allow_html=True)
        for _, r in gainers.iterrows():
            st.markdown(f"<div style='font-size: 0.8rem; color: #292D2A; margin-bottom: 0.2rem;'>• <strong>{r[dp.COL_ENTITY]}</strong>: Climbed +{int(r['Delta_Rank'])} ranks (#{int(r['Rank_A'])} to #{int(r['Rank_B'])})</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with sc_col2:
        st.markdown("""
        <div class="chart-surface-card" style="margin-bottom: 0.5rem;">
            <div class="chart-card-title" style="font-size: 0.85rem; color: #A34E36;">Top Rank Decliners under Clean Energy Focus</div>
            <div class="chart-card-subtitle" style="margin-bottom: 0.4rem;">Lost most ranks when moving from Equal (33%) to Clean Pioneer (70%)</div>
        """, unsafe_allow_html=True)
        for _, r in decliners.iterrows():
            st.markdown(f"<div style='font-size: 0.8rem; color: #292D2A; margin-bottom: 0.2rem;'>• <strong>{r[dp.COL_ENTITY]}</strong>: Dropped {int(r['Delta_Rank'])} ranks (#{int(r['Rank_A'])} to #{int(r['Rank_B'])})</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-callout" style="margin-top: 0.5rem;">
        <strong>Analytical Summary:</strong> When elevating low-carbon electricity to 70% of the score weight, 
        countries with rich hydropower or geothermal endowments (such as Central African Republic, Ethiopia, and Uganda) 
        climb substantially, despite lower overall grid connectivity. 
        Conversely, nations with universal electrification powered largely by fossil fuels (such as Singapore, Kuwait, and Bahrain) 
        experience noticeable rank drops.
    </div>
    """, unsafe_allow_html=True)
