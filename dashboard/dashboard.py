import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("all_data.csv")

df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

with st.sidebar:
    st.title("📊 Dashboard E-Commerce") 
    st.image("mokaa.png")
    
    min_date = df["order_purchase_timestamp"].min().date()
    max_date = df["order_purchase_timestamp"].max().date()

    st.sidebar.subheader("Filter Waktu")
    start_date = st.sidebar.date_input("Tanggal Mulai", min_date)
    end_date = st.sidebar.date_input("Tanggal Akhir", max_date)

    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)

    filtered_df = df[(df["order_purchase_timestamp"] >= start_date) & (df["order_purchase_timestamp"] <= end_date)]
    
    payment_types = df["order_status"].unique()
    selected_payment = st.multiselect("Pilih Status Pesanan", payment_types, default=payment_types)
    
    df_filtered = filtered_df[filtered_df["order_status"].isin(selected_payment)]

st.title("Dashboard E-Commerce")

st.subheader("Total Penjualan")
total_orders = df_filtered["order_id"].nunique()
total_customers = df_filtered["customer_id"].nunique()
total_sales = filtered_df["payment_value"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", total_orders)
col2.metric("Total Customers", total_customers)
col3.metric("Total Sales", f"${total_sales:,.2f}")

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

st.subheader("Distribusi Metode Pembayaran")
payment_counts = filtered_df["payment_type"].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=payment_counts.index, y=payment_counts.values, palette=colors, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

with st.expander("ℹ️ Penjelasan Diagram"):
    st.write("Diagram ini menunjukkan distribusi metode pembayaran yang digunakan pelanggan. Metode pembayaran yang paling umum digunakan dapat mengindikasikan preferensi pelanggan dalam melakukan transaksi.")

st.subheader("Metode Pembayaran yang Paling Digemari")
bypayment_df = filtered_df["payment_type"].value_counts().reset_index()
bypayment_df.columns = ["payment_type", "payment_count"]

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(y="payment_count", x="payment_type", hue="payment_type", data=bypayment_df.sort_values(by="payment_count", ascending=False), palette=colors, legend=False)
plt.title("Metode Pembayaran yang Paling Digemari", loc="center", fontsize=15)
st.pyplot(fig)

with st.expander("ℹ️ Penjelasan Diagram"):
    st.write("Diagram ini menunjukkan metode pembayaran yang paling sering digunakan oleh pelanggan, yang dapat menjadi indikasi penting untuk strategi bisnis.")

st.subheader("Top 10 Kategori Produk Terlaris")
category_counts = filtered_df["product_category_name"].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=category_counts.values, y=category_counts.index, palette=colors, ax=ax)
st.pyplot(fig)

with st.expander("ℹ️ Penjelasan Diagram"):
    st.write("Diagram ini menampilkan 10 kategori produk dengan jumlah transaksi tertinggi, memberikan wawasan tentang produk yang paling laku di platform.")

st.subheader("Preferensi Harga Pelanggan")
if "price" in filtered_df.columns:
    Q1 = filtered_df["price"].quantile(0.25)
    Q3 = filtered_df["price"].quantile(0.75)

    bins = [0, Q1, Q3, filtered_df["price"].max()]
    labels = ["Murah", "Sedang", "Mahal"]

    filtered_df["price_category"] = pd.cut(filtered_df["price"], bins=bins, labels=labels, include_lowest=True)

    price_preference = filtered_df.groupby("price_category")["customer_id"].nunique().reset_index()
    price_preference.columns = ["price_category", "customer_count"]

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="price_category", y="customer_count", data=price_preference, palette=["#D3D3D3", "#72BCD4", "#D3D3D3"], legend=False)
    plt.title("Preferensi Harga Pelanggan", fontsize=14)
    st.pyplot(fig)

    with st.expander("ℹ️ Penjelasan Diagram"):
        st.write("Diagram ini menunjukkan preferensi harga pelanggan berdasarkan jumlah transaksi dalam kategori harga murah, sedang, dan mahal.")
