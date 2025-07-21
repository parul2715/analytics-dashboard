import numpy as np
import datetime as datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')
import pyodbc
import pandas as pd
import streamlit as st
from itertools import combinations
from collections import Counter
import plotly.express as px
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
# theme colour


def set_dark_theme():
    st.markdown("""
        <style>
        /* 🌙 App background and base text */
        body, .stApp {
            background-color: #000000;
            color: #FFFFFF;
        }

        /* 📦 Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #1e1e1e !important;
        }

        /* 📝 Sidebar text */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] h5,
        section[data-testid="stSidebar"] h6,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div,
        div[data-baseweb="radio"] > div {
            color: #FFFFFF !important;
        }

        /* 🔘 Sidebar buttons */
        section[data-testid="stSidebar"] button {
            background-color: #999999 !important;
            color: #ffffff !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            border: none !important;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        section[data-testid="stSidebar"] button span {
            color: #ffffff !important;
            font-weight: bold !important;
        }

        /* 📌 Sidebar layout for sticky logout */
        [data-testid="stSidebar"] > div:first-child {
            display: flex;
            flex-direction: column;
            height: 100vh;
        }

        .logout-container {
            margin-top: auto;
        }
        </style>
    """, unsafe_allow_html=True)

# kpi theme

def custom_kpi(label, value, delta=None, value_color="#ffffff", delta_color="#00ff99"):
    st.markdown(f"""
        <div style="padding: 15px 20px; border-radius: 12px; background-color: #1e1e1e;
                    color: white; border: 1px solid #333; margin-bottom: 10px;">
            <div style="font-size: 14px; font-weight: 500; color: #cccccc;">{label}</div>
            <div style="font-size: 24px; font-weight: bold; color: {value_color};">{value}</div>
            {f'<div style="font-size: 12px; color: {delta_color};">{delta}</div>' if delta else ''}
        </div>
    """, unsafe_allow_html=True)

#st.set_page_config(layout="wide")
# --------------------------
# USER LOGIN CREDENTIALS
# --------------------------
Users = {
    "Bhawya": '1234',
    'Gaurav': '2345',
    'Parul': '3456'
}

# --------------------------
# LOAD DATA FROM SQL
# --------------------------
@st.cache_data
def load_data():
    engine = create_engine(st.secrets["db_url"])
    

    df_order_items = pd.read_sql("SELECT * FROM order_items", engine)
    df_order_item_refunds = pd.read_sql("SELECT * FROM order_item_refunds", engine)
    df_products = pd.read_sql("SELECT * FROM products", engine)
    df_website_sessions = pd.read_sql("SELECT * FROM website_sessions", engine)
    df_website_pageviews = pd.read_sql("SELECT * FROM website_pageviews", engine)
    df_order = pd.read_sql("SELECT * FROM orders", engine)
    return df_order_items, df_order_item_refunds, df_products, df_website_sessions, df_website_pageviews, df_order

def login_page():
    set_dark_theme()

    st.markdown("""
        <style>
        .stButton > button {
            background-color: #444;
            color: white;
            border-radius: 8px;
            padding: 0.5em 2em;
            transition: 0.3s;
            border: none;
        }

        .stButton > button:hover {
            background-color: #6c63ff;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            "<h4 style='text-align:center; color:#ccc;'>Welcome to the Analytics Dashboard</h4>",
            unsafe_allow_html=True
        )
        st.title("🔐 Login")

        # ✅ Assigning unique keys to all widgets
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        # Track if login was attempted
        if "login_attempted" not in st.session_state:
            st.session_state.login_attempted = False

        if st.button("Login", key="login_button"):
            st.session_state.login_attempted = True
            if username in Users and Users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = "intro"
                st.success("Login Successful")
                st.rerun()

        # Show error only after login attempt
        if st.session_state.login_attempted and not st.session_state.logged_in:
            st.error("Invalid Username or Password", icon="🚫")
# --------------------------
# PROJECT INTRO PAGE
# --------------------------
def project_intro():
    set_dark_theme()
    st.title("📘 Digital Analytics for E-Commerce Company")
    st.markdown("### 👨‍💻 Team Members:")
    st.markdown(" - Bhawya Kumar\n- Gaurav Nailwal\n- Parul Tiwari")

    st.markdown("""
        <style>
        div.stButton > button {
            background-color: #0099FF;
            color: white;
            font-size: 16px;
            padding: 10px 30px;
            border: none;
            border-radius: 8px;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #007ACC;
        }
        </style>
    """, unsafe_allow_html=True)

    # Functional button
    if st.button("👉 Continue to Business Context", key="to_business_context_btn"):
        st.session_state.page = "business"
        st.rerun()

# --------------------------
# BUSINESS CONTEXT PAGE
# --------------------------
def business_context():
    set_dark_theme()
    # Widen content area and style the button
    st.markdown("""
        <style>
        .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 90% !important;
        }
        div.stButton > button {
            background-color: #0099FF;
            color: white;
            font-size: 16px;
            padding: 10px 30px;
            border: none;
            border-radius: 8px;
            transition: 0.3s;
            display: inline-flex;
            white-space: nowrap;
        }
        div.stButton > button:hover {
            background-color: #007ACC;
        }
        </style>
    """, unsafe_allow_html=True)

    # Image from direct URL (centered)
    img_col1, img_col2, img_col3 = st.columns([2, 3, 1])
    with img_col2:
        st.image("https://wallpapers.com/images/hd/teddy-bear-stuffed-toys-hp6lq2r72zqgqchb.jpg", width=300)

    # Title
    st.markdown("""
        <h1 style='text-align:center; font-size:36px;'>💼 Business Context</h1>
    """, unsafe_allow_html=True)

    # Business context paragraph (wide and centered)
    text_col1, text_col2, text_col3 = st.columns([1, 6, 1])
    with text_col2:
        st.markdown("""
            <p style='text-align:justify; font-size:18px; color:#CCCCCC;'>
               A growing e-commerce startup specializing in stuffed animal toys has successfully completed 
               three years of operations. As the company continues its expansion, <strong>Cindy Sharp (CEO)</strong> is preparing 
               for the next round of funding and needs to demonstrate strong business performance supported by 
               data-driven insights.
               <br><br>
               The client aims to leverage these insights to optimize overall business performance, drive 
               successful new product launches, and enhance operational efficiency across the organization.
            </p>
        """, unsafe_allow_html=True)

    # button
    btn_col1, btn_col2, btn_col3 = st.columns([4, 2, 4])
    with btn_col2:
        if st.button("👉 Continue to Dashboard", key="continue_to_dashboard_btn"):
            st.session_state.page = "dashboard"
            st.rerun()


#def test_db_connection():
    #try:
        #engine = create_engine(st.secrets["db_url"])

        # List all tables from your PostgreSQL DB
        #tables_query = """
        #SELECT table_name
        #FROM information_schema.tables
        #WHERE table_schema='public'
        #"""
        #df_tables = pd.read_sql(tables_query, engine)

        #st.success("✅ Database connection successful!")
        #st.subheader("📋 Tables in your database:")
        #st.dataframe(df_tables)

        # Preview first table
        #if not df_tables.empty:
            #table_name = df_tables.iloc[0, 0]
            #df_preview = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5", engine)
            #st.subheader(f"📊 Preview of `{table_name}`:")
            #st.dataframe(df_preview)

    #except Exception as e:
        #st.error(f"❌ Failed to connect or query: {e}")

# --------------------------
# DASHBOARD PAGE
# --------------------------
def dashboard():
    set_dark_theme()
    #test_db_connection()

    df_order_items, df_order_item_refunds, df_products, df_website_sessions, df_website_pageviews, df_order = load_data()
    st.sidebar.title("📂 Navigation")
    selected_page = st.sidebar.radio("Go to", ["KPIs", "Traffic Analysis", "Product Analysis", "Website Performance Analysis", "Business and Seasonality analysis", "User Behavior", "Channel Portfolio Management"])



    st.sidebar.markdown("---")
    st.sidebar.title("🔍 Filters")
    df_website_sessions["created_at"] = pd.to_datetime(df_website_sessions["created_at"])
    df_website_sessions["year"] = df_website_sessions["created_at"].dt.year
    df_website_sessions["quarter"] = df_website_sessions["created_at"].dt.quarter

    df_website_pageviews["created_at"] = pd.to_datetime(df_website_pageviews["created_at"])  
    df_website_pageviews["year"] = df_website_pageviews["created_at"].dt.year
    df_website_pageviews["quarter"] = df_website_pageviews["created_at"].dt.quarter

    df_order["created_at"] = pd.to_datetime(df_order["created_at"])  
    df_order["year"] = df_order["created_at"].dt.year
    df_order["quarter"] = df_order["created_at"].dt.quarter

    df_order_items["created_at"] = pd.to_datetime(df_order_items["created_at"])
    df_order_items["year"] = df_order_items["created_at"].dt.year
    df_order_items["quarter"] = df_order_items["created_at"].dt.quarter

    df_order_item_refunds["created_at"] = pd.to_datetime(df_order_item_refunds["created_at"])
    df_order_item_refunds["year"] = df_order_item_refunds["created_at"].dt.year
    df_order_item_refunds["quarter"] = df_order_item_refunds["created_at"].dt.quarter

    df_products["created_at"] = pd.to_datetime(df_products["created_at"])
    df_products["year"] = df_products["created_at"].dt.year
    df_products["quarter"] = df_products["created_at"].dt.quarter

    years = sorted(df_website_sessions["year"].dropna().unique())
    selected_years = st.sidebar.multiselect("Year", options=years, default=years)
    
    quarters = [1, 2, 3, 4]
    selected_quarters = st.sidebar.multiselect("Quarter", options=quarters, default=quarters)


#---------------------page specific filters--------------------


    if selected_page == "User Behavior":
        
        device_types = df_website_sessions["device_type"].dropna().unique().tolist()
        selected_devices = st.sidebar.multiselect("Device Type", options=device_types, default=device_types)

        campaigns = df_website_sessions["utm_campaign"].dropna().unique().tolist()
        selected_campaigns = st.sidebar.multiselect("Campaign Type", options=campaigns, default=campaigns)

        sources = df_website_sessions["utm_source"].dropna().unique().tolist()
        selected_channels = st.sidebar.multiselect("Channel Type", options=sources, default=sources)

    elif selected_page == "Channel Portfolio Management":
        
        device_types = df_website_sessions["device_type"].dropna().unique().tolist()
        selected_devices = st.sidebar.multiselect("Device Type", options=device_types, default=device_types)

        buyer_types = ["Repeat", "One-Time"]
        selected_buyer_types = st.sidebar.multiselect("Buyer Type", options=buyer_types, default=buyer_types)

        campaigns = df_website_sessions["utm_campaign"].dropna().unique().tolist()
        selected_campaigns = st.sidebar.multiselect("Campaign Type", options=campaigns, default=campaigns)
        
    
    elif selected_page == "Traffic Analysis":

        device_types = df_website_sessions["device_type"].dropna().unique().tolist()
        selected_devices = st.sidebar.multiselect("Device Type", options=device_types, default=device_types)        

        buyer_types = ["Repeat", "One-Time"]
        selected_buyer_types = st.sidebar.multiselect("Buyer Type", options=buyer_types, default=buyer_types,
        key="traffic_buyer_type" )
          
         
    elif selected_page == "Product Analysis":

        device_types = df_website_sessions["device_type"].dropna().unique().tolist()
        selected_devices = st.sidebar.multiselect("Device Type", options=device_types, default=device_types)       

        sources = df_website_sessions["utm_source"].dropna().unique().tolist()
        selected_channels = st.sidebar.multiselect("Channel Type", options=sources, default=sources,
        key="product_channel_type")

        campaigns = df_website_sessions["utm_campaign"].dropna().unique().tolist()
        selected_campaigns = st.sidebar.multiselect("Campaign Type", options=campaigns, default=campaigns,
        key="product_campaign_type")
        


    elif selected_page == "Business and Seasonality analysis":

        device_types = df_website_sessions["device_type"].dropna().unique().tolist()
        selected_devices = st.sidebar.multiselect("Device Type", options=device_types, default=device_types,
        key="website_device_type")       

        buyer_types = ["Repeat", "One-Time"]
        selected_buyer_types = st.sidebar.multiselect("Buyer Type",options=buyer_types,default=buyer_types,
        key="website_buyer_type")             

        campaigns = df_website_sessions["utm_campaign"].dropna().unique().tolist()
        selected_campaigns = st.sidebar.multiselect("Campaign Type",options=campaigns,default=campaigns,
        key="seasonality_campaign_type")

        sources = df_website_sessions["utm_source"].dropna().unique().tolist()
        selected_channels = st.sidebar.multiselect("Channel Type",options=sources,default=sources,
        key="seasonality_channel_type")

    elif selected_page == "Website Performance Analysis":

        device_types = df_website_sessions["device_type"].dropna().unique().tolist()
        selected_devices = st.sidebar.multiselect("Device Type", options=device_types, default=device_types)

        buyer_types = ["Repeat", "One-Time"]
        selected_buyer_types = st.sidebar.multiselect("Buyer Type",options=buyer_types,default=buyer_types,
        key="website_buyer_type")

        campaigns = df_website_sessions["utm_campaign"].dropna().unique().tolist()
        selected_campaigns = st.sidebar.multiselect("Campaign Type",options=campaigns,default=campaigns,
        key="website_campaign_type")



# === PAGE-SPECIFIC DATA FILTERING ===

# Base filters (Year & Quarter)

    base_session_filter = (
        (df_website_sessions["year"].isin(selected_years)) &
        (df_website_sessions["quarter"].isin(selected_quarters))
    )
    base_pageview_filter = (
        (df_website_pageviews["year"].isin(selected_years)) &
        (df_website_pageviews["quarter"].isin(selected_quarters))
    )
    base_order_filter = (
        (df_order["year"].isin(selected_years)) &
        (df_order["quarter"].isin(selected_quarters))
    )
    base_order_item_filter = (
        (df_order_items["year"].isin(selected_years)) &
        (df_order_items["quarter"].isin(selected_quarters))
    )
    base_order_item_refunds_filter = (
        (df_order_item_refunds["year"].isin(selected_years)) &
        (df_order_item_refunds["quarter"].isin(selected_quarters))
    )
    base_products_filter = (
        (df_products["year"].isin(selected_years)) &
        (df_products["quarter"].isin(selected_quarters))
    )


