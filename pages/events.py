import streamlit as st
import json
import requests
from datetime import datetime


if "token" not in st.session_state:
    st.warning("Please login to access the Event Finder.")
    st.stop()


with open("country.json", "r", encoding="utf-8") as f:
    country_to_code = json.load(f)


st.title("🎫 Event Finder")


selected_country = st.selectbox("Select the country you're visiting:", list(country_to_code.keys()))
country_code = country_to_code[selected_country]


start_date = st.date_input("Start Date", datetime.today())
end_date = st.date_input("End Date", datetime.today())


city = st.text_input("City")
keyword = st.text_input("Keyword")


if st.button("🔍 Find Events"):
    API_KEY = 'UTyo7nQKhQYdVcPIkklAxyWqQdddvQOE'
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'

    start_date_iso = f"{start_date}T00:00:00Z"
    end_date_iso = f"{end_date}T23:59:59Z"

    params = {
        'apikey': API_KEY,
        'keyword': keyword,
        'city': city,
        'countryCode': country_code,
        'size': 100,
        'startDateTime': start_date_iso,
        'endDateTime': end_date_iso
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")
        st.stop()

    events = data.get('_embedded', {}).get('events', [])

    if not events:
        st.warning("No events found.")
        st.rerun()
    else:
        st.session_state["events_data"] = events  # 🔐 Store in session
        st.session_state["search_done"] = True
        st.rerun()

# ✅ After search: Display and allow favoriting
if st.session_state.get("search_done"):
    events = st.session_state.get("events_data", [])

    for i, event in enumerate(events):
        name = event.get('name')
        local_date = event.get('dates', {}).get('start', {}).get('localDate')
        local_time = event.get('dates', {}).get('start', {}).get('localTime') or "00:00:00"
        url_link = event.get('url')
        images = event.get('images', [])
        image_url = images[0].get('url') if images else None
        event_id = event.get('id')

        st.subheader(name)
        st.write(f"📅 Date: {local_date}")
        st.write(f"⏰ Time: {local_time}")
        if url_link:
            st.write(f"[🔗 Ticket URL]({url_link})")
        if image_url:
            st.image(image_url, width=300)

        # Create a key for the button to persist its state
        fav_key = f"fav_clicked_{event_id}"
        if fav_key not in st.session_state:
            st.session_state[fav_key] = False

        # ⭐ Favorite button logic
        if not st.session_state[fav_key]:
            if st.button(f"⭐ Favorite", key=event_id):
                token = st.session_state["token"]
                headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
                json_data = {
                    "event_id": event_id,
                    "name": name,
                    "url": url_link,
                    "date": f"{local_date}T{local_time}",
                    "image_url": image_url
                }

                try:
                    res = requests.post("https://eventfinderapplicationbackend.onrender.com/mark_favorite", headers=headers, json=json_data)
                    if res.status_code == 200:
                        st.success("✅ Favorited!")
                        st.session_state[fav_key] = True  # Mark as clicked
                        st.rerun()
                    elif res.status_code == 400:
                        st.warning("Favorited.")
                        st.session_state[fav_key] = True
                        st.rerun()
                    else:
                        st.error("❌ Error favoriting.")
                except Exception as e:
                    st.error(f"🚨 Error: {e}")
        else:
            st.info("Favorited.")

        st.markdown("---")
