import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Web (Judul Tab Browser)
st.set_page_config(page_title="Sales Interactive Dashboard", layout="wide")

# 2. Judul Utama Dashboard
st.title("📊 Interactive Sales Dashboard")
st.markdown("---")

# 3. Load Data dari Excel
@st.cache_data
def load_data():
    df = pd.read_excel('SIRCLO_Sales_Database_2026.xlsx', sheet_name='Sales_Data')
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    return df

df = load_data()

# 4. Sidebar (Filter Interaktif)
st.sidebar.header("Filter Data")
selected_channel = st.sidebar.multiselect(
    "Pilih Kanal Penjualan:",
    options=df['Nama_Kanal'].unique(),
    default=df['Nama_Kanal'].unique()
)

selected_status = st.sidebar.multiselect(
    "Pilih Status Pengiriman:",
    options=df['Status_Pengiriman'].unique(),
    default=df['Status_Pengiriman'].unique()
)

# Apply Filter ke Dataframe
df_filtered = df[
    (df['Nama_Kanal'].isin(selected_channel)) & 
    (df['Status_Pengiriman'].isin(selected_status))
]

# 5. KPI Ringkasan Metrik
total_revenue = df_filtered['Total_Penjualan'].sum()
total_trx = df_filtered['ID_Transaksi'].nunique()
total_qty = df_filtered['Jumlah_Terjual'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Omzet", f"Rp {total_revenue:,.0f}".replace(",", "."))
col2.metric("Total Transaksi", f"{total_trx:,} Transaksi")
col3.metric("Total Unit Terjual", f"{total_qty:,} pcs")

st.markdown("---")

# 6. Visualisasi Grafik Interaktif (Plotly)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Total Penjualan per Produk")
    fig_product = px.bar(
        df_filtered.groupby('Nama_Produk')['Total_Penjualan'].sum().reset_index(),
        x='Total_Penjualan',
        y='Nama_Produk',
        orientation='h',
        color='Nama_Produk',
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig_product.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_product, use_container_width=True)

with col_right:
    st.subheader("Proporsi Status Pengiriman")
    fig_status = px.pie(
        df_filtered,
        names='Status_Pengiriman',
        values='Total_Penjualan',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_status, use_container_width=True)

# 7. Tampilkan Tabel Data Detail
with st.expander("Lihat Data Detail (Tabel Filtered)"):
    st.dataframe(df_filtered)
