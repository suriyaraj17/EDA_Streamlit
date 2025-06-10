import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="EDA Web Application", layout="wide")

# Apply custom CSS styling for improved UI/UX
st.markdown(
    """
    <style>
        /* Global font and background styling */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f9;
            color: #333;
        }
        /* Title styling */
        .main-title {
            color: #4a90e2;
            text-align: center;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        /* Sidebar styling */
        .css-1aumxhk {
            background-color: #2e4053;
            color: white;
            padding: 20px;
            border-radius: 10px;
        }
        .css-1aumxhk .css-15zrgzn {
            color: white;
        }
        /* Subheader styling */
        .stMarkdown h2 {
            color: #333;
            background-color: #dde7f0;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        /* Button styling */
        button {
            background-color: #4a90e2;
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
        }
        button:hover {
            background-color: #2e75c2;
        }
        /* Improved spacing */
        .stTextInput, .stSelectbox, .stButton {
            margin-bottom: 15px;
        }
        /* Add padding to content sections */
        .stMarkdown, .stDataFrame, .stButton {
            padding: 10px;
        }
        /* Adjust margins */
        .stButton, .stSelectbox {
            margin-top: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Dashboard Title with Enhanced Styling
st.markdown(
    """
    <div style="
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: white;
        background: linear-gradient(90deg, #4a90e2, #2e4053);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    ">
        EDA Web Application
    </div>
    """,
    unsafe_allow_html=True,
)

# Subtitle with Instructions
st.markdown(
    """
    <p style="
        text-align: center;
        font-size: 20px;
        color: #555;
        margin-top: 10px;
    ">
        Analyze, clean, and visualize your data effortlessly. Upload your datasets and explore insightful visualizations.
    </p>
    """,
    unsafe_allow_html=True,
)

# Dashboard Layout with Columns
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

# Dashboard Features Section
st.markdown("### Key Features of the App")
features = [
    "Upload your dataset (CSV format).",
    "Generate insightful visualizations and Customize(scatter plots, bar charts, heatmaps, etc.).",
    "Handle missing data automatically.",
    "Download cleaned datasets for further analysis.",
]
for feature in features:
    st.markdown(f"- {feature}")

# Footer
st.markdown(
    """
    <footer style="
        text-align: center;
        font-size: 14px;
        margin-top: 50px;
        color: #777;
    ">
        
    </footer>
    """,
    unsafe_allow_html=True,
)
# Sidebar for uploading dataset
st.sidebar.header("📂 Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

# Initialize session state for dataset
if "df" not in st.session_state:
    st.session_state["df"] = None

# Load and update dataset
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.session_state["df"] = df  # Store dataset in session state

# Show dataset preview if a file is uploaded
if st.session_state["df"] is not None:
    df = st.session_state["df"]  # Access dataset from session state

    # Display Uncleaned Dataset
    st.subheader("🗂️ Dataset Preview")
    st.dataframe(df.head(10), height=200)

    # Dataset Cleaning
    st.subheader("🧹 Dataset Cleaning")
    st.write("Automatically handling missing or invalid values for better analysis.")
    
    df_cleaned = df.copy()  # Make a copy for cleaning
    # Handling missing values
    if df.isnull().sum().sum() > 0:
        st.warning("Your dataset contains missing values. Cleaning them...")
        df_cleaned.fillna(df_cleaned.mean(numeric_only=True), inplace=True)  # Fill numeric missing values with mean
        df_cleaned.fillna("Unknown", inplace=True)  # Fill non-numeric missing values with 'Unknown'
        st.success("✅ Missing values handled successfully!")
    else:
        st.success("✅ No missing values found.")

    # Show Cleaned Dataset Preview
    st.subheader("🗂️ Cleaned Dataset Preview")
    st.dataframe(df_cleaned.head(10), height=200)

    # Dataset Difference
    st.subheader("📊 Dataset Comparison")
    st.write("Below is the difference between the uncleaned and cleaned dataset.")
    st.write(f"**🔍 Missing values before cleaning:** {df.isnull().sum().sum()}")
    st.write(f"**🔍 Missing values after cleaning:** {df_cleaned.isnull().sum().sum()}")

    # Download Cleaned Dataset
    st.subheader("📥 Download Cleaned Dataset")
    buffer = BytesIO()
    df_cleaned.to_csv(buffer, index=False)
    st.download_button(
        label="Download Cleaned Dataset",
        data=buffer.getvalue(),
        file_name="cleaned_dataset.csv",
        mime="text/csv",
    )

    # Show Dataset Head, Tail, Info, and Object Description
    st.subheader("🔍 Dataset Information")

    # Display the first few rows (Head) of the cleaned dataset
    st.subheader("📑 Dataset Head")
    st.dataframe(df_cleaned.head(10), height=200)

    # Display the last few rows (Tail) of the cleaned dataset
    st.subheader("📑 Dataset Tail")
    st.dataframe(df_cleaned.tail(10), height=200)

    # Assuming this part of the code is before the line where you use categorical_columns
    categorical_columns = df_cleaned.select_dtypes(include=['object']).columns.tolist()

    # Show summary statistics for object columns
    st.subheader("📝 Object Columns Summary")
    if len(categorical_columns) > 0:
        st.write(df_cleaned.describe(include=['object']))
    else:
        st.write("No categorical columns available to describe.")

    # Show dataset information
    st.subheader("📝 Basic Information")
    st.write(f"**Number of rows:** {df_cleaned.shape[0]}")
    st.write(f"**Number of columns:** {df_cleaned.shape[1]}")
    st.write("**Columns and Data Types:**")
    st.write(df_cleaned.dtypes)

    # Show summary statistics
    st.subheader("📈 Summary Statistics")
    st.write(df_cleaned.describe())

# Data Visualizations
if st.session_state["df"] is not None:
    st.subheader("📊 Data Visualizations")

    # Select numeric and categorical columns after cleaning
    numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = df_cleaned.select_dtypes(include=['object']).columns.tolist()

    if len(numeric_columns) > 0 or len(categorical_columns) > 0:
        st.sidebar.subheader("⚙️ Visualization Settings")

        # Scatter Plot
        st.sidebar.subheader("📉 Scatter Plot")
        x_axis = st.sidebar.selectbox("X-Axis", options=numeric_columns, key="scatter_x")
        y_axis = st.sidebar.selectbox("Y-Axis", options=numeric_columns, key="scatter_y")
        if st.sidebar.button("Generate Scatter Plot"):
            st.subheader("📉 Scatter Plot")
            fig, ax = plt.subplots()
            sns.scatterplot(data=df_cleaned, x=x_axis, y=y_axis, ax=ax)
            st.pyplot(fig)

        # Bar Plot
        st.sidebar.subheader("📊 Bar Chart")
        bar_col = st.sidebar.selectbox("Bar Chart Column", options=df_cleaned.columns, key="bar_col")
        if st.sidebar.button("Generate Bar Chart"):
            st.subheader("📊 Bar Chart")
            fig, ax = plt.subplots()
            if pd.api.types.is_numeric_dtype(df_cleaned[bar_col]):
                df_cleaned[bar_col].plot(kind='hist', bins=20, ax=ax, color="skyblue", edgecolor="black")
                ax.set_xlabel(bar_col)
                ax.set_ylabel("Frequency")
                ax.set_title(f"Histogram of {bar_col}")
            else:
                df_cleaned[bar_col].value_counts().plot(kind='bar', ax=ax, color="skyblue", edgecolor="black")
                ax.set_xlabel(bar_col)
                ax.set_ylabel("Count")
                ax.set_title(f"Bar Chart of {bar_col}")
            st.pyplot(fig)

        # Pie Chart
        st.sidebar.subheader("🍰 Pie Chart")
        if len(categorical_columns) > 0:
            pie_col = st.sidebar.selectbox("Pie Chart Column", options=categorical_columns, key="pie_col")
            if st.sidebar.button("Generate Pie Chart"):
                st.subheader(f"🍰 Pie Chart of {pie_col}")
                if df_cleaned[pie_col].nunique() <= 20:
                    fig, ax = plt.subplots()
                    df_cleaned[pie_col].value_counts().plot(
                        kind='pie',
                        autopct='%1.1f%%',
                        startangle=90,
                        ax=ax,
                        colors=sns.color_palette("pastel"),
                    )
                    ax.set_ylabel("")
                    ax.set_title(f"Pie Chart of {pie_col}")
                    st.pyplot(fig)
                else:
                    st.warning("The selected column has too many unique values for a pie chart. Please select a column with fewer categories.")
        else:
            st.sidebar.info("No categorical columns available for a pie chart.")

        # Heatmap
        if st.sidebar.button("Generate Heatmap"):
            st.subheader("🔵 Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(df_cleaned[numeric_columns].corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

        # Box Plot
        st.sidebar.subheader("📦 Box Plot")
        if len(numeric_columns) > 0:
            box_col = st.sidebar.selectbox("Box Plot Column", options=numeric_columns, key="box_col")
            if st.sidebar.button("Generate Box Plot"):
                st.subheader(f"📦 Box Plot of {box_col}")
                fig, ax = plt.subplots()
                sns.boxplot(data=df_cleaned, x=box_col, ax=ax)
                st.pyplot(fig)

        # Line Chart
        st.sidebar.subheader("📈 Line Chart")
        if len(numeric_columns) > 0:
            line_col = st.sidebar.selectbox("Line Chart Column", options=numeric_columns, key="line_col")
            if st.sidebar.button("Generate Line Chart"):
                st.subheader(f"📈 Line Chart of {line_col}")
                fig, ax = plt.subplots()
                df_cleaned[line_col].plot(kind='line', ax=ax, color="skyblue", lw=2)
                ax.set_ylabel(line_col)
                ax.set_title(f"Line Chart of {line_col}")
                st.pyplot(fig)