# === USER BEHAVIOR PAGE ===
    if selected_page == "User Behavior":
        df_filtered = df_website_sessions[
            base_session_filter &
            (df_website_sessions["device_type"].isin(selected_devices)) &
            (df_website_sessions["utm_campaign"].isin(selected_campaigns)) &
            (df_website_sessions["utm_source"].isin(selected_channels))
        ]

        df_pageview_filtered = df_website_pageviews[base_pageview_filter]
        df_order_filtered = df_order[base_order_filter]
        df_products_filtered = df_products[base_products_filter]
        df_items_filtered = df_order_items[base_order_item_filter]
        df_refund_filtered = df_order_item_refunds[base_order_item_refunds_filter]

# === CHANNEL PORTFOLIO MANAGEMENT PAGE ===
    elif selected_page == "Channel Portfolio Management":
        df_filtered = df_website_sessions[base_session_filter].copy()

        df_filtered["buyer_type"] = df_filtered["is_repeat_session"].apply(
                lambda x: "Repeat" if x == 1 else "One-Time"
        )

        df_filtered = df_filtered[
                df_filtered["device_type"].isin(selected_devices) &
                df_filtered["buyer_type"].isin(selected_buyer_types) &
                df_filtered["utm_campaign"].isin(selected_campaigns)
        ]

        df_pageview_filtered = df_website_pageviews[base_pageview_filter]
        df_order_filtered = df_order[base_order_filter]
        df_products_filtered = df_products[base_products_filter]
        df_items_filtered = df_order_items[base_order_item_filter]
        df_refund_filtered = df_order_item_refunds[base_order_item_refunds_filter]

# === TRAFFIC ANALYSIS PAGE ===
    elif selected_page == "Traffic Analysis":
        df_filtered = df_website_sessions[base_session_filter].copy()

        df_filtered["buyer_type"] = df_filtered["is_repeat_session"].apply(lambda x: "Repeat" if x == 1 else "One-Time")

        df_filtered = df_filtered[
            (df_filtered["device_type"].isin(selected_devices)) &
            (df_filtered["buyer_type"].isin(selected_buyer_types))
        ]

        df_pageview_filtered = df_website_pageviews[base_pageview_filter]
        df_order_filtered = df_order[base_order_filter]
        df_products_filtered = df_products[base_products_filter]
        df_items_filtered = df_order_items[base_order_item_filter]
        df_refund_filtered = df_order_item_refunds[base_order_item_refunds_filter]
         
         
# ===PRODUCT ANALYSIS PAGE ====
         
    elif selected_page == "Product Analysis":
    
        df_filtered = df_website_sessions[base_session_filter]
        df_filtered = df_filtered[
            (df_filtered["device_type"].isin(selected_devices)) &
            (df_filtered["utm_campaign"].isin(selected_campaigns)) &
            (df_filtered["utm_source"].isin(selected_channels))
        ]

        filtered_session_ids = df_filtered["website_session_id"].unique()
        df_order_filtered = df_order[
            (df_order["website_session_id"].isin(filtered_session_ids)) &
            (df_order["year"].isin(selected_years)) &
            (df_order["quarter"].isin(selected_quarters))
        ]

        order_ids = df_order_filtered["order_id"].unique()
        df_items_filtered = df_order_items[df_order_items["order_id"].isin(order_ids)]
        df_refund_filtered = df_order_item_refunds[df_order_item_refunds["order_id"].isin(order_ids)]

        df_pageview_filtered = df_website_pageviews[
            (df_website_pageviews["website_session_id"].isin(filtered_session_ids)) &
            (df_website_pageviews["year"].isin(selected_years)) &
            (df_website_pageviews["quarter"].isin(selected_quarters))
        ]

        df_products_filtered = df_products[base_products_filter]
       


# === BUSINESS AND SEASONALITY PAGE ====


    elif selected_page == "Business and Seasonality analysis":
        df_filtered = df_website_sessions[base_session_filter].copy()

        df_filtered = df_filtered[
            (df_filtered["device_type"].isin(selected_devices)) &
            (df_filtered["utm_campaign"].isin(selected_campaigns)) &
            (df_filtered["utm_source"].isin(selected_channels))
        ]

        df_order_filtered = df_order[base_order_filter].copy()
        df_pageview_filtered = df_website_pageviews[base_pageview_filter]
        df_products_filtered = df_products[base_products_filter]
        df_items_filtered = df_order_items[base_order_item_filter]
        df_refund_filtered = df_order_item_refunds[base_order_item_refunds_filter]



# === WEBSITE ANALYSIS PAGE ===

    elif selected_page == "Website Performance Analysis":
        df_filtered = df_website_sessions[base_session_filter].copy()


        df_filtered["buyer_type"] = df_filtered["is_repeat_session"].apply(lambda x: "Repeat" if x == 1 else "One-Time")
        df_filtered = df_filtered[
        (df_filtered["device_type"].isin(selected_devices)) &
        (df_filtered["buyer_type"].isin(selected_buyer_types)) &
        (df_filtered["utm_campaign"].isin(selected_campaigns))
        ]

        df_pageview_filtered = df_website_pageviews[base_pageview_filter]
        df_order_filtered = df_order[base_order_filter]
        df_products_filtered = df_products[base_products_filter]
        df_items_filtered = df_order_items[base_order_item_filter]
        df_refund_filtered = df_order_item_refunds[base_order_item_refunds_filter]

# === ------ KPI'S -----  ====

    elif selected_page == "KPIs":
        df_filtered = df_website_sessions[base_session_filter]
        df_order_filtered = df_order[base_order_filter]
        df_pageview_filtered = df_website_pageviews[base_pageview_filter]
        df_products_filtered = df_products[base_products_filter]
        df_items_filtered = df_order_items[base_order_item_filter]
        df_refund_filtered = df_order_item_refunds[base_order_item_refunds_filter]



#log out button block

    st.sidebar.markdown('<div class="logout-container">', unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### 👤 Logged in as: `{st.session_state.username}`")

    if st.sidebar.button("🚪 Logout" , key="logout_button"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "login"
        st.session_state.login_attempted = False 
        st.rerun()

    st.sidebar.markdown('</div>', unsafe_allow_html=True)



#----------------------  KPI'S  ---------------------------------


    if selected_page == "KPIs":
        st.markdown(
    """
    <h1 style='text-align: center; text-decoration: underline; font-weight: bold;font-size: 51px; margin-bottom: 30px;'>
        Key Performance Indicators
    </h1>
    """,
    unsafe_allow_html=True
)
        
        
  # -------------------------------
# 📌 KPI CALCULATIONS SECTION
# -------------------------------

# TOTAL METRICS
        total_orders = df_order_filtered['order_id'].nunique()
        total_sessions = df_filtered['website_session_id'].nunique()
        total_quantities_sold = df_order_filtered['items_purchased'].sum()
        Total_Revenue = df_order_filtered['price_usd'].sum()
        Net_Revenue = df_items_filtered['price_usd'].sum() - df_refund_filtered["refund_amount_usd"].sum()
        total_cost = df_items_filtered['cogs_usd'].sum()
        profit = Net_Revenue - total_cost
        Total_Products = df_products_filtered['product_id'].count()
        Conversion_Rate = (total_orders / total_sessions) * 100
        Avg_revenue_per_order = Total_Revenue / total_orders
        Total_buyers = df_order_filtered['user_id'].nunique()
        Avg_revenue_per_buyer = Total_Revenue / Total_buyers
        avg_profit_per_buyer = profit / Total_buyers
        avg_item_per_order = total_quantities_sold / total_orders
        Total_Refund = df_refund_filtered["refund_amount_usd"].sum()
        Item_refunded_count = df_refund_filtered['order_item_refund_id'].count()
        Total_users = df_filtered['user_id'].nunique()
        Total_items = df_order_filtered['items_purchased'].sum()
        #Net cost
        final_df = df_items_filtered.merge(
                df_refund_filtered[['order_item_id', 'order_item_refund_id']],
                on='order_item_id',
                how='left')
        non_refunded_items = final_df[final_df['order_item_refund_id'].isna()]
        Net_cost = non_refunded_items['cogs_usd'].sum() / 1000


# BOUNCE RATE (Assuming it's calculated from sessions with 1 pageview)
        single_page_sessions = df_website_pageviews.groupby('website_session_id').size()
        bounce_sessions = single_page_sessions[single_page_sessions == 1].count()
        bounce_rate = (bounce_sessions / total_sessions) * 100

# USERS & BUYERS
        user_session_count = df_filtered.groupby('user_id').size().reset_index(name='session_count')
        returning_users = user_session_count[user_session_count['session_count'] > 1]['user_id'].count()
        one_time_users = user_session_count[user_session_count['session_count'] == 1]['user_id'].count()
        avg_sessions_per_user = round(user_session_count['session_count'].mean(), 2)
        avg_sessions_per_visitor = round(df_filtered.groupby('user_id').size().mean(), 2)
        pct_returning_users = (returning_users / user_session_count['user_id'].nunique()) * 100
        pct_one_time_users = (one_time_users / user_session_count['user_id'].nunique()) * 100

        user_order_count = df_order_filtered.groupby('user_id').size().reset_index(name='order_count')
        returning_buyers = user_order_count[user_order_count['order_count'] > 1]['user_id'].count()
        one_time_buyers = user_order_count[user_order_count['order_count'] == 1]['user_id'].count()
        pct_returning_buyers = (returning_buyers / Total_buyers) * 100
        pct_one_time_buyers = (one_time_buyers / Total_buyers) * 100

        pct_returned_items = (Item_refunded_count / total_quantities_sold) * 100

# Days Between First and Second Purchase
        orders_sorted = df_order_filtered.sort_values(['user_id', 'created_at'])
        first_two_orders = orders_sorted.groupby('user_id').head(2).copy()
        first_two_orders['order_rank'] = first_two_orders.groupby('user_id').cumcount() + 1
        pivot_orders = first_two_orders.pivot(index='user_id', columns='order_rank', values='created_at')
        pivot_orders.columns = ['first_order', 'second_order']
        pivot_orders = pivot_orders.dropna()
        pivot_orders['days_between'] = (pivot_orders['second_order'] - pivot_orders['first_order']).dt.days
        avg_gap = pivot_orders['days_between'].mean()

# PRODUCT SUMMARY (Revenue, Cost, Profit, Percentages)
        product_summary = df_items_filtered.groupby('product_id').agg(
                            Revenue=('price_usd', 'sum'),
                            COGS=('cogs_usd', 'sum')
                             ).reset_index()

        product_summary['Profit'] = product_summary['Revenue'] - product_summary['COGS']
        total_revenue = product_summary['Revenue'].sum()
        total_profit = product_summary['Profit'].sum()
        product_summary['Revenue %'] = (product_summary['Revenue'] / total_revenue * 100).round(2)
        product_summary['Profit %'] = (product_summary['Profit'] / total_profit * 100).round(2)

        product_summary = product_summary.merge(
               df_products_filtered[['product_id', 'product_name']], on='product_id', how='left'
               )
        product_summary = product_summary.sort_values(by='Revenue', ascending=False)[
    ['product_name', 'Revenue', 'COGS', 'Profit', 'Revenue %', 'Profit %'] ]
        product_summary.columns = ['Product Name', 'Revenue', 'COGS', 'Profit', 'Revenue %', 'Profit %']
# -------------------------------
# 📊 KPI DASHBOARD LAYOUT
# -------------------------------

           
        st.divider()

# Section 1: Core Metrics
        st.markdown("### 🔢 Core Metrics")
        row1_col1, row1_col2, row1_col3 = st.columns(3)
        with row1_col1:
            custom_kpi("🔢 Total Orders", f"{total_orders:,}")
        with row1_col2:
            custom_kpi("🌐 Total Sessions", f"{total_sessions/1_000:,.0f}K")
        with row1_col3:
            custom_kpi("📈 Total Profit", f"${profit / 1_000_000:,.2f}M")
            

        row2_col1, row2_col2, row2_col3 = st.columns(3)
        with row2_col1:
            custom_kpi("💰 Total Revenue", f"${Total_Revenue / 1_000_000:,.2f}M")
        with row2_col2:
            custom_kpi("💸 Net Revenue", f"${Net_Revenue / 1_000_000:,.2f}M")
        with row2_col3:
            custom_kpi("📉 Total Cost (COGS)", f"${total_cost / 1_000:,.2f}K")

        row3_col1, row3_col2, row3_col3 = st.columns(3)
        with row3_col1:
             custom_kpi("💸 Net Cost", f"${Net_cost:,.2f}K")
        with row3_col2:
            custom_kpi("⚡ Conversion Rate", f"{Conversion_Rate:.2f}%")
        with row3_col3:
            custom_kpi("🚪 Bounce Rate", f"{bounce_rate:.2f}%")

        row10_col1, row10_col2, row10_col3 = st.columns(3)
        with row10_col1:
                custom_kpi("📦 Total Products", f"{Total_Products}")
        with row10_col2:
                custom_kpi("🛒 Total Items", f"{Total_items:,}")
        with row10_col3:
                custom_kpi("👥 Total Buyers", f"{Total_buyers:,}")
                

# Section 2: Buyer Insights
        st.divider()
        st.markdown("### 🧑‍💼 Buyer Behavior")

        row4_col1, row4_col2, row4_col3 = st.columns(3)
        with row4_col1:
            custom_kpi("💳 Avg Revenue/Buyer", f"${Avg_revenue_per_buyer:,.2f}")
        with row4_col2:
            custom_kpi("💹 Avg Profit/Buyer", f"${avg_profit_per_buyer:,.2f}")
        with row4_col3:
            custom_kpi("🛍️ Avg Revenue/Order", f"${Avg_revenue_per_order:,.2f}")

        row5_col1, row5_col2, row5_col3 = st.columns(3)
        with row5_col1:
            custom_kpi("🧾 One-time Buyers", f"{one_time_buyers:,}")
        with row5_col2:
            custom_kpi("🔁 Returning Buyers", f"{returning_buyers:,}")
        with row5_col3:
            custom_kpi("📈 % Returning Buyers", f"{pct_returning_buyers:.2f}%")

        row6_col1, row6_col2, row6_col3 = st.columns(3)
        with row6_col1:
            custom_kpi("📉 % One-time Buyers", f"{pct_one_time_buyers:.2f}%")
        with row6_col2:
            custom_kpi("📊 Avg Items/Order", f"{avg_item_per_order:.2f}")
        with row6_col3:
            custom_kpi("⏱️ Avg Days 1st → 2nd buy", f"{avg_gap:.2f} days")


# Section 3: User Behavior
        st.divider()
        st.markdown("### 🧠 User Behavior")

        row7_col1, row7_col2, row7_col3 = st.columns(3)
        with row7_col1:
            custom_kpi("🧍 One-time Users", f"{one_time_users/1_000:,.2f}k")
        with row7_col2:
            custom_kpi("👥 Returning Users", f"{returning_users/1_000:,.2f}k")
        with row7_col3:
            custom_kpi("📈 Avg Sessions/User", f"{avg_sessions_per_user:.2f}")

        row8_col2, row8_col3 = st.columns(2)
       
        with row8_col2:
            custom_kpi("🧠 % Returning Users", f"{pct_returning_users:.2f}%")
        with row8_col3:
            custom_kpi("📉 % One-time Users", f"{pct_one_time_users:.2f}%")



# Section 4: Refunds
        st.divider()
        st.markdown("### ↩️ Refund Metrics")

        row9_col1, row9_col2, row9_col3 = st.columns(3)
        with row9_col1:
            custom_kpi("💸 Total Refund Amount", f"${Total_Refund / 1_000:,.2f}k")
        with row9_col2:
            custom_kpi("📦 Total Items Refunded", f"{Item_refunded_count:,}")
        with row9_col3:
            custom_kpi("📉 % Returned Items", f"{pct_returned_items:.2f}%")

#-----------------------TRAFFIC ANALYSI

#-----------------------TRAFFIC ANALYSIS -----------------------------------


    elif selected_page == "Traffic Analysis":
        st.markdown(
    """
    <h1 style='text-align: center; text-decoration: underline; font-weight: bold;font-size: 51px; margin-bottom: 30px;'>
        Traffic Analysis
    </h1>
    """,
    unsafe_allow_html=True
)
        
                         # 1. Traffic Sources
        
        top_traffic_sources = df_filtered.groupby('utm_source')['website_session_id'].count().reset_index().sort_values(by='website_session_id', ascending=False)
        

        st.subheader("🔝 Top Traffic Sources")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=top_traffic_sources, x='utm_source', y='website_session_id', palette='Set2', ax=ax)
        for p in ax.patches:
            height = p.get_height()
            ax.text(p.get_x() + p.get_width() / 2., height + 1, f'{height / 1_000:,.2f}K', ha='center', va='bottom', fontsize=10, color='black')
        plt.title('Top Traffic Sources')
        plt.xlabel('Source')
        plt.ylabel('Count of Sessions')
        plt.grid(False)
        st.pyplot(fig)

                            # 2.Traffic Source Trends 

        df_filtered['month'] = df_filtered['created_at'].dt.month
        traffic_trend = df_filtered.groupby([df_filtered['utm_source'],df_filtered['month']])['website_session_id'].count().reset_index()

        traffic_trend.columns = ['utm_source', 'month', 'sessions']

        st.subheader("📈 Traffic Source Trends")
        fig, ax = plt.subplots(figsize=(13, 6))
        sns.set(style='whitegrid')

        ax = sns.lineplot(
        data=traffic_trend,
        x='month',
        y='sessions',
        hue='utm_source',
        marker='o',
        palette='Set2'
         )
        for line in ax.lines:
          x_vals = line.get_xdata()
          y_vals = line.get_ydata()
    
    # Label every 2nd point
          for i in range(0, len(x_vals), 2):
            ax.text(
             x_vals[i], y_vals[i],
             f'{int(y_vals[i])}',
             color=line.get_color(),
             ha='center', va='bottom', fontsize=10
            )
        plt.title('Monthly Website Sessions by Traffic Source (All Years Combined)', fontsize=16)
        plt.xlabel('Month',fontsize = 16)
        plt.ylabel('Number of Sessions',fontsize = 16)
        plt.xticks(range(1, 13))
        plt.legend(title='Traffic Source')
        ax.grid(False)
        plt.xticks(fontsize=16)
        plt.xticks(fontsize=16)
        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)

                     
                     # 3.Bid Optimization


    # Filter only paid sessions (gsearch, bsearch)
        paid_sources = ['gsearch', 'bsearch']
        paid_sessions = df_filtered[df_filtered['utm_source'].isin(paid_sources)]

    # Merge with orders to get conversions
        paid_conversions = pd.merge(paid_sessions,
           df_order_filtered[['website_session_id', 'order_id']],
           on='website_session_id',
           how='left' )

    # Segment by source and campaign
        bid_optimization = paid_conversions.groupby(['utm_source', 'utm_campaign']).agg(
          Sessions=('website_session_id', 'count'),
          Orders=('order_id', 'nunique')
          ).reset_index()

    # Calculate CVR
        bid_optimization['CVR'] = bid_optimization['Orders'] / bid_optimization['Sessions'] * 100

    # Remove 'Other' campaigns
        bid_optimization = bid_optimization[
          bid_optimization['utm_campaign'].notna() &
          (bid_optimization['utm_campaign'].str.strip().str.lower() != 'other')
          ]

    # Sort campaigns by average CVR
        sorted_campaigns = (
          bid_optimization.groupby('utm_campaign')['CVR'].mean()
           .sort_values(ascending=False).index)

        st.subheader("🎯 Bid Optimization")

    # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
          x='utm_campaign',y='CVR',
          hue='utm_source',
          data=bid_optimization,
          order=sorted_campaigns,
          dodge=False,
          palette='Set2',
          ax=ax
          )

        ax.set_title("Brand vs Non-Brand Conversion Rate")
        ax.set_xlabel("Campaign")
        ax.set_ylabel("Conversion Rate (%)")
        ax.legend(title="Search Engine")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.grid(False)
        for container in ax.containers:
            ax.bar_label(container, fmt='%.1f%%', label_type='edge', padding=-2)
        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)
 
                     # 4. Traffic Source Segmentation

    # Classify traffic segments
        def classify_traffic(row):
            if pd.isnull(row['utm_source']) or row['utm_source'] == 'direct':
                return 'Direct'
            elif 'brand' in str(row['utm_campaign']):
                return 'Branded'
            else:
                return 'Non-Brand'

