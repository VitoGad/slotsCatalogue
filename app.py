import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.title("🎰 Slotstemple Slot Info (No Search Needed)")

def slugify(name):
    name = name.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_-]+", "-", name)
    name = name.strip("-")
    return name

def get_slot_data(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        st.error(f"Failed to fetch slot page (status {res.status_code})")
        return None

    soup = BeautifulSoup(res.text, "html.parser")
    rows = soup.select("tbody tr.game-info-table-row")

    data = {}
    for row in rows:
        label = row.find("th").get_text(strip=True)
        td = row.find("td")
        if label == "Software:":
            a = td.find("a")
            data["Game Provider"] = a.get_text(strip=True) if a else td.get_text(strip=True)
        elif label == "RTP:":
            data["RTP"] = td.get_text(strip=True)
        elif label == "Min Bet (all lines covered):":
            data["Min Bet"] = td.get_text(strip=True)

    return data

# Input form
game_name = st.text_input("Enter slot game name", "Eye of Medusa")

if st.button("Get Slot Info"):
    slug = slugify(game_name)
    url = f"https://www.slotstemple.com/free-slots/{slug}/"
    st.write(f"🔗 Checking: {url}")

    data = get_slot_data(url)
    if data:
        st.success("Slot data retrieved!")
        for k, v in data.items():
            st.write(f"**{k}**: {v}")
    else:
        st.warning("Slot not found or data missing.")
