import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("peer_benchmark_cleaned.csv")

# Sidebar input
selected_region = st.selectbox("Pilih Kabupaten/Kota", df["Kabupaten / Kota"].unique())
selected_row = df[df["Kabupaten / Kota"] == selected_region].iloc[0]

# Show profile
st.markdown(f"""
## 📍 Profil: {selected_row['Kabupaten / Kota']}
- Provinsi: {selected_row['Provinsi']}
- Ekonomi: **{selected_row['Ekonomi Sejahtera']}**
- Wilayah: **{selected_row['Mayoritas Wilayah']}**
- AFI: **{selected_row['AFI']}**
- UFI: **{selected_row['UFI']}**
- Sebaran Ekonomi: **{selected_row['Sebaran Aktivitas Ekonomi']}**
""")

# Find peers
peers = df[
    (df["Ekonomi Sejahtera"] == selected_row["Ekonomi Sejahtera"]) &
    (df["Mayoritas Wilayah"] == selected_row["Mayoritas Wilayah"]) &
    (df["AFI"] == selected_row["AFI"]) &
    (df["UFI"] == selected_row["UFI"]) &
    (df["Sebaran Aktivitas Ekonomi"] == selected_row["Sebaran Aktivitas Ekonomi"])
]

st.markdown("## 🤝 Wilayah Serumpun:")
st.dataframe(peers[["Provinsi", "Kabupaten / Kota"]])

