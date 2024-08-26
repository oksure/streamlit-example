# pages/1_Basic_Viewer.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Basic CSV Viewer", page_icon="📊", layout="wide")

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

def main():
    st.title("Basic CSV Viewer")

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
        
        fig, ax = plt.subplots()
        sns.scatterplot(data=filtered_df, x=x_axis, y=y_axis, ax=ax)
        plt.title(f"{y_axis} vs {x_axis}")
        st.pyplot(fig)

if __name__ == "__main__":
    main()