# Apply classification
        df_filtered['traffic_segment'] = df_filtered.apply(classify_traffic, axis=1)

# Count sessions per segment
        segment_counts = df_filtered['traffic_segment'].value_counts().reset_index()
        segment_counts.columns = ['traffic_segment', 'session_count']
        st.subheader("📊 Traffic Segment Distribution")
        
        fig, ax = plt.subplots(figsize=(8, 6))
        barplot = sns.barplot(
                x='traffic_segment',
                y='session_count',
                data=segment_counts,
                palette='coolwarm',
                errorbar=None  )

# Add data labels above bars
        for bar in barplot.patches:
            height = bar.get_height()
            barplot.text(
            bar.get_x() + bar.get_width() / 2,
            height + (segment_counts['session_count'].max() * 0.01),
            f"{height / 1_000_000:,.2f}M",
            ha='center',
            va='bottom',
            fontsize=12,
            color='black'
            )

        ax.set_title("Traffic Distribution by Segment")
        ax.set_xlabel("Traffic Segment")
        ax.set_ylabel("Number of Sessions")
        ax.grid(False)
        st.pyplot(fig)


        st.markdown("<br><br>", unsafe_allow_html=True)

                  # 5.Traffic Source Performing Ranking  
                  
  # Merge sessions with orders
        session_conversions = pd.merge(df_filtered,
                                       df_order_filtered[['website_session_id', 'order_id', 'price_usd']],
                                         on='website_session_id',how='left')
# Fill NA values
        session_conversions['order_id'] = session_conversions['order_id'].fillna(0)
        session_conversions['converted'] = (session_conversions['order_id'] != 0).astype(int)

# Aggregate metrics by utm_source
        traffic_ranking = session_conversions.groupby('utm_source').agg(
             Sessions=('website_session_id', 'count'),
               Converted_Sessions=('converted', 'sum'),Revenue=('price_usd', 'sum')
                                ).reset_index()

# Calculate CVR and AOV
        traffic_ranking['CVR'] = (traffic_ranking['Converted_Sessions'] / traffic_ranking['Sessions']) * 100
        traffic_ranking['AOV'] = traffic_ranking['Revenue'] / traffic_ranking['Converted_Sessions']
        traffic_ranking = traffic_ranking.sort_values(by='CVR', ascending=False)

        df_pageview_filtered = df_pageview_filtered.sort_values(by=['website_session_id', 'created_at'])
        df_pageview_filtered['pageview_order'] = df_pageview_filtered.groupby('website_session_id').cumcount() + 1

# Count total pageviews per session
        session_page_count = df_pageview_filtered.groupby('website_session_id').size().reset_index(name='pages_viewed')
# Mark bounce sessions
        session_page_count['is_bounce'] = (session_page_count['pages_viewed'] == 1).astype(int)
# Join back to sessions
        session_with_bounces = pd.merge(df_filtered[['website_session_id', 'utm_source']],
                                  session_page_count[['website_session_id', 'is_bounce']],
                                     on='website_session_id',
                                        how='left').fillna({'is_bounce': 0})

# Calculate bounce rate per source
        bounce_rate = session_with_bounces.groupby('utm_source').agg(
                      Total_Sessions=('website_session_id', 'count'),
                        Bounced_Sessions=('is_bounce', 'sum')).reset_index()

        bounce_rate['Bounce_Rate'] = (bounce_rate['Bounced_Sessions'] /
                                       bounce_rate['Total_Sessions']) * 100

# Merge conversion + revenue metrics with bounce rate
        full_analysis = pd.merge(traffic_ranking, bounce_rate[['utm_source', 'Bounce_Rate']],
                                  on='utm_source', how='left')

# Add average pages viewed per session 
        avg_pages_per_session = df_pageview_filtered.groupby('website_session_id').size().reset_index(name='page_count')
        avg_pages_per_session = pd.merge(
                        df_filtered[['website_session_id', 'utm_source']],
                          avg_pages_per_session, on='website_session_id', how='left')
        
        avg_engagement = avg_pages_per_session.groupby('utm_source')['page_count'].mean().reset_index()
        avg_engagement.rename(columns={'page_count': 'Avg_Pages_Per_Session'}, inplace=True)
# Final merge
        full_analysis = pd.merge(full_analysis, avg_engagement,
                                  on='utm_source', how='left')
        full_analysis['Avg_Pages_Per_Session'] = full_analysis['Avg_Pages_Per_Session'].fillna(1)  # Assume bounce=1 page
# Remove 'other' traffic source
        filtered_data = full_analysis[full_analysis['utm_source'].str.strip().
                                      str.lower() != 'other']  
        # Start plotting
        st.subheader("📈 Traffic Source Performance Metrics")

        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        fig.tight_layout(pad=5)

# --- CVR ---
        cvr_sorted = filtered_data.sort_values(by='CVR', ascending=False)
        sns.barplot(ax=axs[0, 0], y='CVR', x='utm_source', data=cvr_sorted, palette='Blues_d')
        axs[0, 0].set_title("Conversion Rate by Traffic Source")
        axs[0, 0].set_ylabel("Conversion Rate (%)")
        axs[0, 0].set_xlabel("Traffic Source")
        for bar in axs[0, 0].patches:
            axs[0, 0].text(bar.get_x() + bar.get_width() / 2,
                              bar.get_y() + bar.get_height() / 2,
                                   f"{bar.get_height():.1f}%",
                                     ha='center', va='center', fontsize=9, color='black')

# --- Bounce Rate ---
        bounce_sorted = filtered_data.sort_values(by='Bounce_Rate', ascending=False)
        sns.barplot(ax=axs[0, 1], y='Bounce_Rate', x='utm_source', data=bounce_sorted, palette='Reds_d')
        axs[0, 1].set_title("Bounce Rate by Traffic Source")
        axs[0, 1].set_ylabel("Bounce Rate (%)")
        axs[0, 1].set_xlabel("Traffic Source")
        for bar in axs[0, 1].patches:
         axs[0, 1].text(bar.get_x() + bar.get_width() / 2,
                         bar.get_y() + bar.get_height() / 2,f"{bar.get_height():.1f}%",
                            ha='center', va='center', fontsize=9, color='black')

# --- AOV ---
        aov_sorted = filtered_data.sort_values(by='AOV', ascending=False)
        sns.barplot(ax=axs[1, 0], y='AOV', x='utm_source', data=aov_sorted, palette='Greens_d')
        axs[1, 0].set_title("Average Order Value (AOV)")
        axs[1, 0].set_ylabel("AOV ($)")
        axs[1, 0].set_xlabel("Traffic Source")
        for bar in axs[1, 0].patches:
            axs[1, 0].text(bar.get_x() + bar.get_width() / 2,
                            bar.get_y() + bar.get_height() / 2,
                            f"${bar.get_height():.0f}",
                              ha='center', va='center', fontsize=9, color='black')

# --- Avg Pages per Session ---
        pages_sorted = filtered_data.sort_values(by='Avg_Pages_Per_Session', ascending=False)
        sns.barplot(ax=axs[1, 1], y='Avg_Pages_Per_Session', x='utm_source', data=pages_sorted, palette='Purples_d')
        axs[1, 1].set_title("Engagement: Avg Pages/Session")
        axs[1, 1].set_ylabel("Avg Pages Viewed")
        axs[1, 1].set_xlabel("Traffic Source")
        for bar in axs[1, 1].patches:
            axs[1, 1].text(bar.get_x() + bar.get_width() / 2,
                            bar.get_y() + bar.get_height() / 2,f"{bar.get_height():.2f}",
                                ha='center', va='center', fontsize=9, color='black')

        st.pyplot(fig)  

        st.markdown("<br><br>", unsafe_allow_html=True)


                    # 6. Wasteful Traffic Identification
                    
#  Merge sessions with orders ---
        session_conversions = pd.merge(df_filtered,
                                df_order_filtered[['website_session_id', 'order_id', 'price_usd']],
                                 on='website_session_id',how='left')

        session_conversions['converted'] = session_conversions['order_id'].notnull().astype(int)

#  Pageview order ---
        df_pageview_filtered = df_pageview_filtered.sort_values(by=['website_session_id', 'created_at'])
        df_pageview_filtered['pageview_order'] = df_pageview_filtered.groupby('website_session_id').cumcount() + 1

