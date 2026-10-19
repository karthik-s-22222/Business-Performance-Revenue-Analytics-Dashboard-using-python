import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ==============================================================================
# PAGE CONFIGURATION & STYLING
# ==============================================================================
st.set_page_config(
    page_title= "Business Performance & Revenue Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom injection for professional layout spacing
st.markdown("""
    <style>
    .block-container {padding-top: 1.5rem; padding-bottom: 1.5rem;}
    [data-testid="stMetricValue"] {font-size: 1.8rem; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# MOCK DATA GENERATION ENGINE
# ==============================================================================
@st.cache_data
def generate_mock_crm_data():
    np.random.seed(42)
    end_date = datetime(2026, 10, 31)
    start_date = datetime(2026, 8, 1)
    delta_days = (end_date - start_date).days
    
    # Base Timestamps
    timestamps = [start_date + timedelta(days=np.random.randint(0, delta_days)) for _ in range(500)]
    
    services = ['Private Limited Company', 'LLP Registration', 'Trademark', 'Startup India Registration', 'ISO Certification']
    sources = ['Google Ads', 'Website', 'Other', 'Just Dial']
    statuses = ['New', 'Qualified', 'Converted', 'Unqualified']
    priorities = ['High', 'Medium', 'Low']
    employees = ['Nancy Singh', 'Sneha Choudhary', 'Tannu Kumari', 'Gaurav Pant', 'Srishti Upadhyay', 'Azam Alam']

    leads_pool = []
    for i, ts in enumerate(timestamps):
        lead_id = f"LOD-{1000 + i}"
        status = np.random.choice(statuses, p=[0.20, 0.30, 0.20, 0.30])
        source = np.random.choice(sources, p=[0.70, 0.20, 0.05, 0.05])
        service = np.random.choice(services, p=[0.40, 0.25, 0.15, 0.12, 0.08])
        priority = np.random.choice(priorities, p=[0.40, 0.50, 0.10])
        emp = np.random.choice(employees)
        
        # Financial logic modeling based on service tier variables
        base_val = {"Private Limited Company": 12000, "LLP Registration": 8000, 
                    "Trademark": 4000, "Startup India Registration": 3500, "ISO Certification": 5000}[service]
        
        quoted_amt = base_val * np.random.uniform(0.9, 1.3)
        collected_amt = quoted_amt if status == 'Converted' and np.random.rand() > 0.3 else (quoted_amt * 0.4 if status == 'Converted' else 0)
        
        leads_pool.append({
            "Lead_ID": lead_id, "Timestamp": ts, "Status": status, "Source": source,
            "Service": service, "Priority": priority, "Owner": emp,
            "Quoted_Amount": round(quoted_amt, 2), "Collected_Amount": round(collected_amt, 2)
        })    
    return pd.DataFrame(leads_pool)

df_master = generate_mock_crm_data()

# ==============================================================================
# GLOBAL SIDEBAR FILTERS (Requirement 2)
# ==============================================================================
st.sidebar.title("🎛️ Control Panel")
date_preset = st.sidebar.selectbox(
    "Date Range Preset", 
    ["Today", "Last 7 Days", "Last 30 Days", "Custom Range Setting Options"], 
    index=2
)

max_date = df_master['Timestamp'].max().date()
min_date = df_master['Timestamp'].min().date()

if date_preset == "Today":
    start_curr, end_curr = max_date, max_date
elif date_preset == "Last 7 Days":
    start_curr, end_curr = max_date - timedelta(days=7), max_date
elif date_preset == "Last 30 Days":
    start_curr, end_curr = max_date - timedelta(days=30), max_date
else:
    start_curr = st.sidebar.date_input("Start Date Selector", min_date)
    end_curr = st.sidebar.date_input("End Date Selector", max_date)

# Context matching calculations for comparative periods
duration = (end_curr - start_curr).days + 1
start_prev = start_curr - timedelta(days=duration)
end_prev = start_curr - timedelta(days=1)

# Segment calculations
df_curr = df_master[(df_master['Timestamp'].dt.date >= start_curr) & (df_master['Timestamp'].dt.date <= end_curr)]
df_prev = df_master[(df_master['Timestamp'].dt.date >= start_prev) & (df_master['Timestamp'].dt.date <= end_prev)]

# Additional dropdown filters
selected_owner = st.sidebar.multiselect("Filter by Representative/User", options=df_master['Owner'].unique())
selected_service = st.sidebar.multiselect("Filter by Department/Service", options=df_master['Service'].unique())

if selected_owner:
    df_curr = df_curr[df_curr['Owner'].isin(selected_owner)]
    df_prev = df_prev[df_prev['Owner'].isin(selected_owner)]
if selected_service:
    df_curr = df_curr[df_curr['Service'].isin(selected_service)]
    df_prev = df_prev[df_prev['Service'].isin(selected_service)]

# Header display structure
st.title("📊 Business Performance & Revenue Analytics")
st.caption(f"Showing operational activity pipeline metrics from **{start_curr}** to **{end_curr}** compared against the prior period context loop.")

# ==============================================================================
# SECTION 1: LEAD ANALYTICS KPI CARDS (Requirement 1 & 2)
# ==============================================================================
def create_delta_metric(col, label, current_val, prior_val, is_percentage=False):
    if prior_val == 0:
        pct_change = 0.0
    else:
        pct_change = ((current_val - prior_val) / prior_val) * 100
    
    fmt = "{:.1f}%" if is_percentage else "{:,}"
    delta_str = f"{pct_change:+.1f}% vs prior period"
    col.metric(label=label, value=fmt.format(current_val), delta=delta_str)

col1, col2, col3, col4, col5 = st.columns(5)
create_delta_metric(col1, "Total New Leads", len(df_curr), len(df_prev))
create_delta_metric(col2, "Qualified Leads", len(df_curr[df_curr['Status'] == 'Qualified']), len(df_prev[df_prev['Status'] == 'Qualified']))
create_delta_metric(col3, "Converted Deals", len(df_curr[df_curr['Status'] == 'Converted']), len(df_prev[df_prev['Status'] == 'Converted']))
create_delta_metric(col4, "Unqualified Bounces", len(df_curr[df_curr['Status'] == 'Unqualified']), len(df_prev[df_prev['Status'] == 'Unqualified']))

curr_conv = (len(df_curr[df_curr['Status'] == 'Converted']) / len(df_curr) * 100) if len(df_curr) > 0 else 0
prev_conv = (len(df_prev[df_prev['Status'] == 'Converted']) / len(df_prev) * 100) if len(df_prev) > 0 else 0
create_delta_metric(col5, "Gross Conversion Rate", curr_conv, prev_conv, is_percentage=True)

# Visualizing distributions
st.markdown("---")
layout_col1, layout_col2 = st.columns([1, 1])

with layout_col1:
    st.subheader("🎯 Lead Conversion Funnel Progression")
    funnel_stages = ['Total Pool', 'Qualified Tracker', 'Converted Won']
    funnel_counts = [
        len(df_curr),
        len(df_curr[df_curr['Status'].isin(['Qualified', 'Converted'])]),
        len(df_curr[df_curr['Status'] == 'Converted'])
    ]
    fig_funnel = px.funnel(x=funnel_counts, y=funnel_stages, color=funnel_stages, template="plotly_white")
    st.plotly_chart(fig_funnel, use_container_width=True)

with layout_col2:
    st.subheader("🌐 Volume Capture by Lead Acquisition Source")
    source_distribution = df_curr['Source'].value_counts().reset_index()
    fig_donut = px.pie(source_distribution, values='count', names='Source', hole=0.45, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_donut, use_container_width=True)

# ==============================================================================
# SECTION 2: QUOTATION & VALUE ANALYTICS (Requirement 3 & Drill-down Views)
# ==============================================================================
st.markdown("---")
st.header("🧾 Quotation Analytics Framework")

service_summary = df_curr.groupby('Service').agg(
    Total_Quotes=('Quoted_Amount', 'count'),
    Total_Proposed_Value=('Quoted_Amount', 'sum'),
    Converted_Deals=('Status', lambda x: (x == 'Converted').sum())
).reset_index()

col_q1, col_q2 = st.columns([1, 1])

with col_q1:
    st.subheader("📈 Total Gross Valuations Split By Segment Line")
    fig_bar = px.bar(service_summary, x='Service', y='Total_Proposed_Value', color='Service', text_auto='.2s')
    st.plotly_chart(fig_bar, use_container_width=True)

with col_q2:
    st.subheader("📋 Core Service-Wise Transaction Metrics Grid Table")
    st.dataframe(service_summary, use_container_width=True, hide_index=True)

# IMPLEMENTATION OF REQ: Drill-down Interactive Selection Layer
st.subheader("🔍 Contextual Drill-Down Account Registry Audits")
chosen_service = st.selectbox("Select specific segment profile catalog to extract ledger records:", ["All Profiles"] + list(service_summary['Service'].unique()))

if chosen_service != "All Profiles":
    filtered_drilldown = df_curr[df_curr['Service'] == chosen_service]
else:
    filtered_drilldown = df_curr

st.dataframe(filtered_drilldown[['Lead_ID', 'Timestamp', 'Owner', 'Source', 'Status', 'Quoted_Amount', 'Collected_Amount']], use_container_width=True)

# ==============================================================================
# SECTION 3: DEALS & REVENUE PERFORMANCE (Requirement 4 & 5)
# ==============================================================================
st.markdown("---")
st.header("💰 Closed Deals & Strategic Revenue Health")

rev_total = df_curr['Quoted_Amount'].sum()
rev_collected = df_curr['Collected_Amount'].sum()
rev_outstanding = rev_total - rev_collected

r_col1, r_col2, r_col3 = st.columns(3)
r_col1.metric("Gross Pipeline Value Invoiced", f"₹{rev_total:,.2f}")
r_col2.metric("Liquid Capital Collections Accounted", f"₹{rev_collected:,.2f}")
r_col3.metric("Outstanding Accounts Receivables", f"₹{rev_outstanding:,.2f}", delta="- Action Required" if rev_outstanding > 0 else "Balanced")

# Daily Financial Runway Chart