import streamlit as st
import cloudscraper
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="🎰 Slot Info Finder", layout="centered")
st.title("🎰 Slot Info from Slotstemple")

# Helper to slugify game name to URL format
def slugify(name):
    name = name.lower()
    name = re.sub(r"[^\w\s-]", "", name)  # Remove punctuation
    name = re.sub(r"[\s_-]+", "-", name)  # Replace spaces/underscores with hyphens
    name = name.strip("-")
    return name

# Scrape data using cloudscraper to bypass 403
def get_slot_data(url):
    scraper = cloudscraper.create_scraper()
    try:
        res = scraper.get(url)
    except Exception as e:
        st.error(f"Request failed: {e}")
        return None

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

# Input UI
game_name = st.text_input("Enter the slot game name", value="Eye of Medusa")

if st.button("Get Slot Info"):
    slug = slugify(game_name)
    url = f"https://www.slotstemple.com/free-slots/{slug}/"
    st.markdown(f"🔗 **Fetching**: [{url}]({url})")

    data = get_slot_data(url)
    if data:
        st.success("✅ Data found!")
        st.markdown("### 🎯 Game Info")
        for key, value in data.items():
            st.write(f"**{key}**: {value}")
    else:
        st.warning("⚠️ No data found or slot page structure has changed.")