# Get landing pages 
        landing_pages = df_pageview_filtered[df_pageview_filtered['pageview_order'] == 1][['website_session_id', 'pageview_url']]
        landing_pages.rename(columns={'pageview_url': 'lander_page'}, inplace=True)
        session_conversions = pd.merge(session_conversions, landing_pages, on='website_session_id', how='left')

#  Bounce detection ---
        session_page_count = df_pageview_filtered.groupby('website_session_id').size().reset_index(name='pages_viewed')
        session_page_count['is_bounce'] = (session_page_count['pages_viewed'] == 1).astype(int)
        session_conversions = pd.merge(session_conversions,
                                  session_page_count[['website_session_id', 'is_bounce']],
                                     on='website_session_id',how='left')

        session_conversions['is_bounce'] = session_conversions['is_bounce'].fillna(0)

# Group by traffic source ---
        traffic_analysis = session_conversions.groupby('utm_source').agg(
                          Sessions=('website_session_id', 'count'),
                          Converted_Sessions=('converted', 'sum'),
                          Bounced_Sessions=('is_bounce', 'sum'),
                          Total_Revenue=('price_usd', 'sum')
                          ).reset_index()

        traffic_analysis['CVR'] = (traffic_analysis['Converted_Sessions'] / traffic_analysis['Sessions']) * 100
        traffic_analysis['Bounce_Rate'] = (traffic_analysis['Bounced_Sessions'] / traffic_analysis['Sessions']) * 100
        traffic_analysis['AOV'] = traffic_analysis['Total_Revenue'] / traffic_analysis['Converted_Sessions']
        traffic_analysis['Revenue_Per_Session'] = traffic_analysis['Total_Revenue'] / traffic_analysis['Sessions']

        traffic_analysis = traffic_analysis.sort_values(by='CVR', ascending=False)

#  Identify wasteful traffic ---
        avg_cvr = traffic_analysis['CVR'].mean()
        avg_bounce_rate = traffic_analysis['Bounce_Rate'].mean()

        traffic_analysis['Is_Wasteful'] = ((traffic_analysis['CVR'] < avg_cvr) &
                                (traffic_analysis['Bounce_Rate'] > avg_bounce_rate))

        wasteful_channels = traffic_analysis[traffic_analysis['Is_Wasteful']]

#  Streamlit section ---
        st.subheader("🚫 Wasteful Traffic Identification")

        fig, ax = plt.subplots(figsize=(12, 6))

# Conversion Rate bars
        sns.barplot(x='CVR',y='utm_source',data=traffic_analysis,color='skyblue',
                      label="Conversion Rate (%)", ax=ax)

# Bounce Rate overlay
        sns.barplot(x='Bounce_Rate',y='utm_source',data=traffic_analysis,color='salmon',
                    alpha=0.7,label="Bounce Rate (%)",ax=ax)

        ax.axvline(avg_cvr, color='blue', linestyle='--', label=f"Avg CVR ({avg_cvr:.2f}%)")
        ax.axvline(avg_bounce_rate, color='red', linestyle='--', label=f"Avg Bounce Rate ({avg_bounce_rate:.2f}%)")

        ax.set_title("Traffic Source Performance: CVR vs Bounce Rate")
        ax.set_xlabel("Rate (%)")
        ax.set_ylabel("Traffic Source")
        ax.legend()
        ax.grid(False)

        st.pyplot(fig)
        
        st.markdown("<br><br>", unsafe_allow_html=True)

# --- 8. Table output ---
        st.markdown("### ⚠️ Channels Flagged as Wasteful")
        st.dataframe(wasteful_channels[['utm_source', 'Sessions', 'CVR', 'Bounce_Rate', 'Revenue_Per_Session']]
                      .sort_values(by='CVR').reset_index(drop=True))
                                       

## --------------------PRODUCT ANALYSIS------------------

    elif selected_page == "Product Analysis":
        st.markdown(
    """
    <h1 style='text-align: center; text-decoration: underline; font-weight: bold;font-size: 51px; margin-bottom: 30px;'>
        Product Analysis
    </h1>
    """,
    unsafe_allow_html=True
)
        
        
        
#------------------Product Analysis--------------------


#---------------Top products by orders---------------------  
        
        
        sales_data = (
                df_items_filtered
                .merge(df_products_filtered[['product_id', 'product_name']], on='product_id', how='left')
                .merge(df_order_filtered[['order_id', 'items_purchased']], on='order_id', how='left')
        )

        
        st.header("📦 Product Sales Performance")


# Count unique order_ids per product
        top_products_by_orders = (
                sales_data.groupby('product_name')['order_id']
                .nunique()
                .reset_index()
                .rename(columns={'order_id': 'order_count'})
                .sort_values(by='order_count', ascending=False)
        )

        st.subheader("📦 Top Products By Order")

# Plot
        fig, ax = plt.subplots(figsize=(8, 5))  
        sns.set(style="white")

        ax = sns.barplot(
                data=top_products_by_orders,
                x='order_count',
                y='product_name',
                hue='product_name',
                palette='Purples_d',
               
        )
        #ax.legend_.remove()
        for patch in ax.patches:
                width = patch.get_width()
                y = patch.get_y() + patch.get_height() / 2
                ax.text(
                        width - 1000,  
                        y,
                        f"{width:,.0f}",
                        va='center',
                        ha='right',
                        fontsize=9,
                        color='black'
                )

        ax.set_title("Top Products by Number of Orders")
        ax.set_xlabel("Number of Orders")
        ax.set_ylabel("Product")
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)


#--------------Top products by revenue -------------------

# Group by product and revenue
        top_sales = (
                sales_data.groupby('product_name')['price_usd']
                .sum()
                .reset_index()
                .rename(columns={'price_usd': 'total_sales_usd'})
                .sort_values(by='total_sales_usd', ascending=False)
        )

        st.subheader("🧮 Top Products By Revenue")

#Plot
        fig, ax = plt.subplots(figsize=(8, 5)) 
        sns.set(style="white")

        ax = sns.barplot(
                data=top_sales,
                y='product_name',
                x='total_sales_usd',
                hue='product_name',
                palette='Blues_d',
                
        )

        formatter = FuncFormatter(lambda x, _: f'{x / 1e6:.1f}M')
        ax.xaxis.set_major_formatter(formatter)
        
        for patch in ax.patches:
                width = patch.get_width()
                y = patch.get_y() + patch.get_height() / 2
                ax.text(
                        width - (width * 0.02),  
                        y,
                        f"${width / 1e6:.2f}M",
                        va='center',
                        ha='right',
                        fontsize=9,
                        color='black'  
                )

        ax.set_title("Top Selling Products by Revenue")
        ax.set_xlabel("Total Sales (USD)")
        ax.set_ylabel("Product")
        #ax.legend_.remove()
        plt.tight_layout()

        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)

#---------------Avg price per product------------------

#Merge order_items with product info
        sales_data = df_items_filtered.merge(
                df_products[['product_id', 'product_name']],
                on='product_id',
                how='left'
        )


#Calculate Average Price per Product

        avg_price = (
                sales_data
                .groupby('product_name')['price_usd']
                .mean()
                .reset_index()
                .sort_values(by='price_usd', ascending=False)
        )

        st.subheader("💰 Average Price Per Product")


#Plot 

        fig, ax = plt.subplots(figsize=(8, 4))  
        sns.set(style="white")

        ax = sns.barplot(
                data=avg_price,
                x='price_usd',
                y='product_name',
                hue='product_name',
                palette='Purples_d',
                dodge=False,
                
        )
        #ax.legend_.remove()
        for container in ax.containers:
                ax.bar_label(
                        container,
                        labels=[f"${v:.2f}" for v in container.datavalues],
                        label_type='center',
                        padding=-2,
                        fontsize=10,
                        color='black'
                )

        ax.set_title('Average Selling Price per Product')
        ax.set_xlabel('Average Price (USD)')
        ax.set_ylabel('Product')
        plt.tight_layout()

        st.pyplot(fig)


        st.markdown("<br><br>", unsafe_allow_html=True)

# -----------monthly product sales trend---------------

# Extract month number and name 
        df_order_filtered['month_num'] = df_order_filtered['created_at'].dt.month
        df_order_filtered['month_name'] = df_order_filtered['created_at'].dt.strftime('%b')

# Merge product names
        df_order_filtered = df_order_filtered.merge(
                df_products_filtered[['product_id', 'product_name']],
                left_on='primary_product_id',
                right_on='product_id',
                how='left'
        )

# Group by month and product, sum revenue
        monthly_revenue = (
                df_order_filtered
                .groupby(['month_num', 'month_name', 'product_name'])['price_usd']
                .sum()
                .reset_index()
        )

# Sort by month number 
        monthly_revenue = monthly_revenue.sort_values('month_num')

#Pivot for plotting
        monthly_revenue_pivot = monthly_revenue.pivot(index='month_name', columns='product_name', values='price_usd').fillna(0)

#Reorder explicitly in case some months are missing
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_revenue_pivot = monthly_revenue_pivot.reindex(month_order)

# Plot
        st.subheader("📊 Monthly Revenue Trend by Product")

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.set(style="white")

        for product in monthly_revenue_pivot.columns:
                ax.plot(
                        monthly_revenue_pivot.index,
                        monthly_revenue_pivot[product],
                        marker='o',
                        label=product
                )


        ax.set_title("Monthly Revenue Trend by Product")
        ax.set_xlabel("Month")
        ax.set_ylabel("Revenue (USD)")
        plt.setp(ax.get_xticklabels(), rotation=0)
        ax.legend(title="Product")
        plt.tight_layout()
        st.pyplot(fig)


        st.divider()
        st.markdown("### 📦 Product Revenue + Profit Breakdown")

        
        # PRODUCT SUMMARY (Revenue, Cost, Profit, Percentages)
        product_summary = df_items_filtered.groupby('product_id').agg(Revenue=('price_usd', 'sum'),COGS=('cogs_usd', 'sum')).reset_index()

        product_summary['Profit'] = product_summary['Revenue'] - product_summary['COGS']
        total_revenue = product_summary['Revenue'].sum()
        total_profit = product_summary['Profit'].sum()
        product_summary['Revenue %'] = (product_summary['Revenue'] / total_revenue * 100).round(2)
        product_summary['Profit %'] = (product_summary['Profit'] / total_profit * 100).round(2)

        product_summary = product_summary.merge(
            df_products_filtered[['product_id', 'product_name']], on='product_id', how='left')

# Format Revenue, COGS, Profit as "$XM"
        for col in ['Revenue', 'COGS', 'Profit']:
             product_summary[col] = product_summary[col].apply(lambda x: f"${round(x / 1e6, 2)}M")

# Add % sign to percentage columns
        product_summary['Revenue %'] = product_summary['Revenue %'].apply(lambda x: f"{x:.2f}%")
        product_summary['Profit %'] = product_summary['Profit %'].apply(lambda x: f"{x:.2f}%")

        product_summary = product_summary.sort_values(by='Revenue', ascending=False)[['product_name', 'Revenue', 'COGS', 'Profit', 'Revenue %', 'Profit %']]
        product_summary.columns = ['Product Name', 'Revenue', 'COGS', 'Profit', 'Revenue %', 'Profit %']

        with st.expander("📦 Product Revenue + Profit Breakdown"):
             st.dataframe(product_summary, use_container_width=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)

## --------------------  Cross Sell  ----------------------------

        orders_with_products = df_items_filtered.groupby('order_id')['product_id'].apply(list).reset_index(name='product')

        def get_product_pairs(products_list):
            return list(combinations(sorted(set(products_list)), 2))  # avoid duplicates like (2,1) and (1,2)

        all_pairs = []
        for _, row in orders_with_products.iterrows():
            if len(row['product']) > 1:
                all_pairs.extend(get_product_pairs(row['product']))

        pair_counter = Counter(all_pairs)

# Convert to DataFrame 
        cross_sell_df = pd.DataFrame(pair_counter.items(), columns=['Product_Pair', 'Count'])
        cross_sell_df[['Product_ID_1', 'Product_ID_2']] = pd.DataFrame(cross_sell_df['Product_Pair'].tolist(), index=cross_sell_df.index)
        cross_sell_df.drop(columns='Product_Pair', inplace=True)
        cross_sell_df.sort_values(by='Count', ascending=False, inplace=True)

#  Map to product names
        product_lookup = df_products.set_index('product_id')['product_name'].to_dict()
        cross_sell_df['Product_Name_1'] = cross_sell_df['Product_ID_1'].map(product_lookup)
        cross_sell_df['Product_Name_2'] = cross_sell_df['Product_ID_2'].map(product_lookup)
        cross_sell_df['Pair_Label'] = cross_sell_df['Product_Name_1'] + "\n&\n" + cross_sell_df['Product_Name_2']

# Plot 
        st.subheader("🔁 Top Product Combinations (Cross-Sell)")

        fig, ax = plt.subplots(figsize=(14, 6))
        sns.barplot(x='Pair_Label',y='Count',data=cross_sell_df.head(10),
                    palette='husl',ax=ax,errorbar=None)

# Add count labels
        for bar in ax.patches:
             height = bar.get_height()
             ax.text(
        bar.get_x() + bar.get_width() / 2,
        height - 0.05 * height,  # push label slightly below the top
        f"{int(height)}",
        ha='center',
        va='top',
        fontsize=10,
        color='black'  # white text works better on colored bars
    )

# Styling
        ax.set_title("Top Product Combinations Sold Together")
        ax.set_xlabel("Product Pair")
        ax.set_ylabel("Number of Orders Containing Both Products")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='center')
        ax.grid(False)

        st.pyplot(fig)


        st.markdown("<br><br>", unsafe_allow_html=True)
# --- 5. Optional table view ---
        #with st.expander("📋 View Full Cross-Sell Table"):
            #st.dataframe(cross_sell_df[['Product_Name_1', 'Product_Name_2', 'Count']])


            #. Product Refund and Product Revenue

#  Units sold per product 
        units_sold = df_items_filtered.groupby('product_id').size().reset_index(name='Units_Sold')
        units_sold['product_id'] = units_sold['product_id'].astype(int)

