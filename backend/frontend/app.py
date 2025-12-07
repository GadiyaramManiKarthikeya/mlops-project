# frontend/app.py
import streamlit as st
import requests
import os

st.set_page_config(page_title="Recommendation Demo", layout="centered")
st.title("Recommendation UI — AI Fashion Designer (Demo)")

# Backend URL - change when deployed
backend_url = st.text_input("Backend base URL (include http:// or https://)", value=os.getenv("BACKEND_URL","http://localhost:8000"))
st.write("Backend:", backend_url)

user_id = st.number_input("Enter user id", min_value=1, max_value=10000, value=1)
if st.button("Get Recommendations"):
    try:
        payload = {"user_id": int(user_id), "context_data": {}}
        r = requests.post(f"{backend_url.rstrip('/')}/recommend", json=payload, timeout=10)
        if r.status_code == 200:
            data = r.json()
            st.subheader("Recommendations")
            for i, item in enumerate(data.get("recommendations", []), start=1):
                st.write(f"{i}. {item}")
            st.write(f"Latency: {data.get('latency_ms', 'n/a')} ms")
        else:
            st.error(f"API returned {r.status_code}: {r.text}")
    except Exception as e:
        st.error(f"Failed to call backend: {e}")