else:
    st.warning("Kolom 'price' tidak ditemukan dalam dataset.")

st.subheader("Top 10 Kota dengan Transaksi Terbanyak")
city_transactions = filtered_df["customer_city"].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=city_transactions.values, y=city_transactions.index, palette=colors, ax=ax)
st.pyplot(fig)

with st.expander("ℹ️ Penjelasan Diagram"):
    st.write("Diagram ini menunjukkan kota-kota dengan jumlah transaksi terbanyak, memberikan wawasan tentang lokasi dengan aktivitas pembelian tertinggi.")

st.subheader("Top 10 Negara dengan Transaksi Terbanyak")
state_transactions = filtered_df["customer_state"].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(x=state_transactions.values, y=state_transactions.index, palette=colors, ax=ax)
st.pyplot(fig)

with st.expander("ℹ️ Penjelasan Diagram"):
    st.write("Diagram ini menampilkan negara bagian dengan jumlah transaksi terbanyak, membantu dalam memahami sebaran pelanggan.")

st.subheader("Peluang Bisnis Berdasarkan Kota")
city_transactions = filtered_df["customer_city"].value_counts().reset_index()
city_transactions.columns = ["city", "transaction_count"]

Q1 = city_transactions["transaction_count"].quantile(0.25)
Q3 = city_transactions["transaction_count"].quantile(0.75)

bins = [0, Q1, Q3, city_transactions["transaction_count"].max()]
labels = ["Peluang Kecil", "Peluang Sedang", "Peluang Besar"]

city_transactions["business_opportunity"] = pd.cut(city_transactions["transaction_count"], bins=bins, labels=labels, include_lowest=True)

category_opportunity_city = city_transactions["business_opportunity"].value_counts().reset_index()
category_opportunity_city.columns = ["business_opportunity", "count"]

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="business_opportunity", y="count", data=category_opportunity_city, order=["Peluang Besar", "Peluang Sedang", "Peluang Kecil"], palette=["#72BCD4", "#72BCD4", "#72BCD4"], ax=ax)
plt.title("Distribusi Peluang Bisnis Berdasarkan Kota", fontsize=15)
st.pyplot(fig)

with st.expander("ℹ️ Penjelasan Diagram"):
    st.write("Diagram ini memberikan wawasan mengenai peluang bisnis berdasarkan jumlah transaksi di tiap kota, membantu dalam menentukan lokasi strategis untuk ekspansi.")

state_transactions = filtered_df["customer_state"].value_counts().reset_index()
state_transactions.columns = ["state", "transaction_count"]

Q1 = state_transactions["transaction_count"].quantile(0.25)
Q3 = state_transactions["transaction_count"].quantile(0.75)

bins = [0, Q1, Q3, state_transactions["transaction_count"].max()]
labels = ["Peluang Kecil", "Peluang Sedang", "Peluang Besar"]

state_transactions["business_opportunity"] = pd.cut(
    state_transactions["transaction_count"], bins=bins, labels=labels, include_lowest=True
)

state_transactions = state_transactions.sort_values(by="transaction_count", ascending=False)

category_opportunity_state = state_transactions["business_opportunity"].value_counts().reset_index()
category_opportunity_state.columns = ["business_opportunity", "count"]

st.subheader("Peluang Bisnis Berdasarkan Negara")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="business_opportunity",
    y="count",
    data=category_opportunity_state,
    order=["Peluang Besar", "Peluang Sedang", "Peluang Kecil"], 
    palette=["#72BCD4", "#72BCD4", "#72BCD4"], ax=ax
)

plt.title("Distribusi Peluang Bisnis Berdasarkan Negara", fontsize=15)
st.pyplot(fig)

with st.expander("ℹ️ Penjelasan Diagram"):
    st.write(
        "Diagram ini menunjukkan peluang bisnis berdasarkan jumlah transaksi di setiap negara bagian. "
        "Negara bagian dengan transaksi tinggi memiliki peluang bisnis lebih besar untuk ekspansi dan investasi."
    )

st.caption("© 2025 E-Commerce Analytics")