# --- 2. Refund amounts per product ---
        refund_counts = pd.merge(df_refund_filtered[['order_item_id']],
                         df_items_filtered[['order_item_id', 'product_id', 'price_usd']],
                         on='order_item_id',how='inner')

        refunded_per_product = refund_counts.groupby('product_id').agg(
                               Refunded_Items=('order_item_id', 'count'),
                               Refund_Amount_Loss=('price_usd', 'sum')
                                 ).reset_index()

#  Merge with sales and product info ---
        product_refund_impact = pd.merge(units_sold, refunded_per_product, on='product_id', how='left')
        product_refund_impact.fillna({'Refunded_Items': 0, 'Refund_Amount_Loss': 0}, inplace=True)

        product_refund_impact = pd.merge(
                                 product_refund_impact,
                                 df_products[['product_id', 'product_name']],
                                 on='product_id',how='left')

# Refund Amount Loss Plot ---
        st.subheader("💸 Refund Amount Loss by Product")

        visual_data_sorted = product_refund_impact.sort_values(by='Refund_Amount_Loss', ascending=False)
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        palette = sns.color_palette("husl", n_colors=len(visual_data_sorted))

        sns.barplot(x='product_name',y='Refund_Amount_Loss',data=visual_data_sorted,
                        palette=palette,ax=ax1 )
        
        ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x/1000:.0f}k'))

        for bar in ax1.patches:
             height = bar.get_height()
             x = bar.get_x() + bar.get_width() / 2
             ax1.text(
                          x,
        height - 0.05 * height,  # position inside bar
        f"${height / 1000:.1f}k",  # format as 10.5k
        ha='center',
        va='top',
        fontsize=10,
        color='black'  
    )

        ax1.set_title("Product-Level Refund Loss ($)", fontsize=16)
        ax1.set_xlabel("Product Name")
        ax1.set_ylabel("Revenue Lost Due to Refunds ($)")
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
        ax1.grid(False)
        st.pyplot(fig1)

# Refund Rate Calculation ---
        refund_counts_simple = pd.merge(df_refund_filtered[['order_item_id']],
                                 df_items_filtered[['order_item_id', 'product_id']],
                                 on='order_item_id',how='inner' )

        refunded_per_product_simple = refund_counts_simple.groupby('product_id').size().reset_index(name='Refunded_Items')
        product_refund_rate = pd.merge(units_sold, refunded_per_product_simple, on='product_id', how='left')
        product_refund_rate.fillna({'Refunded_Items': 0}, inplace=True)
        product_refund_rate['Refund_Rate'] = (product_refund_rate['Refunded_Items'] / product_refund_rate['Units_Sold']) * 100

        product_refund_rate = pd.merge(product_refund_rate,
                                       df_products[['product_id', 'product_name']],
                                       on='product_id',how='left' )

#  Refund Rate Plot 
        st.subheader("📊 Refund Rate (%) by Product")

        top_refund_rate = product_refund_rate.sort_values(by='Refund_Rate', ascending=False).head(10)

        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='product_name',y='Refund_Rate',data=top_refund_rate,
                      palette='husl', ax=ax2, errorbar=None )

        for bar in ax2.patches:
             yval = bar.get_height()
             ax2.text(
        bar.get_x() + bar.get_width() / 2,
        yval - 0.05 * yval,  
        f"{yval:.2f}%",
        ha='center',
        va='top',
        fontsize=10,
        color='black'  
    )
        ax2.set_title("Refund Rate by Product Sold", fontsize=14)
        ax2.set_xlabel("Product Name")
        ax2.set_ylabel("Refund Rate (%)")
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
        ax2.grid(False)
        st.pyplot(fig2)
           

        st.markdown("<br><br>", unsafe_allow_html=True)

    #-------------------> New Product Launch Evaluation---------------------


        st.header("🚀 New Product Launch Evaluation")

#----------------Monthly units sold for Product 4-------------------


    # Ensure 'created_at' is datetime
        if 'created_at' in df_order_filtered.columns:
            df_order_filtered['created_at'] = pd.to_datetime(df_order_filtered['created_at'])

    #Filter Product 4 orders 
        product_4_orders = df_order_filtered[
            (df_order_filtered['primary_product_id'] == 4) &
            (df_order_filtered['created_at'] >= '2014-12-05')
        ]

    # Proceed only if there is data after filtering
        if not product_4_orders.empty:

        # perform  merge with product names
            if 'product_name' in df_products_filtered.columns:
                product_4_orders = product_4_orders.merge(
                    df_products_filtered[['product_id', 'product_name']],
                    left_on='primary_product_id',
                    right_on='product_id',
                    how='left'
                )
            else:
                st.warning("❗ 'product_name' column not found in product data.")
                product_4_orders['product_name'] = "Product 4"

        # Extract product name
            if 'product_name' in product_4_orders.columns:
                product_names = product_4_orders['product_name'].dropna().unique()
                product_4_name = product_names[0] if len(product_names) > 0 else "Product 4"
            else:
                product_4_name = "Product 4"

        # Create month column 
            product_4_orders['month'] = product_4_orders['created_at'].dt.to_period('M').astype(str)

        # Group by month to get units sold
            monthly_units = (
                product_4_orders
                .groupby('month')['items_purchased']
                .sum()
                .reset_index()
            )

        
            st.subheader(f'📆 Monthly Units Sold For {product_4_name}')

        # plot
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.set(style="white")

            ax = sns.lineplot(
                data=monthly_units,
                x='month',
                y='items_purchased',
                marker='o',
                color='steelblue'
            )

            for x, y in zip(monthly_units['month'], monthly_units['items_purchased']):
                label_y = y - 10 if str(x) == '2015-01' else y + 1
                ax.text(x, label_y, f'{int(y)}', fontsize=9, ha='center', va='bottom', rotation=45)

            ax.set_title(f'Monthly Units Sold for Product 4 : The Hudson River Mini Bear(Post Launch)')
            ax.set_xlabel('Year-Month')
            ax.set_ylabel('Units Sold')
            plt.xticks(rotation=45)
            plt.tight_layout()

            st.pyplot(fig)

        else:
            st.warning("⚠️ No data found for Product 4 after applying filters.")

            st.markdown("<br><br>", unsafe_allow_html=True)

##----------------- Monthly Revenue trend for product 4----------------



# Ensure 'created_at' is datetime
        if 'created_at' in df_order_filtered.columns:
             df_order_filtered['created_at'] = pd.to_datetime(df_order_filtered['created_at'])

# Filter Product 4 orders
        product_4_orders = df_order_filtered[
            (df_order_filtered['primary_product_id'] == 4) &
            (df_order_filtered['created_at'] >= '2014-12-05')
        ]

# Proceed only if there is data after filtering
        if not product_4_orders.empty:

    # Create 'month' column
            product_4_orders['month'] = product_4_orders['created_at'].dt.to_period('M').astype(str)

    # Group by month to get revenue
            monthly_revenue = (
            product_4_orders
            .groupby('month')['price_usd'] 
            .sum()
            .reset_index()
            )
          

            st.subheader('💰 Monthly Revenue Trend for Product 4')

    # Plot
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.set(style="white")

            ax = sns.lineplot(
                data=monthly_revenue,
                x='month',
                y='price_usd',
                marker='o',
                color='steelblue'
            )

    
            for x, y in zip(monthly_revenue['month'], monthly_revenue['price_usd']):
                if str(x) == '2015-01':
                    ax.text(x, y - 10, f'${y:,.0f}', fontsize=9, ha='center', va='top', rotation=45)
                else:
                    ax.text(x, y + 10, f'${y:,.0f}', fontsize=9, ha='center', va='bottom', rotation=45)

            ax.set_title('Monthly Revenue for Product 4: The Hudson River Mini Bear')
            ax.set_xlabel('Year-Month')
            ax.set_ylabel('Revenue USD')
            plt.xticks(rotation=45)
            plt.tight_layout()

            st.pyplot(fig)

        else:
            st.warning("⚠️ No data found for Product 4 after applying filters.")


            st.markdown("<br><br>", unsafe_allow_html=True)

## -------------------- WEBSITE PERFORMANCE ANALYSIS ----------------------------------
       

    elif selected_page == "Website Performance Analysis":
        st.markdown(
                """
                <h1 style='text-align: center; text-decoration: underline; font-weight: bold;font-size: 49px; margin-bottom: 30px;'>
        Website Performance Analysis
    </h1>
                """, unsafe_allow_html=True
        )

        df_filtered = df_website_sessions[base_session_filter].copy()
        df_filtered["buyer_type"] = df_filtered["is_repeat_session"].apply(lambda x: "Repeat" if x == 1 else "One-Time")
        df_filtered = df_filtered[
            (df_filtered["device_type"].isin(selected_devices)) &
            (df_filtered["buyer_type"].isin(selected_buyer_types)) &
            (df_filtered["utm_campaign"].isin(selected_campaigns))]
        
        filtered_session_ids = df_filtered["website_session_id"].unique()
        
        df_pageview_filtered = df_website_pageviews[
            (df_website_pageviews["website_session_id"].isin(filtered_session_ids)) &
            (df_website_pageviews["year"].isin(selected_years)) &
            (df_website_pageviews["quarter"].isin(selected_quarters))].copy()          

                 
        landing_pages = df_pageview_filtered.sort_values('created_at').groupby('website_session_id').first() 

#Count total pageviews per session
        pageview = df_pageview_filtered.groupby('website_session_id')['pageview_url'].count().reset_index(name='pageview_count') 

#Merge landing page with pageview count
        bounce = pd.merge(landing_pages,pageview, on = 'website_session_id')

# saving a new column by identifying bounce sessions
        bounce['is_bounce'] = bounce['pageview_count'] == 1

# Group by landing page and calculate bounce rate
        bounce_rate = bounce.groupby('pageview_url').agg(total_sessions = ('website_session_id','count'), bounce_sessions = ('is_bounce','sum'))

# calculating bounce %age 

        bounce_rate['percentage'] = (bounce_rate['bounce_sessions'] / bounce_rate['total_sessions']) * 100

        bounce_rate_percentage = bounce_rate.sort_values(by = 'percentage', ascending = False).reset_index()

        st.subheader("🔁 Bounce Rate by landing page")

        fig, ax = plt.subplots(figsize=(16, 10))  # Adjust size as needed

# Plot horizontal bars for all landing pages
        bars = plt.barh(bounce_rate_percentage['pageview_url'],
                bounce_rate_percentage['percentage'],
                color='deeppink')

# Add percentage labels to bars
        for bar in bars:
         width = bar.get_width()
         plt.text(
           width - 3,  # small offset to the right
           bar.get_y() + bar.get_height() / 2,
           f"{width:.2f}%",
           va='center',
           ha = 'right',
           fontsize=15,
           color='black'
        )

# Add labels and formatting
        plt.ylabel('Landing Page', fontsize=16, labelpad=10)
        plt.xlabel('Bounce Rate (%)', fontsize=16, labelpad=10)
        plt.title('Bounce Rate by Landing Page', fontsize=20, pad=20)
        plt.gca().invert_yaxis()  # Highest bounce at top
        plt.tight_layout()
        plt.grid(False)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)

                      # 2.Landing Page  Analysis

        landing_sessions = pd.merge(landing_pages, df_filtered, on='website_session_id')
        landing_orders = pd.merge(landing_sessions, df_order, on='website_session_id', how='left')

#calculating metrics per landing page 

        landing_page_analysis = landing_orders.groupby('pageview_url').agg(total_sess = ('website_session_id','count'), total_orders = ('order_id','count'), total_revenue = ('price_usd','sum'))

# calculating average order value and conversion rate percentage
        landing_page_analysis['conversion_rate_Percentage'] = (landing_page_analysis['total_orders']/landing_page_analysis['total_sess']) * 100
        landing_page_analysis['Average_order_value'] = (landing_page_analysis['total_revenue']/landing_page_analysis['total_orders'])

        final_ab_test = pd.merge(landing_page_analysis, bounce_rate_percentage, on='pageview_url')




        st.subheader("🧭 Landing Page Analysis")

# Create two columns for side-by-side charts
        col1, col2 = st.columns(2)

        with col1:
           st.markdown("#### 🧮 Conversion Rate (%)")
           sorted_conversion = final_ab_test.sort_values(by='conversion_rate_Percentage', ascending=False)
           fig1, ax1 = plt.subplots(figsize=(6, 5))
           bars1= sns.barplot(data=final_ab_test, x='pageview_url', y='conversion_rate_Percentage', color='skyblue', ax=ax1)
           ax1.bar_label(ax1.containers[0], fmt='%.2f%%', label_type='edge', fontsize=12, padding=-2)
           ax1.set_xlabel('Landing Page', fontsize=12)
           ax1.set_ylabel('Conversion Rate (%)', fontsize=12)
           ax1.tick_params(labelsize=11)
           ax1.grid(False)
           st.pyplot(fig1)
        
        with col2:
           st.markdown("#### 💵 Average Order Value")
           sorted_aov = final_ab_test.sort_values(by='Average_order_value', ascending=False)
           fig2, ax2 = plt.subplots(figsize=(6, 5))
           ax2 = sns.barplot(data=final_ab_test, x='pageview_url', y='Average_order_value', color='skyblue', ax=ax2)
           ax2.bar_label(ax2.containers[0], fmt='%.2f', label_type='edge', fontsize=12, padding=-2)
           ax2.set_xlabel('Landing Page', fontsize=12)
           ax2.set_ylabel('AOV', fontsize=12)
           ax2.tick_params(labelsize=11)
           ax2.grid(False)
           st.pyplot(fig2)

           st.markdown("<br><br>", unsafe_allow_html=True)


                         # 3. TOP 10 WEBSITE PAGES

#  Calculate Top Pages ---
        top_pages = df_pageview_filtered.groupby('pageview_url').size().reset_index(name='Total_Views')
        top_pages = top_pages.sort_values(by='Total_Views', ascending=False).head(10)

#  Visual Header 
        st.subheader("📈 Top 10 Website Pages by Views")

        #with st.expander("📋 View Table"):
            #st.dataframe(top_pages.reset_index(drop=True))

# Bar Plot 
        top_pages_sorted = top_pages.sort_values(by='Total_Views', ascending=False).reset_index(drop=True)
        colors = sns.color_palette("husl", len(top_pages_sorted))

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='pageview_url',y='Total_Views',data=top_pages_sorted,
                     palette=colors,ax=ax)

