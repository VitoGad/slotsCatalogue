import streamlit as st
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def search_slots(query):
    search_url = f"https://www.bigwinboard.com/?s={query.replace(' ', '+')}"
    res = requests.get(search_url, headers=HEADERS)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    results = []
    for post in soup.select("article.post"):
        title_tag = post.select_one("h2.entry-title a")
        snippet_tag = post.select_one("div.entry-content")
        if title_tag and snippet_tag:
            results.append({
                "title": title_tag.text.strip(),
                "url": title_tag['href'],
                "snippet": snippet_tag.text.strip()
            })
    return results

def scrape_slot_details(url):
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    # Initialize details dict
    details = {
        "Game Provider": "N/A",
        "RTP": "N/A",
        "Min Bet": "N/A"
    }

    # Search for Game Provider (usually inside .game-provider or similar)
    provider_tag = soup.find(string="Software:")
    if provider_tag:
        # Provider is next <a> tag or sibling
        provider = provider_tag.find_next('a')
        if provider:
            details["Game Provider"] = provider.text.strip()

    # Search for RTP (look for "RTP:" string)
    rtp_tag = soup.find(string="RTP:")
    if rtp_tag:
        rtp_value = rtp_tag.find_next(text=True)
        if rtp_value:
            details["RTP"] = rtp_value.strip()

    # Search for Min Bet (look for "Min Bet" string)
    min_bet_tag = soup.find(string=lambda t: t and "Min Bet" in t)
    if min_bet_tag:
        min_bet_value = min_bet_tag.find_next(text=True)
        if min_bet_value:
            details["Min Bet"] = min_bet_value.strip()

    return details

def main():
    st.title("Bigwinboard Slot Search")

    query = st.text_input("Enter slot game name", "")

    if query:
        st.write(f"Searching for: **{query}**")
        try:
            results = search_slots(query)
            if not results:
                st.write("No results found.")
                return
            for idx, res in enumerate(results):
                st.subheader(f"{res['title']}")
                st.write(res['snippet'])
                st.markdown(f"[Open Slot Page]({res['url']})")

                if st.button(f"Get details for '{res['title']}'", key=f"btn_{idx}"):
                    with st.spinner("Fetching slot details..."):
                        details = scrape_slot_details(res['url'])
                    st.json(details)

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
