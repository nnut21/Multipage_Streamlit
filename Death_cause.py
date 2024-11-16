import streamlit as st
import pandas as pd
import numpy as np
st.title("Death Cause Analysis")
#@st.cache_data
#def load_data():
#    return pd.read_csv("https://raw.githubusercontent.com/nnut21/Project_Dads5001_Data/refs/heads/main/Data/cause_of_deaths.csv", index_col=0)
df_death = pd.read_csv("https://raw.githubusercontent.com/nnut21/Project_Dads5001_Data/refs/heads/main/Data/cause_of_deaths.csv", index_col=0)
st.header("First Dataset")
st.write("`st.data_editor` allows us to display AND edit data")
st.data_editor(df_death)

st.divider()

st.header('Chart')
st.bar_chart(df_death[['Code','Year','Drug Use Disorders']], x='Code',y='Drug Use Disorders')

st.write('Interactive')
selected_year = st.selectbox("Select a year",list(df_death.Year.unique())[::-1])
if selected_year:
    df_selected_year = df_death[df_death.Year == selected_year]

    # Display chart
    st.bar_chart(df_selected_year,
                 x='Code',
                 y='Drug Use Disorders')