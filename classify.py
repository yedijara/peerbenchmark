import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Load data
df = pd.read_csv("peer_benchmark_cleaned.csv")

# Sidebar input
selected_region = st.selectbox("Pilih Kabupaten/Kota", df["Kabupaten / Kota"].unique())
selected_row = df[df["Kabupaten / Kota"] == selected_region].iloc[0]

# Tampilkan profil wilayah
st.markdown(f"""
## 📍 Profil: {selected_row['Kabupaten / Kota']}
- Provinsi: {selected_row['Provinsi']}
- Ekonomi: **{selected_row['Ekonomi Sejahtera']}**
- Wilayah: **{selected_row['Mayoritas Wilayah']}**
- AFI: **{selected_row['AFI']}**
- UFI: **{selected_row['UFI']}**
- Sebaran Ekonomi: **{selected_row['Sebaran Aktivitas Ekonomi']}**
""")

# Cari peer group
peers = df[
    (df["Ekonomi Sejahtera"] == selected_row["Ekonomi Sejahtera"]) &
    (df["Mayoritas Wilayah"] == selected_row["Mayoritas Wilayah"]) &
    (df["AFI"] == selected_row["AFI"]) &
    (df["UFI"] == selected_row["UFI"]) &
    (df["Sebaran Aktivitas Ekonomi"] == selected_row["Sebaran Aktivitas Ekonomi"])
]

st.markdown("## 🤝 Wilayah Serumpun:")
st.dataframe(peers[["Provinsi", "Kabupaten / Kota"]])

# Peta peer group (dummy lat/lon generator for demo)
import hashlib
import random

def dummy_lat_lon(name):
    seed = int(hashlib.sha256(name.encode('utf-8')).hexdigest(), 16)
    random.seed(seed)
    return -2 + random.random() * 8, 95 + random.random() * 25

m = folium.Map(location=[-2, 118], zoom_start=5)

for _, row in peers.iterrows():
    lat, lon = dummy_lat_lon(row["Kabupaten / Kota"])
    popup = f"{row['Kabupaten / Kota']} ({row['Provinsi']})"
    color = "red" if row["Kabupaten / Kota"] == selected_region else "blue"
    folium.Marker(location=[lat, lon], popup=popup, icon=folium.Icon(color=color)).add_to(m)

st.markdown("## 🗺️ Peta Wilayah Serumpun")
st_folium(m, width=700)
