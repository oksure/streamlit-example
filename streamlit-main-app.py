# main.py
import streamlit as st

st.set_page_config(page_title="CSV Data Viewer", page_icon="📊", layout="wide")

st.title("Welcome to the CSV Data Viewer")
st.write("This application allows you to upload and analyze CSV files in various ways.")

st.header("Available Viewers")
st.write("Please select a viewer from the sidebar to get started.")

st.markdown("""
- **Basic Viewer**: Upload and view your CSV data with basic filtering and visualization options.
- **Advanced Viewer**: Includes additional features like log scale transformations and interactive plots.
""")

st.header("How to Use")
st.write("""
1. Select a viewer from the sidebar.
2. Upload your CSV file.
3. Use the provided options to filter and visualize your data.
4. Explore and analyze your data using the interactive features.
""")

st.header("About")
st.write("""
This application is designed to help you explore and analyze CSV data quickly and easily. 
Whether you're a data analyst, researcher, or just curious about your data, our viewers 
provide powerful tools to gain insights from your CSV files.
""")
