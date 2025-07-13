import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import io
import base64
import json

# Set page config
st.set_page_config(
    page_title="Retail Transaction Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.kpi-container {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
}
.kpi-title {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 0.2rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: bold;
    color: #1f77b4;
}
.filter-container {
    background-color: #ffffff;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #e6e6e6;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for filters
if 'filters_applied' not in st.session_state:
    st.session_state.filters_applied = False

# Function to load and process data
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(r"C:\Users\avaza\Desktop\Streamlit Apps\Transaction\retail_data.csv")
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.dropna(subset=['Date'], inplace=True)
            return df
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None
    return None

# Function to create downloadable CSV
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV File</a>'
    return href

# Function to create downloadable Excel
def get_excel_download_link(df, filename):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Data', index=False)
    processed_data = output.getvalue()
    b64 = base64.b64encode(processed_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
    return href

# File upload widget
uploaded_file = st.file_uploader("Upload retail_data.csv", type="csv")

if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    if df is not None:
        # Main dashboard
        st.markdown('<h1 class="main-header">🛒 Retail Transaction Dashboard</h1>', unsafe_allow_html=True)

        # Sidebar filters
        st.sidebar.markdown("## 🎛️ Filters")

        # Date range filter
        date_range = st.sidebar.date_input(
            "📅 Select Date Range",
            value=(df['Date'].min(), df['Date'].max()),
            min_value=df['Date'].min(),
            max_value=df['Date'].max()
        )

        # Amount range slider
        amount_range = st.sidebar.slider(
            "💰 Amount Range",
            min_value=float(df['Amount'].min()),
            max_value=float(df['Amount'].max()),
            value=(float(df['Amount'].min()), float(df['Amount'].max())),
            step=10.0
        )

        # Age range slider
        age_range = st.sidebar.slider(
            "👥 Age Range",
            min_value=int(df['Age'].min()),
            max_value=int(df['Age'].max()),
            value=(int(df['Age'].min()), int(df['Age'].max()))
        )

        # Multi-select filters
        countries = st.sidebar.multiselect(
            "🌍 Countries",
            options=df['Country'].unique(),
            default=df['Country'].unique()
        )

        product_categories = st.sidebar.multiselect(
            "📦 Product Categories",
            options=df['Product_Category'].unique(),
            default=df['Product_Category'].unique()
        )

        customer_segments = st.sidebar.multiselect(
            "⭐ Customer Segments",
            options=df['Customer_Segment'].unique(),
            default=df['Customer_Segment'].unique()
        )

        payment_methods = st.sidebar.multiselect(
            "💳 Payment Methods",
            options=df['Payment_Method'].unique(),
            default=df['Payment_Method'].unique()
        )

        order_status = st.sidebar.multiselect(
            "📋 Order Status",
            options=df['Order_Status'].unique(),
            default=df['Order_Status'].unique()
        )

        # Reset filters button
        if st.sidebar.button("🔄 Reset All Filters"):
            st.rerun()

        # Apply filters button
        apply_filters = st.sidebar.button("✅ Apply Filters")

        # Filter data
        filtered_df = df.copy()

        if apply_filters or st.session_state.filters_applied:
            st.session_state.filters_applied = True
            
            filtered_df = filtered_df[
                (filtered_df['Date'] >= pd.to_datetime(date_range[0])) & 
                (filtered_df['Date'] <= pd.to_datetime(date_range[1]))
            ]
            
            filtered_df = filtered_df[
                (filtered_df['Amount'] >= amount_range[0]) & 
                (filtered_df['Amount'] <= amount_range[1])
            ]
            
            filtered_df = filtered_df[
                (filtered_df['Age'] >= age_range[0]) & 
                (filtered_df['Age'] <= age_range[1])
            ]
            
            filtered_df = filtered_df[filtered_df['Country'].isin(countries)]
            filtered_df = filtered_df[filtered_df['Product_Category'].isin(product_categories)]
            filtered_df = filtered_df[filtered_df['Customer_Segment'].isin(customer_segments)]
            filtered_df = filtered_df[filtered_df['Payment_Method'].isin(payment_methods)]
            filtered_df = filtered_df[filtered_df['Order_Status'].isin(order_status)]

        # Display filter status
        if st.session_state.filters_applied:
            st.success(f"✅ Filters applied! Showing {len(filtered_df):,} out of {len(df):,} records")
        else:
            st.info("ℹ️ Showing all records. Use filters in the sidebar to narrow down the data.")

        # KPIs Section
        st.markdown("## 📊 Key Performance Indicators")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(
                f"""
                <div class="kpi-container">
                    <div class="kpi-title">Total Transactions</div>
                    <div class="kpi-value">{len(filtered_df):,}</div>
                </div>
                """, 
                unsafe_allow_html=True
            )

        with col2:
            total_revenue = filtered_df['Amount'].sum()
            st.markdown(
                f"""
                <div class="kpi-container">
                    <div class="kpi-title">Total Revenue</div>
                    <div class="kpi-value">${total_revenue:.2f}</div>
                </div>
                """, 
                unsafe_allow_html=True
            )

        with col3:
            avg_order_value = filtered_df['Amount'].mean()
            st.markdown(
                f"""
                <div class="kpi-container">
                    <div class="kpi-title">Avg Order Value</div>
                    <div class="kpi-value">${avg_order_value:.2f}</div>
                </div>
                """, 
                unsafe_allow_html=True
            )

        with col4:
            unique_customers = filtered_df['Customer_ID'].nunique()
            st.markdown(
                f"""
                <div class="kpi-container">
                    <div class="kpi-title">Unique Customers</div>
                    <div class="kpi-value">{unique_customers:,}</div>
                </div>
                """, 
                unsafe_allow_html=True
            )

        with col5:
            avg_rating = filtered_df['Ratings'].mean()
            st.markdown(
                f"""
                <div class="kpi-container">
                    <div class="kpi-title">Avg Rating</div>
                    <div class="kpi-value">{avg_rating:.1f}⭐</div>
                </div>
                """, 
                unsafe_allow_html=True
            )

        # Data Summary Section
        st.markdown("## 📈 Data Summary")

        tab1, tab2, tab3 = st.tabs(["📊 Overview", "📋 Detailed Stats", "🔍 Data Quality"])

        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Revenue by Category")
                category_revenue = filtered_df.groupby('Product_Category')['Amount'].sum().sort_values(ascending=False)
                fig_category = px.bar(
                    x=category_revenue.index, 
                    y=category_revenue.values,
                    labels={'x': 'Product Category', 'y': 'Revenue ($)'},
                    title="Revenue by Product Category"
                )
                st.plotly_chart(fig_category, use_container_width=True)
            
            with col2:
                st.subheader("Customer Segment Distribution")
                segment_counts = filtered_df['Customer_Segment'].value_counts()
                fig_segment = px.pie(
                    values=segment_counts.values, 
                    names=segment_counts.index,
                    title="Customer Segment Distribution"
                )
                st.plotly_chart(fig_segment, use_container_width=True)

        with tab2:
            st.subheader("Detailed Statistics")
            
            numerical_cols = ['Age', 'Amount', 'Total_Amount', 'Ratings']
            stats_df = filtered_df[numerical_cols].describe()
            st.dataframe(stats_df, use_container_width=True)
            
            st.subheader("Categorical Data Distribution")
            categorical_cols = ['Country', 'Product_Category', 'Customer_Segment', 'Payment_Method', 'Order_Status']
            
            for col in categorical_cols[:3]:
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**{col}**")
                    st.write(filtered_df[col].value_counts().head(10))

        with tab3:
            st.subheader("Data Quality Report")
            
            missing_data = filtered_df.isnull().sum()
            missing_percentage = (missing_data / len(filtered_df)) * 100
            
            quality_df = pd.DataFrame({
                'Column': missing_data.index,
                'Missing Count': missing_data.values,
                'Missing %': missing_percentage.values
            })
            quality_df = quality_df[quality_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
            
            if not quality_df.empty:
                st.dataframe(quality_df, use_container_width=True)
            else:
                st.success("✅ No missing values found in the filtered dataset!")
            
            st.subheader("Data Types")
            dtype_df = pd.DataFrame({
                'Column': filtered_df.dtypes.index,
                'Data Type': filtered_df.dtypes.values
            })
            st.dataframe(dtype_df, use_container_width=True)

        # Visualizations Section
        st.markdown("## 📊 Interactive Visualizations")

        st.subheader("📈 Sales Trends Over Time")
        daily_sales = filtered_df.groupby('Date')['Amount'].sum().reset_index()
        fig_timeseries = px.line(
            daily_sales, 
            x='Date', 
            y='Amount',
            title="Daily Sales Trend",
            labels={'Amount': 'Sales Amount ($)', 'Date': 'Date'}
        )
        st.plotly_chart(fig_timeseries, use_container_width=True)

        st.subheader("🔥 Correlation Heatmap")
        corr_cols = ['Age', 'Amount', 'Total_Amount', 'Ratings']
        corr_matrix = filtered_df[corr_cols].corr()
        
        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix of Numerical Variables"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

        st.subheader("🌍 Geographic Distribution")
        country_stats = filtered_df.groupby('Country').agg({
            'Amount': ['sum', 'mean', 'count']
        }).round(2)
        country_stats.columns = ['Total Revenue', 'Avg Order Value', 'Transaction Count']
        country_stats = country_stats.sort_values('Total Revenue', ascending=False)
        st.dataframe(country_stats, use_container_width=True)

        # Export Section
        st.markdown("## 💾 Export Data")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📥 Export Filtered Data (CSV)"):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"retail_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

        with col2:
            if st.button("📥 Export Summary Stats (CSV)"):
                summary_stats = filtered_df.describe()
                csv = summary_stats.to_csv()
                st.download_button(
                    label="Download Summary Stats",
                    data=csv,
                    file_name=f"retail_summary_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

        with col3:
            if st.button("📥 Export KPIs (JSON)"):
                kpis = {
                    'total_transactions': len(filtered_df),
                    'total_revenue': float(total_revenue),
                    'avg_order_value': float(avg_order_value),
                    'unique_customers': int(unique_customers),
                    'avg_rating': float(avg_rating),
                    'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                json_data = json.dumps(kpis, indent=2)
                st.download_button(
                    label="Download KPIs (JSON)",
                    data=json_data,
                    file_name=f"retail_kpis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

        # Raw Data Section
        st.markdown("## 🔍 Raw Data Viewer")

        show_sample = st.checkbox("Show Sample Data (first 1000 rows)")
        if show_sample:
            st.dataframe(filtered_df.head(1000), use_container_width=True)

        with st.expander("ℹ️ Dataset Information"):
            st.write(f"**Dataset Shape:** {filtered_df.shape}")
            st.write(f"**Memory Usage:** {filtered_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            st.write(f"**Date Range:** {filtered_df['Date'].min()} to {filtered_df['Date'].max()}")
            st.write(f"**Unique Products:** {filtered_df['Product_Type'].nunique()}")
            st.write(f"**Unique Brands:** {filtered_df['Product_Brand'].nunique()}")

        # Footer
        st.markdown("---")
        st.markdown("### 🚀 Dashboard Features")
        st.markdown("""
        - **Interactive Filters**: Use sidebar widgets to filter data dynamically
        - **Real-time KPIs**: Key metrics update automatically with filters
        - **Multiple Visualizations**: Charts, graphs, and statistical summaries
        - **Export Capabilities**: Download filtered data in multiple formats
        - **Data Quality Checks**: Built-in data validation and quality reports
        - **Responsive Design**: Optimized for different screen sizes
        """)
    else:
        st.error("Failed to load the data. Please check the file format and try again.")
else:
    st.info("Please upload the retail_data.csv file to begin.")