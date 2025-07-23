# app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("🎰 SlotCatalog Data Extractor")

url = st.text_input("Enter SlotCatalog Slot URL:", "https://slotcatalog.com/en/slots/eye-of-medusa")

def get_slot_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    result = {}
    for dt in soup.select("dl.slot__params dt"):
        label = dt.get_text(strip=True)
        dd = dt.find_next_sibling("dd")
        value = dd.get_text(strip=True) if dd else ""
        result[label] = value

    return result

if st.button("Fetch Data"):
    try:
        data = get_slot_data(url)
        st.success("Data fetched successfully!")
        st.write("## Slot Info:")
        for key in ["Provider", "RTP", "Min bet ($,€)", "Release date", "Max bet ($,€)"]:
            st.write(f"**{key}**: {data.get(key, 'N/A')}")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
