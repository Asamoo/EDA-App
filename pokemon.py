import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_bool_dtype


def main():
    st.title("Application for Exploratory Data Analysis of Two Variables")

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

    st.header("Column Summaries")

    col1 = st.text_input('Choose a column you would like summarized.')
    col2 = st.text_input('Choose a second column you would like summarized.')

    if col1 in df.columns and col2 in df.columns:
        is_col1_numeric = pd.api.types.is_numeric_dtype(df[col1])
        is_col2_numeric = pd.api.types.is_numeric_dtype(df[col2])
        
        if is_col1_numeric and is_col2_numeric:
            summary1 = df[col1].describe()
            summary2 = df[col2].describe()

            st.write(f"Five Number Summary of {col1}:")
            st.write(summary1)

            st.write(f"Five Number Summary of {col2}:")
            st.write(summary2)

            st.header("Density Graph with Marginal Density Plots for Corresponding Variables")
            sns.jointplot(x=df[col1], y=df[col2], shade=True, kind="kde", cmap="coolwarm", marginal_kws=dict(color = "indigo", shade=True))
            st.pyplot(plt)

            st.write("The above graph shows the correlation between two variables. A density graph was used to prevent overplotting. Dark red indicates a greater density, while dark blue indicates sparser. There are density plots in the margins showing the distributions of the variables.")
        elif is_col1_numeric:
            summary1 = df[col1].describe()

            st.write(f"Five Number Summary of {col1}:")
            st.write(summary1)

            proportions2 = df[col2].value_counts(normalize=True)

            st.write(f"Proportions of {col2}:")
            st.write(proportions2)

            st.header("Categorized Violin Graph")
            plt.figure(figsize=(10, 6))
            sns.violinplot(data=df, x=col1, y=col2, color='goldenrod', edgecolor="black")
            plt.title(f"{col1}")
            st.pyplot(plt)

            st.write("The above graph gives five number summary values on the lines, where the median is indicated by a white dot and the quartiles are given by the ends of the center lines. Each plot has surrounding density plots to indicate the categorical frequency of a value without overplotting.")
        elif is_col2_numeric:
            summary2 = df[col2].describe()

            st.write(f"Five Number Summary of {col2}:")
            st.write(summary2)

            proportions1 = df[col1].value_counts(normalize=True)

            st.write(f"Proportions of {col1}:")
            st.write(proportions1)

            st.header("Categorized Violin Graph")
            plt.figure(figsize=(10, 6))
            sns.violinplot(data=df, x=col2, y=col1, color='mediumslateblue', edgecolor="crimson")
            plt.title(f"{col1}")
            st.pyplot(plt)

            st.write("The above graph gives five number summary values on the lines, where the median is indicated by a white dot and the quartiles are given by the ends of the center lines. Each plot has surrounding density plots to indicate the categorical frequency of a value without overplotting.")
        else:
            proportions1 = df[col1].value_counts(normalize=True, ascending=True)
            proportions2 = df[col2].value_counts(normalize=True)

            st.write(f"Proportions of {col1}:")
            st.write(proportions1)

            st.write(f"Proportions of {col2}:")
            st.write(proportions2)

            st.header("Categorical Bar Graphs")

            plt.figure(figsize=(10, 6))
            plt.subplot(1, 2, 1)
            proportions1.plot(kind='bar', color="whitesmoke", edgecolor="royalblue")
            plt.title(f"{col1}")

            plt.subplot(1, 2, 2)
            proportions2.plot(kind='bar', color="black", edgecolor="moccasin")
            plt.title(f"{col2}")

            st.pyplot(plt)

            st.write("The above two plots are bar graphs indicate the relative frequency of two separate categorical variables. The graphs use proportions to avoid crowding the graph with extreme values. The two graphs are also mirrored with ascending and descending values, respectively, as well as opposing color schemes. This was done because it looks totally wicked and the developer thought users would appreciate the visual spectacle.")
    else:
        st.write("Error: Column name not recognized. Please enter a valid column name.")


if __name__ == "__main__":
    main()

