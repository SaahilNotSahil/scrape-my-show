import os

import dateparser
import pandas as pd
import streamlit as st

from utils.date import format_date

st.set_page_config(page_title="ScrapeMyShow", layout="centered")


@st.cache_data
def load_data():
    data = []
    data_files = os.listdir("./data")
    for file in data_files:
        if file.endswith(".csv"):
            data.append(pd.read_csv(f"./data/{file}"))

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


df = load_data()

st.title("ScrapeMyShow")
st.write("Events Data")
st.write(df)
