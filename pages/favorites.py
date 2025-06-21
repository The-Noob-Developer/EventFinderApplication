import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="⭐ Favorites")

# 🛡️ Require login
if "token" not in st.session_state:
    st.warning("Please log in to view your favourite events.")
    st.stop()

API_BASE = "https://eventfinderbackend.onrender.com"  # ← change if your backend lives elsewhere


@st.cache_data(show_spinner=False, ttl=60)  # 1‑min cache
def fetch_favorites(token: str):
    """Call FastAPI to retrieve the current user’s favourites."""
    try:
        r = requests.get(
            f"{API_BASE}/favorites",
            headers={"Authorization": f"Bearer {token}"}
        )
        r.raise_for_status()
        return r.json()                # → list[dict]
    except requests.exceptions.RequestException as exc:
        st.error(f"Could not fetch favourites 😕\n\n{exc}")
        return []


favorites = fetch_favorites(st.session_state["token"])

st.title("⭐ My Favourite Events")

if not favorites:
    st.info("You haven’t marked any events as favourite yet.")
else:
    for fav in favorites:
        # Each favourite in its own nicely bordered container
        with st.container(border=True):
            col_img, col_info = st.columns([1, 3], gap="large")

            # 📸 Image (if available)
            with col_img:
                if fav.get("image_url"):
                    st.image(fav["image_url"], use_container_width=True)
                else:
                    st.empty()

            # ℹ️  Event details
            with col_info:
                st.subheader(fav["name"])
                if fav.get("date"):
                    try:
                        dt = datetime.fromisoformat(fav["date"])
                        st.markdown(f"**Date:** {dt:%d %b %Y, %I:%M %p}")
                    except ValueError:
                        st.markdown(f"**Date:** {fav['date']}")
                st.markdown(f"[🔗 Event Link]({fav['url']})")

                # --- Optional: “Remove” button (uncomment if you implement endpoint) ---
                # if st.button("Remove from favourites", key=f"rem-{fav['id']}"):
                #     remove_favourite(fav["id"])
                # ---------------------------------------------------------------------

st.divider()
st.markdown(
    "Head back to **Event Finder** to discover more events and mark them as favourites."
)