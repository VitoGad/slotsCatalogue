import streamlit as st
import requests
from bs4 import BeautifulSoup

# For Playwright
try:
    from playwright.sync_api import sync_playwright
    playwright_available = True
except ImportError:
    playwright_available = False

st.title("🎰 SlotCatalog Slot Data Extractor")

url = st.text_input("Enter SlotCatalog URL:", "https://slotcatalog.com/en/slots/eye-of-medusa")

use_playwright = st.checkbox("Use Playwright (headless browser, bypass Cloudflare)", value=False)

def get_html_requests(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    return response.text

def get_html_playwright(url):
    if not playwright_available:
        st.error("Playwright is not installed. Run 'pip install playwright' and 'playwright install'")
        return None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        html = page.content()
        browser.close()
    return html

def parse_slot_data(html):
    soup = BeautifulSoup(html, "html.parser")
    # Debug: show first 1000 chars of HTML
    st.text("Preview of HTML content:")
    st.code(html[:1000])

    data = {}
    for dt in soup.select("dl.slot__params dt"):
        label = dt.get_text(strip=True)
        dd = dt.find_next_sibling("dd")
        value = dd.get_text(strip=True) if dd else ""
        data[label] = value
    return data

if st.button("Fetch Data"):
    if not url.startswith("http"):
        st.error("Please enter a valid URL starting with http or https")
    else:
        try:
            if use_playwright:
                st.info("Fetching using Playwright (headless browser)...")
                html = get_html_playwright(url)
            else:
                st.info("Fetching using requests + BeautifulSoup...")
                html = get_html_requests(url)
            if html:
                slot_data = parse_slot_data(html)
                if slot_data:
                    st.success("Data fetched!")
                    keys = ["Provider", "RTP", "Min bet ($,€)", "Release date", "Max bet ($,€)"]
                    for key in keys:
                        st.write(f"**{key}**: {slot_data.get(key, 'N/A')}")
                else:
                    st.warning("Could not find slot info on the page.")
            else:
                st.error("Failed to retrieve page HTML.")
        except Exception as e:
            st.error(f"Error: {e}")

