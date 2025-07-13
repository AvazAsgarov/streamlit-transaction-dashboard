# Retail Transaction Dashboard

A comprehensive **Retail Transaction Dashboard** built with [Streamlit](https://streamlit.io/), [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/), and [Plotly](https://plotly.com/). This interactive web application allows users to upload and analyze retail transaction data, providing insights into key performance indicators (KPIs), sales trends, customer demographics, and geographic distributions through dynamic visualizations and filters.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Deployment](#deployment)
- [Contact](#contact)

## Overview
The Retail Transaction Dashboard is designed for retail analysts and managers to explore and analyze transaction data. Users can upload a CSV file containing transaction details and use interactive filters to drill down into specific date ranges, amounts, ages, countries, product categories, customer segments, payment methods, and order statuses. The dashboard features real-time KPIs, multiple visualizations, data quality reports, and export options for further analysis.

## Features
- **Interactive Visualizations**: Includes bar charts, pie charts, line graphs, heatmaps, and geographic distributions powered by Plotly.
- **Dynamic Filters**: Filter data by date range, amount, age, country, product category, customer segment, payment method, and order status using sidebar controls.
- **Key Performance Indicators (KPIs)**: Displays total transactions, total revenue, average order value, unique customers, and average ratings.
- **Data Summary**: Provides detailed statistics, categorical data distribution, and data quality reports.
- **Data Export**: Download filtered data as CSV, summary stats as CSV, and KPIs as JSON with timestamps.
- **Raw Data Viewer**: Option to view a sample of the data and dataset information.
- **Responsive Design**: Optimized for both desktop and mobile devices with a wide layout.

## Screenshots
Below are screenshots of the Retail Transaction Dashboard (to be added as you capture them):

### KPIs and Filters
![KPIs and Filters](screenshots/kpis_filters.png)
*Displays key performance indicators and sidebar filters.*

### Revenue by Category
![Revenue by Category](screenshots/revenue_by_category.png)
*Shows a bar chart of revenue by product category.*

### Customer Segment Distribution
![Customer Segment Distribution](screenshots/customer_segment.png)
*Illustrates customer segment distribution with a pie chart.*

### Sales Trends Over Time
![Sales Trends](screenshots/sales_trends.png)
*Displays daily sales trends with a line graph.*

### Correlation Heatmap
![Correlation Heatmap](screenshots/correlation_heatmap.png)
*Shows correlations between numerical variables.*

## Installation
To run the dashboard locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AvazAsgarov/streamlit-transaction-dashboard.git
   cd streamlit-transaction-dashboard
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.8+ installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   Launch the Streamlit app:
   ```bash
   streamlit run retail_transaction_streamlit_app.py
   ```
   The dashboard will open in your default web browser.

## Usage
1. **Access the Live App**: Visit [Retail Transaction Dashboard](https://transaction-dashboard-avaz-asgarov.streamlit.app/) to explore the dashboard online.
2. **Upload Data**: Use the file uploader to load your `retail_data.csv` file.
3. **Adjust Filters**: Use the sidebar to set filters such as date range, amount, age, and categorical options.
4. **Explore Tabs**:
   - **Overview**: View KPIs and basic visualizations.
   - **Data Summary**: Access detailed stats, categorical distributions, and data quality reports.
   - **Interactive Visualizations**: Analyze sales trends, correlations, and geographic data.
   - **Export Data**: Download filtered data, summary stats, or KPIs.
   - **Raw Data Viewer**: Check a sample of the data and dataset info.
5. **Export Data**: Use the export buttons to download data in various formats.

## Dataset
The dashboard supports a CSV file (`retail_data.csv`) with the following columns:
- **Date**: Transaction date
- **Amount**: Transaction amount
- **Age**: Customer age
- **Country**: Customer country
- **Product_Category**: Product category
- **Customer_Segment**: Customer segment
- **Payment_Method**: Payment method
- **Order_Status**: Order status
- **Customer_ID**: Unique customer identifier
- **Ratings**: Product ratings
- **Total_Amount**: Total amount (if applicable)
- **Product_Type**: Product type
- **Product_Brand**: Product brand

The dataset should be in CSV format, with `Date` convertible to a datetime object.

## Deployment
This dashboard is deployed using [Streamlit Community Cloud](https://streamlit.io/cloud). Access the live app at [Retail Transaction Dashboard](https://transaction-dashboard-avaz-asgarov.streamlit.app/). The deployment is managed from this GitHub repository, requiring only the Python script (`retail_transaction_streamlit_app.py`) and `requirements.txt`.

## Contact
For any questions or suggestions, please open an issue in this repository or connect with me on LinkedIn: **[Avaz Asgarov](https://www.linkedin.com/in/avaz-asgarov/)**.