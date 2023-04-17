import json
import os

import dateparser
import pandas as pd
import streamlit as st

from utils import format_date

st.set_page_config(page_title="ScrapeMyShow", layout="centered")


@st.cache_data(ttl=1800.00)
def load_data():
    data = []
    data_files = os.listdir("./data")
    for file in data_files:
        if file.endswith(".csv"):
            df = pd.read_csv(f"./data/{file}")

            if not df.empty:
                data.append(df)

    df = pd.concat(data, axis=0)
    df = df.dropna(axis=0)
    df = df.astype(str)

    df['date'] = df['date'].apply(lambda x: str(dateparser.parse(x)))
    df = df.sort_values(by='date', ascending=True)
    df['date'] = df['date'].apply(format_date)

    df = df[['date', 'name', 'link']]
    df.rename(columns={'date': 'Date', 'name': 'Name',
              'link': 'Link'}, inplace=True)
    df.index = pd.Index(range(1, len(df) + 1))

    return df


@st.cache_data
def get_base_urls():
    f = open("base_urls.json", "r")
    base_urls = json.load(f)
    f.close()

    return base_urls


df = load_data()
base_urls = get_base_urls()

st.title("ScrapeMyShow")
st.write("Events Data")

st.sidebar.title("Filter by Date")
date_options = df['Date'].unique().tolist()
date_options.insert(0, "All")
selected_date = st.sidebar.selectbox("Select Date", date_options)

st.sidebar.title("Filter by Website")
website_options = list(base_urls.keys())
website_options.insert(0, "All")
selected_site = str(st.sidebar.selectbox("Select Site", website_options))

if selected_date == "All" and selected_site != "All":
    filtered_df = df[df['Link'].str.contains(base_urls[selected_site])]
    st.write(filtered_df)
elif selected_date != "All" and selected_site == "All":
    filtered_df = df[df['Date'] == selected_date]
    st.write(filtered_df)
elif selected_date != "All" and selected_site != "All":
    filtered_df = df[(df['Date'] == selected_date) & (
        df['Link'].str.contains(base_urls[selected_site]))]
    st.write(filtered_df)
else:
    st.write(df)
