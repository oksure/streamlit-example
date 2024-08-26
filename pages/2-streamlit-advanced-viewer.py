# pages/2_Advanced_Viewer.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
from matplotlib.ticker import ScalarFormatter

st.set_page_config(page_title="Advanced CSV Viewer", page_icon="📊", layout="wide")

def apply_filters(df, filters):
    for column, condition in filters.items():
        if condition['operator'] == 'equals':
            df = df[df[column] == condition['value']]
        elif condition['operator'] == 'contains':
            df = df[df[column].astype(str).str.contains(condition['value'], case=False)]
        elif condition['operator'] == 'greater than':
            df = df[df[column] > float(condition['value'])]
        elif condition['operator'] == 'less than':
            df = df[df[column] < float(condition['value'])]
    return df

def prepare_for_log_scale(series):
    series = series.replace([np.inf, -np.inf], np.nan).dropna()
    if len(series) == 0:
        return pd.Series([1])
    min_positive = series[series > 0].min() if any(series > 0) else 1e-10
    series = series.apply(lambda x: max(x, min_positive / 10))
    return series

class CustomScalarFormatter(ScalarFormatter):
    def _set_format(self):
        self.format = '%1.1e'

def main():
    st.title("Advanced CSV Viewer")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
        
        st.subheader("Data Filtering")
        filters = {}
        columns = df.columns.tolist()
        
        num_filters = st.number_input("Number of filters", min_value=0, max_value=5, value=1)
        for i in range(num_filters):
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_column = st.selectbox(f"Column {i+1}", options=columns, key=f"filter_column_{i}")
            with col2:
                filter_operator = st.selectbox(f"Operator {i+1}", options=['equals', 'contains', 'greater than', 'less than'], key=f"filter_operator_{i}")
            with col3:
                filter_value = st.text_input(f"Value {i+1}", key=f"filter_value_{i}")
            
            if filter_column and filter_operator and filter_value:
                filters[filter_column] = {'operator': filter_operator, 'value': filter_value}
        
        filtered_df = apply_filters(df, filters)
        
        st.subheader("Data Preview")
        st.write(filtered_df)
        
        st.subheader("Dataset Info")
        st.write(f"Number of rows: {filtered_df.shape[0]}")
        st.write(f"Number of columns: {filtered_df.shape[1]}")
        
        st.subheader("Data Visualization")
        columns = filtered_df.columns.tolist()
        x_axis = st.selectbox("Select X-axis", options=columns)
        y_axis = st.selectbox("Select Y-axis", options=columns)
        
        log_x = st.checkbox("Use log scale for X-axis")
        log_y = st.checkbox("Use log scale for Y-axis")
        
        plot_df = filtered_df.copy()
        if log_x:
            plot_df[x_axis] = prepare_for_log_scale(plot_df[x_axis])
        if log_y:
            plot_df[y_axis] = prepare_for_log_scale(plot_df[y_axis])
        
        st.write("Seaborn Scatter Plot:")
        fig, ax = plt.subplots()
        sns.scatterplot(data=plot_df, x=x_axis, y=y_axis, ax=ax)
        if log_x:
            ax.set_xscale('log')
            ax.xaxis.set_major_formatter(CustomScalarFormatter())
        if log_y:
            ax.set_yscale('log')
            ax.yaxis.set_major_formatter(CustomScalarFormatter())
        plt.title(f"{y_axis} vs {x_axis}")
        st.pyplot(fig)
        
        st.write("Plotly Interactive Scatter Plot:")
        fig_plotly = px.scatter(plot_df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}",
                                log_x=log_x, log_y=log_y)
        st.plotly_chart(fig_plotly)

if __name__ == "__main__":
    main()
