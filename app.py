import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ----------------- PAGE SETUP -----------------
st.set_page_config(
    page_title="Global Malaria Analytics (DS30)",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional, premium interface
st.markdown("""
<style>
    .main {
        background-color: #f5f7f8;
    }
    .stMetric {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #003366;
    }
    .stMetric:nth-child(2) {
        border-left-color: #800000;
    }
    .stMetric:nth-child(3) {
        border-left-color: #008080;
    }
    h1, h2, h3 {
        color: #003366;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- DATA LOADING -----------------
@st.cache_data
def load_data():
    df = pd.read_csv('estimated_numbers_cleaned.csv')
    return df

df = load_data()

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.image("https://img.icons8.com/color/96/mosquito.png", width=80)
st.sidebar.title("Dashboard Controls")

# Student Details
st.sidebar.markdown("""
<div style='background-color:#f0f2f6; padding:10px; border-radius:5px; margin-bottom:15px;'>
    <h4 style='margin:0; color:#003366;'>Student Info</h4>
    <p style='margin:0; font-size:12px;'><b>Name:</b> Deus Tumusiime</p>
    <p style='margin:0; font-size:12px;'><b>Reg. No:</b> 2025/HD05/26375U</p>
    <p style='margin:0; font-size:12px;'><b>Dataset:</b> DS30 (Malaria)</p>
</div>
""", unsafe_allow_html=True)

# Year Range Slider
years = sorted(df['Year'].unique())
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=(int(min(years)), int(max(years)))
)

# WHO Region Selection
regions = sorted(df['WHO_Region'].unique())
selected_regions = st.sidebar.multiselect(
    "Select WHO Regions",
    options=regions,
    default=regions
)

# Filter Data
filtered_df = df[
    (df['Year'] >= year_range[0]) & 
    (df['Year'] <= year_range[1]) & 
    (df['WHO_Region'].isin(selected_regions))
]

# ----------------- MAIN PANEL -----------------
st.title(" Global Malaria Incidence and Deaths (2010–2017)")
st.markdown("Interactive exploration dashboard of country-level malaria estimates across WHO regions.")

# KPI Metric Cards
kpi_cols = st.columns(3)
if len(filtered_df) > 0:
    total_cases = filtered_df['No. of cases_median'].sum()
    total_deaths = filtered_df['No. of deaths_median'].sum()
    
    # Calculate estimated case fatality ratio as a percentage
    estimated_case_fatality_ratio = (
        total_deaths / total_cases * 100
        if total_cases > 0
        else 0.0
    )
    
    kpi_cols[0].metric("Total Estimated Cases", f"{total_cases/1e6:.2f} Million", help="Sum of median case estimates over selection")
    kpi_cols[1].metric("Total Estimated Deaths", f"{total_deaths/1e3:.1f} Thousand", help="Sum of median death estimates over selection")
    kpi_cols[2].metric(
        label="Estimated Case Fatality Ratio",
        value=f"{estimated_case_fatality_ratio:.2f}%",
        help="Estimated deaths as a percentage of estimated cases over the selection"
    )
else:
    st.warning("No data available with the current selection filters.")

# Tabs Layout
tabs = st.tabs([
    "Temporal & Regional Trends", 
    "Geographic Distribution", 
    "Bivariate & Correlation Analysis",
    "Filtered Data Inspector"
])

# ---- TAB 1: Trends ----
with tabs[0]:
    st.header("Global & Regional Transmission Dynamics")
    
    if len(filtered_df) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Global Temporal Trend (2010-2017)")
            temp_df = filtered_df.groupby('Year', as_index=False).agg(
                Cases=('No. of cases_median', 'sum'),
                Deaths=('No. of deaths_median', 'sum')
            )
            
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(
                x=temp_df['Year'], y=temp_df['Cases']/1e6,
                name="Cases (Millions)", line=dict(color='teal', width=3),
                mode='lines+markers'
            ))
            fig_temp.add_trace(go.Scatter(
                x=temp_df['Year'], y=temp_df['Deaths']/1e3,
                name="Deaths (Thousands)", line=dict(color='crimson', width=3),
                yaxis="y2", mode='lines+markers'
            ))
            
            fig_temp.update_layout(
                yaxis=dict(title=dict(text="Cases (Millions)", font=dict(color="teal")), tickfont=dict(color="teal")),
                yaxis2=dict(
                    title=dict(text="Deaths (Thousands)", font=dict(color="crimson")), 
                    tickfont=dict(color="crimson"), anchor="x", overlaying="y", side="right"
                ),
                legend=dict(x=0.01, y=0.99),
                margin=dict(l=40, r=40, t=30, b=40),
                height=450
            )
            st.plotly_chart(fig_temp, use_container_width=True)
            
        with col2:
            st.subheader("Regional Caseload Comparison")
            region_df = filtered_df.groupby(['Year', 'WHO_Region'], as_index=False)['No. of cases_median'].sum()
            fig_bar = px.bar(
                region_df, x="Year", y="No. of cases_median", color="WHO_Region",
                barmode="group", labels={"No. of cases_median": "Cases (Median Estimate)"},
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_bar.update_layout(
                margin=dict(l=40, r=40, t=30, b=40),
                height=450
            )
            st.plotly_chart(fig_bar, use_container_width=True)

# ---- TAB 2: Maps ----
with tabs[1]:
    st.header("Geographic Distribution of Estimated Malaria Cases")
    
    if len(filtered_df) > 0:
        available_years = sorted(filtered_df['Year'].unique())
        selected_map_year = st.selectbox("Select Map Year", options=available_years, index=len(available_years)-1)
        
        map_df = filtered_df[filtered_df['Year'] == selected_map_year]
        
        st.subheader(f"Geographic Case Burden Distribution in {selected_map_year}")
        fig_map = px.choropleth(
            map_df,
            locations="Country",
            locationmode="country names",
            color="log_cases",
            hover_name="Country",
            hover_data={"No. of cases_median": True, "No. of deaths_median": True},
            color_continuous_scale=px.colors.sequential.Plasma,
            labels={'log_cases': 'Log(Cases + 1)'}
        )
        fig_map.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular'),
            height=600,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig_map, use_container_width=True)
        st.info("The map is plotted on a logarithmic scale ($y = \\log(x+1)$) to highlight differences across regions and reveal transmission boundaries.")

# ---- TAB 3: Correlations ----
with tabs[2]:
    st.header("Epidemiological Correlation Analysis")
    
    if len(filtered_df) > 0:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Scatter Plot: Cases vs Deaths")
            log_axis = st.checkbox("Apply Logarithmic Scales (Recommended)", value=True)
            
            fig_scatter = px.scatter(
                filtered_df,
                x="No. of cases_median" if not log_axis else "log_cases",
                y="No. of deaths_median" if not log_axis else "log_deaths",
                color="WHO_Region",
                size="Case_Uncertainty_Range",
                hover_name="Country",
                hover_data=["Year"],
                labels={
                    "No. of cases_median": "Cases Median",
                    "No. of deaths_median": "Deaths Median",
                    "log_cases": "Log(Cases + 1)",
                    "log_deaths": "Log(Deaths + 1)"
                },
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            fig_scatter.update_layout(height=500, margin=dict(l=40, r=40, t=30, b=40))
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with col2:
            st.subheader("Substantive Variables Correlation")
            anal_cols = [
                'No. of cases_median', 'No. of deaths_median',
                'Case_Uncertainty_Range', 'Death_Uncertainty_Range',
                'Deaths_per_1000_Cases'
            ]
            corr_subset = filtered_df[anal_cols].dropna()
            
            if len(corr_subset) > 1:
                corr_method = st.radio("Correlation Method", options=["Pearson (Linear)", "Spearman (Monotonic)"], index=0)
                method_key = "pearson" if "Pearson" in corr_method else "spearman"
                
                corr_matrix = corr_subset.corr(method=method_key)
                
                fig_heat = px.imshow(
                    corr_matrix,
                    text_auto=".3f",
                    color_continuous_scale="RdBu",
                    zmin=-1.0, zmax=1.0,
                    labels=dict(color="Correlation"),
                    x=anal_cols, y=anal_cols
                )
                fig_heat.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig_heat, use_container_width=True)
            else:
                st.warning("Insufficient observations to compute correlation matrix.")

# ---- TAB 4: Inspector ----
with tabs[3]:
    st.header("Filtered Data Inspector")
    st.markdown("Download and inspect the subset of records corresponding to the dashboard selections.")
    
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download Button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Dataset as CSV",
        data=csv,
        file_name="malaria_filtered_data.csv",
        mime="text/csv"
    )
