import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("benchmark_data_for_streamlit.csv")

df = load_data()

# Sidebar selections
st.sidebar.title("Peer Benchmarking Tool")
selected_view = st.sidebar.radio("Pilih Mode", [
    "Peer Benchmarking by Inclusion",
    "Peer Benchmarking by Utilization",
    "Peer Benchmarking by Welfare / Economy"
])

selected_region = st.sidebar.selectbox("Pilih Kabupaten/Kota", df["Kabupaten / Kota"].unique())

# Fetch selected region data
region = df[df["Kabupaten / Kota"] == selected_region].iloc[0]

# Display region profile
st.header(f"Profil Wilayah: {region['Kabupaten / Kota']}")

with st.expander("📊 Statistik Wilayah Ini"):
    st.markdown(f"""
    - **AFI:** {region['AFI - Inklusi Keuangan']} (**{region['Klasifikasi AFI']}**)
    - **D1:** {region['D1 - Penetrasi']} (**{region['Klasifikasi D1']}**)
    - **D2:** {region['D2 - Ketersediaan']} (**{region['Klasifikasi D2']}**)
    - **D3:** {region['D3 - Penggunaan']} (**{region['Klasifikasi D3']}**)
    - **UFI:** {region['UFI - Utilisasi Keuangan']} (**{region['Klasifikasi UFI']}**)
    - **PDRB Per Kapita:** Rp{int(region['PDRB Per kapita\n(Rp)']):,} (**{region['Klasifikasi PDRB']}**)
    - **IPM:** {region['IPM']} (**{region['Klasifikasi IPM']}**)
    - **Tingkat Kemiskinan:** {region['Tingkat Kemiskinan']}% (**{region['Klasifikasi Kemiskinan']}**)
    - **Mayoritas Wilayah:** {region['Mayoritas Wilayah']}
    - **IDSD Institusi:** {region['IDSD - Institusi']}
    - **IDSD Infrastruktur:** {region['IDSD - Infrastruktur']}
    - **IDSD Adopsi TIK:** {region['IDSD - Adopsi TIK']}
    - **IDSD Kesehatan:** {region['IDSD - Kesehatan']}
    - **IDSD Komposit:** {region['IDSD Komposit']} (**{region['Klasifikasi IDSD']}**)
    """)

# Determine peers based on selected view
if selected_view == "Peer Benchmarking by Inclusion":
    peers = df[df["Klasifikasi AFI"] == region["Klasifikasi AFI"]]
elif selected_view == "Peer Benchmarking by Utilization":
    peers = df[df["Klasifikasi UFI"] == region["Klasifikasi UFI"]]
else:  # Welfare / Economy
    peers = df[
        (df["Klasifikasi IPM"] == region["Klasifikasi IPM"]) &
        (df["Klasifikasi Kemiskinan"] == region["Klasifikasi Kemiskinan"]) &
        (df["Klasifikasi PDRB"] == region["Klasifikasi PDRB"]) &
        (df["Klasifikasi IDSD"] == region["Klasifikasi IDSD"])
    ]

# Show peer average stats
st.subheader("📈 Rata-rata Statistik Peer Group")
peer_avg = peers[[
    "AFI - Inklusi Keuangan", "D1 - Penetrasi", "D2 - Ketersediaan", "D3 - Penggunaan",
    "UFI - Utilisasi Keuangan", "IPM", "Tingkat Kemiskinan", "PDRB Per kapita\n(Rp)",
    "IDSD - Institusi", "IDSD - Infrastruktur", "IDSD - Adopsi TIK", "IDSD - Kesehatan", "IDSD Komposit"
]].mean()

st.dataframe(peer_avg.rename("Rata-rata Peer Group"))
