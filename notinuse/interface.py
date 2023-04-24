import streamlit as st
import pandas as pd
from WebScraping import WebScraping
from User import User


# This function takes in the input csv file given by the user, and returns the filled out csv
def get_info(data): 
    #TODO
    return False

st.title('Virginia Tech Advanced Research Corperation Web Scraping Tool')
search_file = st.file_uploader("Researcher and Institution File")


if search_file is not None:
    data = pd.read_csv(search_file)
    out_data = get_info(data)

st.header('Output csv file')
'''
out_data = pd.read_csv('output.csv')
st.write(out_data)
'''

data_as_csv= out_data.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download data as CSV", 
    data_as_csv, 
    "researcher_data.csv",
    "text/csv",
    key="download-tools-csv",
)
