import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("benchmark_data_for_streamlit.csv")

df = load_data()

# Helper for colored classification
def colored_text(label, value):
    color_map = {
        "Sangat Tinggi": "green",
        "Tinggi": "limegreen",
        "Sedang": "orange",
        "Rendah": "orangered",
        "Sangat Rendah": "red",
        "Tertinggal": "gray"
    }
    color = color_map.get(value, "black")
    return f"<span style='color:{color}'>{label}: {value}</span>"

# Klasifikasi Gini

def classify_gini(gini):
    if pd.isna(gini): return ""
    if gini < 0.2: return "Sangat Rendah"
    elif gini < 0.3: return "Rendah"
    elif gini < 0.4: return "Sedang"
    elif gini < 0.5: return "Tinggi"
    else: return "Sangat Tinggi"

# Sidebar selections
st.set_page_config(layout="wide")
st.markdown("<style>body { font-family: 'Arial'; font-size: 13px; }</style>", unsafe_allow_html=True)

st.sidebar.title("Peer Benchmarking Tool")
selected_view = st.sidebar.radio("Pilih Mode", [
    "Peer Benchmarking by Inclusion",
    "Peer Benchmarking by Utilization",
    "Peer Benchmarking by Welfare / Economy",
    "Inclusion + Welfare Economy",
    "Utilization + Welfare Economy"
])

selected_region = st.sidebar.selectbox("Pilih Kabupaten/Kota", df["Kabupaten / Kota"].unique())
region = df[df["Kabupaten / Kota"] == selected_region].iloc[0]

# Determine peers
if selected_view == "Peer Benchmarking by Inclusion":
    peers = df[df["Klasifikasi AFI"] == region["Klasifikasi AFI"]]
elif selected_view == "Peer Benchmarking by Utilization":
    peers = df[df["Klasifikasi UFI"] == region["Klasifikasi UFI"]]
elif selected_view == "Peer Benchmarking by Welfare / Economy":
    peers = df[
        (df["Klasifikasi PDRB"] == region["Klasifikasi PDRB"]) &
        (df["Klasifikasi IPM"] == region["Klasifikasi IPM"]) &
        (df["Klasifikasi Kemiskinan"] == region["Klasifikasi Kemiskinan"])
    ]
elif selected_view == "Inclusion + Welfare Economy":
    peers = df[
        (df["Klasifikasi AFI"] == region["Klasifikasi AFI"]) &
        (df["Klasifikasi PDRB"] == region["Klasifikasi PDRB"]) &
        (df["Klasifikasi IPM"] == region["Klasifikasi IPM"]) &
        (df["Klasifikasi Kemiskinan"] == region["Klasifikasi Kemiskinan"])
    ]
else:
    peers = df[
        (df["Klasifikasi UFI"] == region["Klasifikasi UFI"]) &
        (df["Klasifikasi PDRB"] == region["Klasifikasi PDRB"]) &
        (df["Klasifikasi IPM"] == region["Klasifikasi IPM"]) &
        (df["Klasifikasi Kemiskinan"] == region["Klasifikasi Kemiskinan"])
    ]

# Display layout with two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"<h4>📍 Statistik: {region['Kabupaten / Kota']}</h4>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:13px'>", unsafe_allow_html=True)

    cols = [
        ("AFI - Inklusi Keuangan", "Klasifikasi AFI"),
        ("D1 - Penetrasi", "Klasifikasi D1"),
        ("D2 - Ketersediaan", "Klasifikasi D2"),
        ("D3 - Penggunaan", "Klasifikasi D3"),
        ("UFI - Utilisasi Keuangan", "Klasifikasi UFI"),
        ("PDRB Per kapita\n(Rp)", "Klasifikasi PDRB"),
        ("IPM", "Klasifikasi IPM"),
        ("Tingkat Kemiskinan", "Klasifikasi Kemiskinan"),
        ("Mayoritas Wilayah", None),
        ("Gini NTL", None),
        ("IDSD - Institusi", None),
        ("IDSD - Infrastruktur", None),
        ("IDSD - Adopsi TIK", None),
        ("IDSD - Kesehatan", None),
        ("IDSD Komposit", "Klasifikasi IDSD")
    ]

    for metric, classification in cols:
        if metric == "Mayoritas Wilayah":
            icon = "🏠" if region[metric] == "Hunian" else "🌳"
            st.markdown(f"**Mayoritas Wilayah:** {icon} {region[metric]}")
        elif metric == "Gini NTL":
            gini_class = classify_gini(region[metric])
            st.markdown(colored_text("Gini NTL", gini_class), unsafe_allow_html=True)
        elif classification:
            st.markdown(colored_text(metric, region[classification]), unsafe_allow_html=True)
        else:
            st.markdown(f"**{metric}:** {region[metric]}")

    st.markdown("</div>", unsafe_allow_html=True)

    st.subheader(f"👥 Daftar Peer ({len(peers)} wilayah)")
    for _, row in peers.iterrows():
        with st.expander(f"{row['Kabupaten / Kota']}"):
            for metric, classification in cols:
                if metric == "Mayoritas Wilayah":
                    icon = "🏠" if row[metric] == "Hunian" else "🌳"
                    st.markdown(f"**Mayoritas Wilayah:** {icon} {row[metric]}")
                elif metric == "Gini NTL":
                    gini_class = classify_gini(row[metric])
                    st.markdown(colored_text("Gini NTL", gini_class), unsafe_allow_html=True)
                elif classification:
                    st.markdown(colored_text(metric, row[classification]), unsafe_allow_html=True)
                else:
                    st.markdown(f"**{metric}:** {row[metric]}")

    st.subheader("📊 Rata-Rata Peer Group")
    avg = peers[[c for c, _ in cols if c in peers.columns]].mean(numeric_only=True)

    for col_name in avg.index:
        st.markdown(f"**{col_name}:** {avg[col_name]:.2f}")

with col2:
    # Search image from DuckDuckGo as first result (basic fallback demo)
    try:
        query = f"{region['Kabupaten / Kota']} kabupaten kota indonesia site:wikipedia.org"
        url = f"https://source.unsplash.com/300x200/?{region['Kabupaten / Kota'].replace(' ', '%20')}"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        st.image(img, caption=f"{region['Kabupaten / Kota']}", use_column_width=True)
    except:
        st.markdown("_Gambar tidak tersedia_ ☁️")
