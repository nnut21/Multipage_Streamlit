import streamlit as st
import pandas as pd
import numpy as np
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
st.title('Calculater')
#input box

st.write("Text_input")
X1 = st.number_input(label="X1:")
X2 = st.number_input(label="X2:")

ans = 0
 
if st.button(" result "):
    st.success(f"Answer = {X1 + X2}")
   