import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

st.title("🎰 Slotstemple Slot Data Extractor (Search by Game Name)")

game_name = st.text_input("Enter Slot Game Name:", "eye of medusa")

def search_game_url(game_name):
    query = quote_plus(game_name)
    search_url = f"https://www.slotstemple.com/?s={query}&post_type=slots"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(search_url, headers=headers)
    if res.status_code != 200:
        st.error(f"Search failed with status {res.status_code}")
        return None

    soup = BeautifulSoup(res.text, "html.parser")
    # Find the first search result link under <h2 class="entry-title">
    h2 = soup.find("h2", class_="entry-title")
    if h2 and h2.a:
        return h2.a["href"]
    else:
        return None

def get_slot_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        st.error(f"Failed to retrieve page, status code: {res.status_code}")
        return None
    
    soup = BeautifulSoup(res.text, "html.parser")
    rows = soup.select("tbody tr.game-info-table-row")
    
    data = {}
    for row in rows:
        label = row.find("th", class_="game-info-table-column").get_text(strip=True)
        td = row.find("td", class_="game-info-table-column")
        
        if label == "Software:":
            a = td.find("a")
            data["Game Provider"] = a.get_text(strip=True) if a else td.get_text(strip=True)
        elif label == "RTP:":
            data["RTP"] = td.get_text(strip=True)
        elif label == "Min Bet (all lines covered):":
            data["Min Bet"] = td.get_text(strip=True)

    return data

if st.button("Search and Fetch Data"):
    if not game_name.strip():
        st.error("Please enter a game name.")
    else:
        url = search_game_url(game_name)
        if url:
            st.write(f"Found game URL: {url}")
            slot_data = get_slot_data(url)
            if slot_data:
                st.success("Data fetched successfully!")
                for key, val in slot_data.items():
                    st.write(f"**{key}**: {val}")
            else:
                st.warning("Could not find slot data on the page.")
        else:
            st.warning("No results found for your search.")