# Add labels inside bars
        for bar in ax.patches:
            height = bar.get_height()
            x = bar.get_x() + bar.get_width() / 2
            ax.text(x,height * 0.5,f"{height/1_000_000:,.2f}M",ha='center',
                    va='center',color='black',fontsize=10 )
            
        ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, _: f'{x/1_000_000:.2f}M'))

# Styling
        ax.set_title("Top Website Pages by Pageviews", fontsize=14)
        ax.set_xlabel("Page URL")
        ax.set_ylabel("Total Views")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(False)

        st.pyplot(fig)   

        st.markdown("<br><br>", unsafe_allow_html=True) 

                    
                    #4. TOP ENTRY(LANDING) PAGES
                    
# Recreate pageview_order manually
        df_pageview_filtered = df_pageview_filtered.sort_values(by=['website_session_id', 'created_at'])
        df_pageview_filtered['pageview_order'] = df_pageview_filtered.groupby('website_session_id').cumcount() + 1

# Get landing pages (first pageview per session)
        landing_pages = df_pageview_filtered[df_pageview_filtered['pageview_order'] == 1][['website_session_id', 'pageview_url']]
        landing_pages.rename(columns={'pageview_url': 'lander_page'}, inplace=True)

# Merge landing pages with orders using website_session_id
        lander_cvr = pd.merge(
                              landing_pages,
                              df_order_filtered[['website_session_id', 'price_usd']],
                              on='website_session_id',
                              how='left')

# Conversion flag
        lander_cvr['converted'] = lander_cvr['price_usd'].notnull().astype(int)

# Aggregate metrics
        cvt_by_lander = lander_cvr.groupby('lander_page').agg(
                           Sessions=('website_session_id', 'count'),
                           Orders=('converted', 'sum')
                             ).reset_index()

        cvt_by_lander['CVR'] = (cvt_by_lander['Orders'] / cvt_by_lander['Sessions']) * 100
        cvt_by_lander = cvt_by_lander[cvt_by_lander['Sessions'] >= 10]  # Optional filter to avoid low-volume noise


        
        #st.subheader("🚪 Top Landing Pages")

        #with st.expander("📋 Full Landing Page Table"):
            #st.dataframe(cvt_by_lander.sort_values(by='CVR', ascending=False).reset_index(drop=True))



#----------------- Sessions by Landing Page ---------------------

        st.markdown("### 📈 Top Landing Pages by Session Count")

        top10_sessions = cvt_by_lander.sort_values(by='Sessions', ascending=False).head(10)
        colors_sessions = sns.color_palette("husl", len(top10_sessions))

        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='lander_page', y='Sessions', data=top10_sessions, palette=colors_sessions, ax=ax2)

        for bar in ax2.patches:
            height = bar.get_height()
            x = bar.get_x() + bar.get_width() / 2
            ax2.text(x, height + (top10_sessions['Sessions'].max() * 0.01), f"{height/1_000:,.2f}K", ha='center', fontsize=10)

        ax2.get_yaxis().set_major_formatter(FuncFormatter(lambda x, _: f'{x/1_000:.0f}K'))

        ax2.set_title("Top Landing Pages by Session Volume")
        ax2.set_xlabel("Landing Page")
        ax2.set_ylabel("Sessions")
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
        ax2.grid(False)
        st.pyplot(fig2)

        st.markdown("<br><br>", unsafe_allow_html=True)

                    # 5. SESSION SEGMENTATION

 # --- Merge sessions with orders ---
        session_orders = pd.merge(df_filtered,
                           df_order_filtered[['website_session_id', 'price_usd']],
                            on='website_session_id',
                            how='left')

# Conversion flag
        session_orders['converted'] = session_orders['price_usd'].notnull().astype(int)

# --- Optional: Classify campaign types ---
        def classify_campaign(row):
            if 'brand' in str(row['utm_campaign']).lower():
                return 'Brand'
            elif 'nonbrand' in str(row['utm_campaign']).lower():
                return 'Non-Brand'
            else:
                return 'Other'

        session_orders['campaign_type'] = session_orders.apply(classify_campaign, axis=1)

# --- Group by source and device ---
        source_device_cvr = session_orders.groupby(['utm_source', 'device_type']).agg(
                                      Sessions=('website_session_id', 'count'),
                                      Conversions=('converted', 'sum')
                                       ).reset_index()

        source_device_cvr['CVR'] = (source_device_cvr['Conversions'] / source_device_cvr['Sessions']) * 100

# --- Clean data ---
        source_device_cvr = source_device_cvr[
                              source_device_cvr['utm_source'].notna() &
                              (source_device_cvr['utm_source'].str.lower().str.strip() != 'other')
                                                   ]

# --- Visualization ---
        st.subheader("💻 Session Segmentation by Traffic Source & Device")

        fig, ax = plt.subplots(figsize=(10, 6))

# Barplot with distinct hues for devices
        sns.barplot( x='utm_source',y='CVR',hue='device_type',
                      data=source_device_cvr,palette='Set2',ax=ax )

# Add data labels
        for bar in ax.patches:
            height = bar.get_height()
            if height > 0:
                ax.text(
                     bar.get_x() + bar.get_width() / 2,
                     height - 0.5,
                     f"{height:.1f}%",
                     ha='center',
                     va='bottom',
                     fontsize=9,
                     color='black' )

# Styling
        ax.set_title("Conversion Rate by Traffic Source & Device Type")
        ax.set_xlabel("Traffic Source")
        ax.set_ylabel("Conversion Rate (%)")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.grid(False)
        ax.legend(title="Device Type")

        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)


                    # 6. STEP WISE DROP ANLAYSIS

# Preprocess pageviews
        pageview = df_pageview_filtered.sort_values(by=['website_session_id', 'created_at'])
        pageview['pageview_order'] = pageview.groupby('website_session_id').cumcount() + 1

# Define funnel steps
        funnel_steps = ['/home', '/lander-1', '/products', '/the_ultimate_pricing', '/cart', '/shipping', '/billing', '/thankyou']
        funnel_pageviews = pageview[pageview['pageview_url'].isin(funnel_steps)]

# Group pageviews into full session paths
        funnel_paths = funnel_pageviews.groupby('website_session_id')['pageview_url'].apply(list).reset_index(name='path')

# Functions to check if a session reached each page
        def did_progress_to(path, target):
            return int(target in path)

# Extract step-level progression
        funnel_paths['landed_home'] = funnel_paths['path'].apply(lambda x: x[0] if len(x) > 0 else None)
        funnel_paths['visited_products'] = funnel_paths['path'].apply(did_progress_to, args=('/products',))
        funnel_paths['visited_cart'] = funnel_paths['path'].apply(did_progress_to, args=('/cart',))
        funnel_paths['visited_billing'] = funnel_paths['path'].apply(did_progress_to, args=('/billing',))
        funnel_paths['visited_thankyou'] = funnel_paths['path'].apply(did_progress_to, args=('/thankyou',))

# Stepwise user counts
        funnel_counts = [
                     ('Landing Page', funnel_paths['landed_home'].notnull().sum()),
                     ('Products Page', funnel_paths['visited_products'].sum()),
                     ('Cart Page', funnel_paths['visited_cart'].sum()),
                     ('Billing Page', funnel_paths['visited_billing'].sum()),
                     ('Thank You Page', funnel_paths['visited_thankyou'].sum())
                             ]

# Show step table
        #st.subheader("🧭 Funnel Drop-Off Table")

        #dropoff_data = []
        #for i in range(len(funnel_counts)):
            #step, count = funnel_counts[i]
            #if i == 0:
                #dropoff_data.append((step, count, "—"))   
            #else:
                #prev_count = funnel_counts[i - 1][1]
                #drop_rate = ((prev_count - count) / prev_count) * 100 if prev_count else 0
                #dropoff_data.append((step, count, f"{drop_rate:.2f}%"))

        #dropoff_df = pd.DataFrame(dropoff_data, columns=["Funnel Step", "User Count", "Drop-Off Rate"])
        #st.dataframe(dropoff_df)

# Funnel Chart
        st.subheader("📉 Funnel Progression")

        funnel_df = pd.DataFrame({
                                'step': [x[0] for x in funnel_counts],
                                'count': [x[1] for x in funnel_counts]
                                      })

        fig = px.funnel(funnel_df, x='count', y='step', title="Step-wise Funnel Progression")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

                    # 7. PAGEVIEW TREND

# 7. PAGEVIEW TREND

# Add date-based columns
        df_pageview_filtered['view_date'] = df_pageview_filtered['created_at'].dt.date
        df_pageview_filtered['view_month'] = df_pageview_filtered['created_at'].dt.strftime('%b')
        #df_pageview_filtered['month_num'] = df_pageview_filtered['created_at'].dt.month
# Filter specific top pages
        top_pages = ['/home', '/lander-1', '/products', '/cart', '/billing', '/shipping', '/thankyou']
        filtered_pageviews = df_pageview_filtered[df_pageview_filtered['pageview_url'].isin(top_pages)]

# Aggregate monthly trend
        monthly_trend = ( filtered_pageviews
                            .groupby(['view_month', 'pageview_url']).size()
                            .reset_index(name='views') )
# Define the correct month order
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Apply categorical sort on 'view_month'
        monthly_trend['view_month'] = pd.Categorical(monthly_trend['view_month'],
                                 categories=month_order,  ordered=True )

        monthly_trend = monthly_trend.sort_values('view_month').reset_index(drop=True)
# Pivot for lineplot
        pivot_df = monthly_trend.pivot(index='view_month', columns='pageview_url', values='views').fillna(0)

# Plotting
        st.subheader("📈 Monthly Pageview Trends")

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=pivot_df, ax=ax, marker='o')
        ax.set_title("Monthly Pageview Trends")
        ax.set_xlabel("Month")
        ax.set_ylabel("Number of Views")
        plt.xticks(rotation=45)
        ax.legend(title="Page URL", bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)  


#-------------------BUSINESS AND SEASONALITY----------------------------



    elif selected_page == "Business and Seasonality analysis":
        st.markdown(
    """
    <h1 style='text-align: center; text-decoration: underline; font-weight: bold;font-size: 44px; margin-bottom: 30px;'>
        Business and Seasonality Analysis
    </h1>
    """,
    unsafe_allow_html=True
)

        # Sales by Month

        df_filtered = df_website_sessions[base_session_filter].copy()
        df_filtered["buyer_type"] = df_filtered["is_repeat_session"].apply(lambda x: "Repeat" if x == 1 else "One-Time")
        df_filtered = df_filtered[
            (df_filtered["device_type"].isin(selected_devices)) &
            (df_filtered["utm_campaign"].isin(selected_campaigns)) &
            (df_filtered["utm_source"].isin(selected_channels)) &
            (df_filtered["buyer_type"].isin(selected_buyer_types))]
        
        filtered_session_ids = df_filtered["website_session_id"].unique()
        
        df_order_filtered = df_order[
            (df_order["website_session_id"].isin(filtered_session_ids)) &
            (df_order["year"].isin(selected_years)) &
            (df_order["quarter"].isin(selected_quarters))].copy()



        Monthly_Sales = df_order_filtered.groupby(df_order_filtered['created_at'].dt.strftime('%b').rename('month'))['price_usd'].sum().reset_index()
        Monthly_Sales.columns = ['month', 'sales']
        # Define the correct month order
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Apply categorical sort on 'view_month'
        Monthly_Sales['month'] = pd.Categorical(Monthly_Sales['month'],
                                 categories=month_order,  ordered=True )
        Monthly_Sales = Monthly_Sales.sort_values('month').reset_index(drop=True)


        
        st.subheader("📈 Monthly Sales")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.lineplot(data=Monthly_Sales,
                     x='month',
                     y='sales',
                     marker='o',
                     color='royalblue',)
        
        
            
        for x, y in zip(Monthly_Sales['month'], Monthly_Sales['sales']):
            
            plt.text(x, y + y * 0.01, f'{y/1_000_000:.2f}M', ha='center', fontsize=9)
            
            # Chart labels
        plt.title('Monthly Sales Trend', fontsize=16)
        plt.xlabel('Month')
        plt.ylabel('Sales (in Millions)')
        plt.grid(False)
        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)

        # orders by month
        # orders by month
        # Group by short month name and count orders

        
        df_filtered = df_website_sessions[base_session_filter].copy()
        df_filtered["buyer_type"] = df_filtered["is_repeat_session"].apply(lambda x: "Repeat" if x == 1 else "One-Time")
        df_filtered = df_filtered[
            (df_filtered["device_type"].isin(selected_devices)) &
            (df_filtered["buyer_type"].isin(selected_buyer_types)) &
            (df_filtered["utm_source"].isin(selected_channels)) &
            (df_filtered["utm_campaign"].isin(selected_campaigns))]
        
        filtered_session_ids = df_filtered["website_session_id"].unique()
        
        df_order_filtered = df_order[(df_order["website_session_id"].isin(filtered_session_ids)) &(df_order["year"].isin(selected_years)) &
                                     (df_order["quarter"].isin(selected_quarters))]

        monthly_orders = df_order_filtered.groupby(
              df_order_filtered['created_at'].dt.strftime('%b').rename('month'))['order_id'].count().reset_index()
        monthly_orders.columns = ['month', 'orders']
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_orders['month'] = pd.Categorical(monthly_orders['month'],categories=month_order,ordered=True)
        monthly_orders = monthly_orders.sort_values('month').reset_index(drop=True)
        
        st.subheader("🧾 Monthly Orders")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.set(style='whitegrid')
        ax = sns.lineplot(
            data=monthly_orders,
            x='month',
            y='orders',
            marker='o',
            color='royalblue')
        # Add data labels (only at end points to avoid clutter)
        x_data = monthly_orders['month']
        y_data = monthly_orders['orders']

        for x, y in zip(x_data, y_data):
           ax.text(x, y + y * 0.01,  
                    f'{int(y):,}',    
                    ha='center', va='bottom', fontsize=9, rotation=0)
            
            

