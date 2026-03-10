import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="SQL Data Explorer", layout="wide")

st.title("SQL Data Explorer")

# -----------------------------
# Database Connection
# -----------------------------

conn = sqlite3.connect("data.db")

# -----------------------------
# Upload CSV
# -----------------------------

uploaded_file = st.file_uploader("solar_pv.csv", type="csv")

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    # Save dataset to SQL table
    df.to_sql("data_table", conn, if_exists="replace", index=False)

    st.success("Dataset loaded into SQL database")

# -----------------------------
# Show Tables
# -----------------------------

st.subheader("Available Tables")

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
)

st.dataframe(tables)

# -----------------------------
# Table Preview
# -----------------------------

if len(tables) > 0:

    table_name = st.selectbox(
        "Select Table",
        tables["name"]
    )

    preview_query = f"SELECT * FROM {table_name} LIMIT 10"

    preview_df = pd.read_sql(preview_query, conn)

    st.subheader("Table Preview")

    st.dataframe(preview_df)

# -----------------------------
# SQL Query Editor
# -----------------------------

st.subheader("Write SQL Query - ")

query = st.text_area(
    "Enter SQL Query - (table name = data_table)",
    height=150,
    placeholder="Example: SELECT * FROM data_table LIMIT 10"
)

# -----------------------------
# Run Query
# -----------------------------

if st.button("Run Query"):

    try:

        result = pd.read_sql(query, conn)

        st.success("Query executed successfully")

        st.subheader("Query Result")

        st.dataframe(result)

        # -----------------------------
        # Chart Visualization
        # -----------------------------

        if len(result.columns) >= 2:

            st.subheader("Visualization")

            chart_type = st.selectbox(
                "Select Chart Type",
                ["Bar Chart", "Line Chart"]
            )

            if chart_type == "Bar Chart":
                st.bar_chart(result)

            if chart_type == "Line Chart":
                st.line_chart(result)

        # -----------------------------
        # Download Results
        # -----------------------------

        csv = result.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Result as CSV",
            csv,
            "query_result.csv",
            "text/csv"
        )

    except Exception as e:

        st.error(f"Error: {e}")

# -----------------------------
# Footer
# -----------------------------

st.markdown("---")
st.markdown("Built with Streamlit")
