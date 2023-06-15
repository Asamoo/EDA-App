import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_bool_dtype


def main():
    st.title("CSV File Analyzer")

    st.header("Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.header("Data Frame")
        st.dataframe(df)

        st.header("File Summary")
        st.write("Number of rows:", df.shape[0])
        st.write("Number of columns:", df.shape[1])

    def count_numeric_columns(df):
        numeric_columns = [col for col in df.columns if is_numeric_dtype(df[col])]
        return len(numeric_columns)
    
    def count_logical_columns(df):
        logical_columns = [col for col in df.columns if is_bool_dtype(df[col])]
        return len(logical_columns)
    
    def count_string_columns(df):
        string_columns = [col for col in df.columns if is_string_dtype(df[col])]
        return len(string_columns)
    
    numerical_count = count_numeric_columns(df)
    logical_count = count_logical_columns(df)
    string_count = count_string_columns(df)
    
    st.write("Number of columns displaying numerical values:", numerical_count)
    st.write("Number of columns displaying logical values:", logical_count)
    st.write("Number of columns displaying string values:", string_count)

    st.header("Column Summary")

    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    title = st.text_input('Choose a column you would like summarized.')
    if title in df.columns:
        if pd.api.types.is_numeric_dtype(df[title]):
            st.header("Five-Number Summary")
            column_summary = df[title].describe()
            st.write(column_summary)
            sns.kdeplot(data=df, x=title, fill=True, bw = 0.005)
            st.pyplot(plt)
        elif pd.api.types.is_string_dtype(df[title]):
            category_proportions = df[title].value_counts(normalize = True).reset_index()
            category_proportions.columns = ["Category", "Proportion"]
            st.dataframe(category_proportions)
            plt.bar(category_proportions["Category"], category_proportions["Proportion"])
            plt.xlabel("Category")
            plt.ylabel("Proportion")
            plt.xticks(rotation=90)
            st.pyplot(plt)
        else:
            st.write("Error: Column name not recognized. Please enter a valid column name.")


if __name__ == "__main__":
    main()