# Chart labels
        plt.title('Monthly Order Trend', fontsize=16)
        plt.xlabel('Month')
        plt.ylabel('Order Count')
        plt.xticks(rotation=45)
        plt.grid(False)
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)
# Sales by Weekend vs Weekday
        sales_by_daytype = df_order_filtered.groupby(df_order_filtered['created_at'].dt.weekday.apply(lambda x: 'weekend' if x >=5 else 'weekday'))['price_usd'].sum().reset_index()
        sales_by_daytype.columns = ['DayType', 'Sales']
        
        st.subheader("🗓️ Weekday vs Weekend Sales ")
        fig, ax = plt.subplots(figsize=(8,6))
        bars = plt.bar(sales_by_daytype['DayType'], sales_by_daytype['Sales'], color=['skyblue', 'lightcoral'])
        
        ax.ticklabel_format(style='plain', axis='y')
        yticks = ax.get_yticks()  # Get current y-axis tick positions
        ax.set_yticklabels([f"{y / 1_000_000:.1f}M" for y in yticks], fontsize=10)
        # Add data labels
        for bar in bars:
            yval = bar.get_height()
            label = f"${yval / 1_000_000:.1f}M"
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01*yval, label, ha='center', va='bottom', fontsize=8)
        plt.title('Sales by Weekend vs Weekday')
        plt.ylabel('Total Sales (USD)')
        plt.xlabel('Day Type')
        plt.grid(False)
        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)


# Sessions by Hour of Day
        hourly_sessions = df_filtered.groupby(df_filtered['created_at'].dt.hour)['website_session_id'].count().reset_index(name = 'Number of Sessions')

        st.subheader("🕒 Sessions by Hour of Day")
        fig, ax = plt.subplots(figsize=(14, 8))
        bars = plt.bar(hourly_sessions['created_at'], hourly_sessions['Number of Sessions'],width=0.4, color='mediumseagreen')
        for bar in bars:
            yval = bar.get_height()
            label = f"${yval/1_000:.2f}K"
            plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{yval/1_000:.1f}K", ha='center', va='bottom', fontsize=12)
        plt.title('Website Sessions by Hour of Day', fontsize = 16)
        plt.xlabel('Hour of Day (0–23)', fontsize = 16)
        plt.ylabel('Number of Sessions( in Thousands)', fontsize = 16)
        plt.xticks(range(0, 24))  # Show all 24 hours
        plt.grid(False)  # Remove grid lines
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)

# Avg Revenue per Day
        average_revenue_day = df_order_filtered.groupby(df_order_filtered['created_at'].dt.day_name())['price_usd'].mean().reset_index(name = 'Average Revenue')
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        average_revenue_day['created_at'] = pd.Categorical(average_revenue_day['created_at'], categories=day_order)
        average_revenue_day = average_revenue_day.sort_values('created_at').reset_index(drop=True)
        
        st.subheader("💰 Average Revenue Per Day")
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = plt.bar(average_revenue_day['created_at'], average_revenue_day['Average Revenue'], width=0.5, color='cornflowerblue')
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f"${yval:,.2f}", ha='center', va='bottom', fontsize=9)
            
        plt.title('Average Revenue by Day of the Week')
        plt.xlabel('Day of the Week')
        plt.ylabel('Average Revenue (USD)')
        plt.grid(False)
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Peak Session Day
        peak_session_day = df_filtered.groupby(df_website_sessions['created_at'].dt.day_name())['website_session_id'].count().sort_values(ascending = False).reset_index(name = 'Count').rename(columns={'created_at': 'Day'}) 
        peak_session_day['Day'] = pd.Categorical(peak_session_day['Day'], categories=day_order)
        peak_session_day = peak_session_day.sort_values('Day').reset_index(drop=True)
        
        
        st.subheader("📊 Session by Day")
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = plt.bar(peak_session_day['Day'], peak_session_day['Count'], color='teal', width=0.5)
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 5, f"{yval / 1_000:,.0f}K", ha='center', va='bottom', fontsize=9)

        plt.title('Website Sessions by Day of the Week')
        plt.xlabel('Day of the Week')
        plt.ylabel('Number of Sessions')
        plt.grid(False)
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Avergae orders per hour 
        orders_per_hour_day = df_order_filtered.groupby(df_order_filtered['created_at'].dt.hour)['order_id'].count().reset_index(name = 'Order Count').rename(columns={'created_at':'Hour'})
        hourly_avg_order = orders_per_hour_day.groupby(df_order_filtered['created_at'].dt.hour)['Order Count'].mean().reset_index(name='Average Orders').rename(columns={'created_at': 'Hour'})
        hourly_avg_order = hourly_avg_order[hourly_avg_order['Average Orders'] > 0]
        
        st.subheader("📦 Average Orders Per day")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax = sns.barplot(data=hourly_avg_order, x='Hour', y='Average Orders', palette='Blues_d')
        for i in ax.patches:
            height = i.get_height()
            ax.text(
                i.get_x() + i.get_width() / 2,
                height + 10,
                f'{height:,.2f}',
                ha='center',
                va='bottom',
                fontsize=8)
            
        plt.title('Average Orders per Hour')
        plt.xlabel('Hour of Day (0–23)')
        plt.ylabel('Average Orders')
        plt.grid(False)
        plt.tight_layout()
        st.pyplot(fig)

 ## ------------------------ USER ANALYSIS-------------------------------------                                     
                                  
    elif selected_page == "User Behavior":
        st.markdown(
    """
    <h1 style='text-align: center; text-decoration: underline; font-weight: bold;font-size: 51px; margin-bottom: 30px;'>
        User Behavior Analysis
    </h1>
    """,
    unsafe_allow_html=True
)

        # ---------------- USER ANALYSIS -------------------
      # ----> Repeat Visitor Analysis --------------------

#Add buyer_type to filtered session data
        df_filtered['buyer_type'] = df_filtered['is_repeat_session'].apply(
        lambda x: 'Repeat' if x == 1 else 'One-Time'
        )

#Sessions count by user type 
        sessions_by_type = (
        df_filtered
          .groupby('buyer_type')
          .size()
          .reset_index(name='session_count')
          .sort_values(by='session_count', ascending=False)
        )

# Pie chart setup
        counts = sessions_by_type['session_count'].values
        labels = sessions_by_type['buyer_type']
        colors = ['#66c2a5', '#fc8d62']
        

        st.subheader("🔁 Repeat Visitor Analysis")

# Plot
        fig, ax = plt.subplots(figsize=(1.5, 1.5))
        wedges, texts, autotexts = ax.pie(
                counts,
                labels=labels,
                autopct='%.1f%%',  
                colors=colors,
                startangle=90
        )


        for text in texts:
                text.set_fontsize(5)

        for autotext in autotexts:
                autotext.set_fontsize(5)


        ax.set_title('Session Counts by Buyer Type', fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)


# ------------ monthly repeat and one time user trend ------------------------

#Extract month number and name 
        df_filtered['month_num'] = df_filtered['created_at'].dt.month
        df_filtered['month_name'] = df_filtered['created_at'].dt.strftime('%b')  # 'Jan', 'Feb', etc.

# Group by month 
        monthly_trend = (
                df_filtered
                .groupby(['month_num', 'month_name', 'buyer_type'])
                .size()
                .reset_index(name='session_count')
        )

# Sort by month_num
        monthly_trend = monthly_trend.sort_values('month_num')

# Pivot 
        monthly_trend_pivot = monthly_trend.pivot(index='month_name', columns='buyer_type', values='session_count').fillna(0)

# Reindex 
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_trend_pivot = monthly_trend_pivot.reindex(month_order)

# Plot
        st.subheader("📈 Monthly Repeat And One Time User Trend")

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.set(style="white")
        sns.lineplot(data=monthly_trend_pivot, markers=True, ax=ax)


        for line in ax.lines:  
                x_data = line.get_xdata()
                y_data = line.get_ydata()
                for i in range(len(x_data)):
                        ax.text(
                                x_data[i],
                                y_data[i] + 300,
                                f'{int(y_data[i])}',
                                ha='center',
                                va='bottom',
                                fontsize=9
                        )

        ax.set_title('Monthly Repeat and One-Time User Trend (Jan to Dec)')
        ax.set_xlabel('Month')
        ax.set_ylabel('Session Count')
        plt.setp(ax.get_xticklabels(), rotation=0)
        ax.legend(title='User Type')
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)


    #--------------------->Purchase Behaviour Analysis--------------------------

        df_filtered = df_website_sessions[base_session_filter].copy()
        df_filtered = df_filtered[
            (df_filtered["device_type"].isin(selected_devices)) &
            (df_filtered["utm_campaign"].isin(selected_campaigns)) &
            (df_filtered["utm_source"].isin(selected_channels))]
        
        filtered_session_ids = df_filtered["website_session_id"].unique()
        
        df_order_filtered = df_order[(df_order["website_session_id"].isin(filtered_session_ids)) &
                                     (df_order["year"].isin(selected_years)) &
                                     (df_order["quarter"].isin(selected_quarters))].copy()



#Classify Orders as New or Repeat 

        first_order = df_order_filtered.groupby('user_id')['created_at'].min().reset_index()
        first_order.columns = ['user_id', 'first_order_date']
    
        orders_labeled = df_order_filtered.merge(first_order, on='user_id')
        orders_labeled['order_type'] = orders_labeled.apply(
            lambda x: 'New' if x['created_at'] == x['first_order_date'] else 'Repeat', axis=1
        )

#Create Purchase Behavior Summary 

        purchase_behavior_summary = orders_labeled.groupby('order_type').agg(
            total_orders=('order_id', 'count'),
            total_revenue=('price_usd', 'sum'),
            avg_order_value=('price_usd', 'mean'),
        ).reset_index()

#Extract Values for Plotting 

        order_labels = purchase_behavior_summary['order_type']            
        total_orders = purchase_behavior_summary['total_orders']         
        total_revenue = purchase_behavior_summary['total_revenue']        
        avg_order_value = purchase_behavior_summary['avg_order_value']    


        revenue_in_millions = total_revenue / 1_000_000 #converting into M

        st.subheader("🛍️ Purchase Behaviour Analysis")

# Plot 3 Pie Charts
        fig, axes = plt.subplots(1, 3, figsize=(10, 5))

# Pie 1: Total Orders
        axes[0].pie(
                total_orders,
                labels=order_labels,
                autopct=lambda pct: f"{pct:.1f}%\n({int(pct / 100. * sum(total_orders)):,})",
                colors=['#66c2a5', '#fc8d62'],
                startangle=90
        )
        axes[0].set_title('Total Orders')

# Pie 2: Total Revenue in Millions (2 decimal places)
        axes[1].pie(
                revenue_in_millions,
                labels=order_labels,
                autopct=lambda pct: f"{pct:.1f}%\n(${pct / 100. * sum(revenue_in_millions):,.2f}M)",
                colors=['#8da0cb', '#e78ac3'],
                startangle=90
        )
        axes[1].set_title('Total Revenue (Million USD)')

# Pie 3: Average Order Value
        def avg_value_autopct(pct):
                total = sum(avg_order_value)
                value = pct * total / 100.0
                return f"${value:,.2f}"

        axes[2].pie(
                avg_order_value,
                labels=order_labels,
                autopct=avg_value_autopct,
                colors=['#a6d854', '#ffd92f'],
                startangle=90
        )
        axes[2].set_title('Average Order Value')

        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("<br><br>", unsafe_allow_html=True)

#--------------------CVR by one time and repeat buyers-----------------

# Count orders per user
        order_counts = df_order_filtered.groupby('user_id').size().reset_index(name='order_count')

# Classify users by order count
        order_counts['buyer_type'] = order_counts['order_count'].apply(lambda x: 'Repeat' if x > 1 else 'One-Time')

# Count sessions per user
        session_counts = df_filtered.groupby('user_id').size().reset_index(name='session_count')

# Merge sessions and orders
        conversion_df = pd.merge(order_counts, session_counts, on='user_id', how='inner')

# Calculate conversion rate per user
        conversion_df['cvr'] = conversion_df['order_count'] / conversion_df['session_count']

# Group by buyer type and calculate average CVR
        cvr_by_type = conversion_df.groupby('buyer_type')['cvr'].mean().reset_index()
        cvr_by_type.columns = ['Buyer Type', 'Avg Conversion Rate']

        st.subheader("📉 CVR By One Time And Repeat Buyers")

# Plot
        sns.set(style="white")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(
                data=cvr_by_type,
                x='Buyer Type',
                y='Avg Conversion Rate',
                hue='Buyer Type',
                palette='pastel',
                legend=False,
                ax=ax
        )
        for p in ax.patches:
                height = p.get_height()
                ax.annotate(f'{height:.2%}', xy=(p.get_x() + p.get_width() / 2, height),
                        xytext=(0, 5), textcoords='offset points',
                        ha='center', va='bottom', fontsize=10)

        ax.set_title('Average Conversion Rate by Buyer Type')
        ax.set_xlabel('Buyer Type')
        ax.set_ylabel('Conversion Rate (%)')
        ax.set_ylim(0, cvr_by_type['Avg Conversion Rate'].max() * 1.2)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))

        plt.tight_layout()
        st.pyplot(fig)


        st.markdown("<br><br>", unsafe_allow_html=True)

#----------------->Customer Segmenatation(RFM)--------------

        df_filtered = df_website_sessions[base_session_filter].copy()
        
        df_filtered = df_filtered[
            (df_filtered["device_type"].isin(selected_devices)) &
            (df_filtered["utm_campaign"].isin(selected_campaigns)) &
            (df_filtered["utm_source"].isin(selected_channels))]
        
        filtered_session_ids = df_filtered["website_session_id"].unique()
        df_order_filtered = df_order[
            (df_order["website_session_id"].isin(filtered_session_ids)) &
            (df_order["year"].isin(selected_years)) &
            (df_order["quarter"].isin(selected_quarters))].copy()

# Define reference date (latest order date)
        reference_date = df_order_filtered['created_at'].max()

# Calculate Recency, Frequency, Monetary per user
        rfm = df_order_filtered.groupby('user_id').agg({
            'created_at': lambda x: (reference_date - x.max()).days,   
            'order_id': 'count',                                       
            'price_usd': 'sum'                                         
        }).reset_index()

        rfm.columns = ['user_id', 'Recency', 'Frequency', 'Monetary']

# Quantile scoring (1–3 scale)
        rfm['R_rank'] = pd.qcut(rfm['Recency'], 3, labels=[3, 2, 1]).astype(int)
        rfm['F_rank'] = pd.qcut(rfm['Frequency'].rank(method='first'), 3, labels=[1, 2, 3]).astype(int)
        rfm['M_rank'] = pd.qcut(rfm['Monetary'], 3, labels=[1, 2, 3], duplicates='drop').astype(int)

# Calculate total RFM Score
        rfm['RFM_Score'] = rfm['R_rank'] + rfm['F_rank'] + rfm['M_rank']

# Segment customers by score
        def segment_customer(score):
            if score >= 7:
                return 'High-Value'
            elif score >= 4:
                return 'Mid-Value'
            else:
                return 'Low-Value'

        rfm['Customer_Segment'] = rfm['RFM_Score'].apply(segment_customer)

#Output clean table
        rfm_segmented = rfm[['user_id', 'Recency', 'Frequency', 'Monetary', 'RFM_Score', 'Customer_Segment']]
        


        st.header("🧾 Customer Segmentation (RFM) Analysis") 

  #--------------Count of customers by segments---------------

# Count of users
        segment_counts = rfm['Customer_Segment'].value_counts()

#autocpt
        def make_autopct(values):
                def my_autopct(pct):
                        total = sum(values)
                        val = int(round(pct * total / 100.0))
                        return f"{pct:.1f}%\n({val:,})"
                return my_autopct

        st.subheader("👥 Count Of Customers By RFM Segmentation")

# Plot
        fig, ax = plt.subplots(figsize=(3, 2))
        colors = ["#8db8d3", "#cdcd92", "#e9968d"]
#font size
        wedges, texts, autotexts = ax.pie(
                segment_counts,
                labels=segment_counts.index,
                autopct=make_autopct(segment_counts.values),
                startangle=140,
                colors=colors
        )

        for text in texts:
                text.set_fontsize(5)         # Segment labels

        for autotext in autotexts:
                autotext.set_fontsize(5)     # Percent + count text

        ax.set_title('Customer Segment Distribution (RFM)', fontsize=10)
        ax.axis('equal')
        plt.tight_layout()
        st.pyplot(fig)


        st.markdown("<br><br>", unsafe_allow_html=True)

        #-------------------Revenue contribution by segment--------------------

# Total revenue by segment
        revenue_by_segment = rfm.groupby('Customer_Segment')['Monetary'].sum().reset_index()

        st.subheader("💼 Revenue Contribution By Segments")

# plot
 
        sns.set(style="white")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(data=revenue_by_segment, x='Customer_Segment', y='Monetary', ax=ax)

        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.2f}M'))

        ax.set_title('Revenue Contribution by Customer Segment')
        ax.set_ylabel('Total Revenue (USD)')
        ax.set_xlabel('Customer Segment')
        for index, row in revenue_by_segment.iterrows():
                ax.text(index, row['Monetary'] + row['Monetary'] * 0.01, f"${row['Monetary']/1e6:.2f}M", ha='center', fontsize=9)

        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("<br><br>", unsafe_allow_html=True)


## -------------------  channel portfolio management------------------- 
        
    elif selected_page == "Channel Portfolio Management":
        st.markdown(
    """
    <h1 style='text-align: center; text-decoration: underline; font-weight: bold;font-size: 51px; margin-bottom: 30px;'>
        Channel Portfolio Management
    </h1>
    """,
    unsafe_allow_html=True
)

        
        # ------------------ 1. Average Session Duration by Channel ------------------
        
# Compute session durations in seconds
        session_times = df_pageview_filtered.groupby('website_session_id')['created_at'].agg(['min', 'max'])
        session_times['session_duration_sec'] = (session_times['max'] - session_times['min']).dt.total_seconds()
        session_times = session_times[['session_duration_sec']].reset_index()

# Merge with session sources
        sessions_with_duration = pd.merge(
                       df_filtered[['website_session_id', 'utm_source']],
                       session_times,on='website_session_id',how='inner')

# Filter out 'other' traffic
        sessions_with_duration = sessions_with_duration[
                sessions_with_duration['utm_source'].str.strip().str.lower() != 'other']

# Group by source
        avg_duration_by_channel = (sessions_with_duration.groupby('utm_source')['session_duration_sec']
                                    .mean().reset_index()
                                .sort_values(by='session_duration_sec', ascending=False)
                                                  )

        st.subheader("⏱️ Average Session Duration by Channel")
# Plot
        fig1, ax1 = plt.subplots(figsize=(5, 3))
        sns.barplot( data=avg_duration_by_channel, x='utm_source',
                     y='session_duration_sec',palette='Set2',ax=ax1 )

# Add labels
        for bar in ax1.patches:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2,
                        height - 2,f"{height:.1f}s",ha='center',va='top',
                        fontsize=9,color='black'  )

        ax1.set_title('Average Session Duration by Channel')
        ax1.set_xlabel('UTM Source (Channel)')
        ax1.set_ylabel('Avg Session Duration (Seconds)')
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=30)
        st.pyplot(fig1)


        st.markdown("<br><br>", unsafe_allow_html=True)


# ------------------ 2. Average Pages Viewed per Session by Channel ------------------

# Count pageviews per session
        pageviews_per_session = (
                        df_pageview_filtered.groupby('website_session_id').size()
                        .reset_index(name='pageviews') )

# Merge with sessions
        session_pages = pd.merge( df_filtered[['website_session_id', 'utm_source']],
                                  pageviews_per_session,on='website_session_id',how='inner'
                                       )

# Remove 'other'
        session_pages = session_pages[
                       session_pages['utm_source'].str.strip().str.lower() != 'other'
                                          ]

# Average pages per session
        avg_pages_by_channel = (session_pages.groupby('utm_source')['pageviews']
                                .mean().reset_index()
                                .sort_values(by='pageviews', ascending=False)
                                        )
        
        st.subheader("📄 Average Pages Viewed per Session by Channel")
# Plot
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.barplot(data=avg_pages_by_channel, x='utm_source',
                     y='pageviews',
                     palette='Set2', ax=ax2 )

# Add labels
        for bar in ax2.patches:
            height = bar.get_height()
            ax2.text(
                     bar.get_x() + bar.get_width() / 2,
                     height - 0.2,
                     f"{height:.2f}",
                     ha='center',
                     va='top',
                     fontsize=9,
                     color='black' )

        ax2.set_title('Average Pages per Session by Channel')
        ax2.set_xlabel('UTM Source (Channel)')
        ax2.set_ylabel('Avg Pages per Session')
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=30)
        st.pyplot(fig2)

        st.markdown("<br><br>", unsafe_allow_html=True)


      # ----------- Total Orders by Channel -----------

# Pre-filter orders linked to filtered sessions
        df_order_filtered = df_order_filtered[
                df_order_filtered['website_session_id'].isin(df_filtered['website_session_id'])
        ].copy()

# Merge orders with filtered session sources
        orders_with_channel = df_order_filtered.merge(
                df_filtered[['website_session_id', 'utm_source']],
                on='website_session_id',
                how='left'
        )

# Filter out 'Other'
        orders_with_channel = orders_with_channel[
                orders_with_channel['utm_source'].str.strip().str.lower() != 'other'
        ]

# Count total orders per channel
        orders_by_channel = (
                orders_with_channel.groupby('utm_source').size()
                .reset_index(name='total_orders')
                .sort_values(by='total_orders', ascending=False)
        )

# Plot as usual
        st.subheader("📦 Total Orders by Channel")

        fig1, ax1 = plt.subplots(figsize=(7, 4))
        sns.set(style="white")
        sns.barplot(
                data=orders_by_channel,
                x='utm_source',
                y='total_orders',
                palette='pastel',
                ax=ax1
        )

        for bar in ax1.patches:
                height = bar.get_height()
                ax1.text(
                bar.get_x() + bar.get_width() / 2,
                height + 5,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=9
        )

        ax1.set_title("Total Orders by Channel")
        ax1.set_xlabel("Channel (utm_source)")
        ax1.set_ylabel("Total Orders")
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=30)
        st.pyplot(fig1)

        st.markdown("<br><br>", unsafe_allow_html=True)


# ----------- Total Revenue by Channel -----------

   

# Step 1: Pre-filter orders using filtered sessions
        df_order_filtered = df_order_filtered[
                df_order_filtered['website_session_id'].isin(df_filtered['website_session_id'])
        ].copy()

# Step 2: Merge orders with session sources
        orders_with_channel = df_order_filtered.merge(
                df_filtered[['website_session_id', 'utm_source']],
                on='website_session_id',
                how='left'
        )

# Step 3: Filter out 'Other'
        orders_with_channel = orders_with_channel[
                orders_with_channel['utm_source'].str.strip().str.lower() != 'other'
        ]

# Step 4: Aggregate revenue
        revenue_by_channel = (
                orders_with_channel.groupby('utm_source')['price_usd']
                .sum()
        .reset_index()
        .sort_values(by='price_usd', ascending=False)
        )

# Step 5: Plotting
        st.subheader("💰 Total Revenue by Channel")

        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.set(style="white")
        sns.barplot(
                data=revenue_by_channel,
                x='utm_source',
                y='price_usd',
                palette='muted',
                ax=ax2
        )

        ax2.ticklabel_format(style='plain', axis='y')

        for bar in ax2.patches:
                height = bar.get_height()
                ax2.text(
                        bar.get_x() + bar.get_width() / 2,
                        height + 1,
                        f"${height / 1_000_000:,.2f}M",
                        ha='center',
                        va='center',
                        fontsize=9
                )

        ax2.set_title("Total Revenue by Channel")
        ax2.set_xlabel("Channel (utm_source)")
        ax2.set_ylabel("Revenue (USD)")
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=30)
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1_000_000:.1f}M'))

        st.pyplot(fig2)
        st.markdown("<br><br>", unsafe_allow_html=True)

             # --------- Avg Revenue per Session by Channel ---------

# Filter sessions (remove 'other')
        filtered_sessions = df_filtered[
        df_filtered['utm_source'].str.strip().str.lower() != 'other']

# Merge orders with sessions to get utm_source
        orders_with_channel = df_order_filtered.merge(
          filtered_sessions[['website_session_id', 'utm_source']],
             on='website_session_id',how='left')

# Total revenue per channel
        revenue_per_channel = orders_with_channel.groupby('utm_source')['price_usd'].sum().reset_index()

# Total sessions per channel
    # Total sessions per channel (fixed version)
        sessions_per_channel = (filtered_sessions.groupby('utm_source')
                    .agg(total_sessions=('website_session_id', 'count'))
                    .reset_index() )


# Calculate Avg Revenue per Session
        avg_revenue_per_session = revenue_per_channel.merge(sessions_per_channel, on='utm_source')
        avg_revenue_per_session['avg_revenue_per_session'] = (
        avg_revenue_per_session['price_usd'] / avg_revenue_per_session['total_sessions'])

# Sort
        avg_revenue_per_session = avg_revenue_per_session.sort_values(
                 by='avg_revenue_per_session', ascending=False )
        st.subheader("💸 Avg Revenue per Session by Channel")
# Plot
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.set(style="white")
        sns.barplot(
        data=avg_revenue_per_session,
        x='utm_source',
        y='avg_revenue_per_session',
        palette='coolwarm',
        ax=ax1)

# Add labels
        for i, row in avg_revenue_per_session.iterrows():
            ax1.text(
                 i,
                row['avg_revenue_per_session'] * 0.5,
                f"${row['avg_revenue_per_session']:.2f}",
                ha='center',
                va='center',
                fontsize=9   )

        ax1.set_title('Average Revenue per Session by Channel')
        ax1.set_xlabel('UTM Source (Channel)')
        ax1.set_ylabel('Avg Revenue per Session (USD)')
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=30)
        st.pyplot(fig1)


        st.markdown("<br><br>", unsafe_allow_html=True)

# --------- Total Refunds by Channel (Order Count) ---------

# Get refunded order IDs + sessions
        refunds_with_session = df_refund_filtered.merge(
          df_order_filtered[['order_id', 'website_session_id']],
             on='order_id',
            how='left' )

# Merge with session source
        refunds_with_channel = refunds_with_session.merge(
    df_website_sessions[['website_session_id', 'utm_source']],
    on='website_session_id',
    how='left'
)

# Count refunds
        refunds_by_channel = (refunds_with_channel.groupby('utm_source')
                         .size().reset_index(name='total_refunds')
                         .sort_values(by='total_refunds', ascending=False)
                             )

        st.subheader("↩️ Total Refunds by Channel")
# Plot
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        sns.barplot(
    data=refunds_by_channel,
    x='utm_source',
    y='total_refunds',
    palette='coolwarm',
    ax=ax2
)

# Add labels
        for patch in ax2.patches:
            height = patch.get_height()
            x = patch.get_x() + patch.get_width() / 2
            ax2.text(x, height + 0.5, f"{int(height)}", ha='center', va='bottom', fontsize=9)

        ax2.set_title("Total Number of Refunds by Channel")
        ax2.set_xlabel("Channel (utm_source)")
        ax2.set_ylabel("Number of Refunds")
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=30)
        st.pyplot(fig2)


        st.markdown("<br><br>", unsafe_allow_html=True)

 # ----------- Total Refund Amount by Channel -----------

# Merge refunds with orders and sessions
        refunds_with_orders = df_refund_filtered.merge(
        df_order_filtered[['order_id', 'website_session_id']],
        on='order_id',
        how='left').merge(df_filtered[['website_session_id', 'utm_source']],
                  on='website_session_id',how='left' )

# Total refund amount per channel
        refunds_by_channel = (
     refunds_with_orders
    .groupby('utm_source')['refund_amount_usd']
    .sum()
    .reset_index()
    .sort_values(by='refund_amount_usd', ascending=False)
)
        st.subheader("↩️ Total Refund Amount by Channel")
# Plot
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        sns.set(style="white")
        sns.barplot(
    data=refunds_by_channel,
    x='utm_source',
    y='refund_amount_usd',
    palette='Reds',
    ax=ax1
)

# Add data labels
        for patch in ax1.patches:
            height = patch.get_height()
            ax1.text(
                    patch.get_x() + patch.get_width() / 2,
                     height + 500,
                     f"${height/1_000:,.2f}k",
                     ha='center',
                     va='bottom',
                     fontsize=9    )

        ax1.set_title("Total Refunds by Channel")
        ax1.set_xlabel("UTM Source")
        ax1.set_ylabel("Refund Amount (USD)")
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=30)
        plt.tight_layout()
        st.pyplot(fig1)



  







# --------------------------
# MAIN APP
# --------------------------
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if not st.session_state.logged_in:
        login_page()
    elif st.session_state.page == "business":
        business_context()
    elif st.session_state.page == "dashboard":
        dashboard()
    else:
        project_intro()

if __name__ == "__main__":
    main()
