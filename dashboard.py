import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
st.title("Dashboard Streamlit Landing Page")
sns.set_theme()


# Menu Navigasi
menu = ["Home", "Month"]
choice = st.sidebar.selectbox("Pilih Halaman", menu)
all_df = pd.read_csv("all_dataset.csv")

# Konten Bagian 1
if choice == "Home":
    st.header("Shoping Chart Data Analysis")
    st.write("")
    # Group by gender and calculate the number of unique customer_id
    gender_data = all_df.groupby(by="gender").agg({"customer_id": "nunique"}).reset_index()

    # Find the index of the maximum value in the 'customer_id' column
    max_prop_index = gender_data["customer_id"].idxmax()

    # Create explode list for pie chart
    explode = [0.1 if i == max_prop_index else 0 for i in range(len(gender_data))]

    # Streamlit Dashboard
    st.title("Customer Gender Distribution Dashboard")

    # Display DataFrame
    st.subheader("Data Summary:")
    st.write(gender_data)

    # Pie chart visualization
    st.subheader("Customer Gender Distribution:")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(gender_data["customer_id"], labels=gender_data["gender"], autopct="%1.1f%%", startangle=90, explode=explode)
    ax.set_title("Proporsi Jumlah Customer berdasarkan Gender")
    st.pyplot(fig)

    # Create age_group column
    all_df["age_group"] = all_df.age.apply(lambda x: "Youth" if x <= 25 else ("Seniors" if x > 60 else "Adults"))

    # Group by age_group and calculate the number of unique order_id
    age_group_counts = all_df.groupby(by="age_group").order_id.nunique().sort_values(ascending=False)

    # Streamlit Dashboard
    st.title("Sales Distribution by Age Group Dashboard")

    # Display DataFrame
    st.subheader("Data Summary:")
    st.write(age_group_counts)

    # Pie chart visualization
    st.subheader("Sales Distribution by Age Group:")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(age_group_counts, labels=age_group_counts.index, autopct="%1.1f%%", startangle=90, colors=['lightblue', 'lightcoral', 'lightgreen'])
    ax.set_title("Proporsi Jumlah Penjualan berdasarkan Grup Usia")
    st.pyplot(fig)

    # Aggregating data
    aggregated_data = all_df.groupby(by="state").agg({
        "order_id": "nunique",
        "total_price": "sum"
    }).sort_values(by='total_price', ascending=False).reset_index()

    # Streamlit Dashboard
    st.title("Sales by State Dashboard")

    # Display DataFrame
    st.subheader("Data Summary:")
    st.write(aggregated_data)

    # Bar plot visualization
    st.subheader("Sales by State:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='state', y='order_id', data=aggregated_data, palette='deep')
    plt.title('Jumlah Penjualan berdasarkan State')
    plt.xlabel('State')
    plt.ylabel('Jumlah Penjualan')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # Bar plot visualization
    st.subheader("Total Sales by State:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='state', y='total_price', data=aggregated_data, palette='viridis')
    plt.title('Total Penjualan berdasarkan State')
    plt.xlabel('State')
    plt.ylabel('Penjualan')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    all_df['order_date'] = pd.to_datetime(all_df['order_date'])
    # Extract month from 'order_date'
    all_df['month'] = all_df['order_date'].dt.to_period('M')

    # Aggregating data
    aggregated_data = all_df.groupby(by='month').agg({
        'sales_id': 'nunique',
        'quantity_x': 'sum',
        'total_price': 'sum'
    }).reset_index()

    # Konversi 'month' ke string sebelum plotting
    aggregated_data['month'] = aggregated_data['month'].astype(str)

    # Streamlit Dashboard
    st.title("Sales Dashboard by Month")

    # Display DataFrame
    st.subheader("Data Summary:")
    st.write(aggregated_data)

    # Line plot visualizations
    st.subheader("Sales by Month:")
    fig_sales, ax_sales = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='month', y='sales_id', data=aggregated_data, marker='o', color='b', ax=ax_sales)
    plt.title('Jumlah Penjualan Berdasarkan Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Penjualan')
    plt.xticks(rotation=45, ha='right')  # Rotate month labels for readability
    st.pyplot(fig_sales)

    st.subheader("Quantity by Month:")
    fig_quantity, ax_quantity = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='month', y='quantity_x', data=aggregated_data, marker='o', color='r', ax=ax_quantity)
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Barang Terjual')
    plt.xticks(rotation=45, ha='right')  # Rotate month labels for readability
    st.pyplot(fig_quantity)

    st.subheader("Total Price by Month:")
    plt.title('Total Omset Berdasarkan Bulan')
    fig_price, ax_price = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='month', y='total_price', data=aggregated_data, marker='o', color='g', ax=ax_price)
    plt.title('Jumlah Barang Terjual Berdasarkan Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Total Omset')
    plt.xticks(rotation=45, ha='right')  # Rotate month labels for readability
    st.pyplot(fig_price)

        # Aggregating data
    aggregated_data = all_df.groupby(by=['state', 'product_type']).agg({
        'sales_id': 'nunique',
        'quantity_x': 'sum',
        'total_price': 'sum'
    }).sort_values(by=['state', 'total_price'], ascending=False).reset_index()
    
    # Streamlit Dashboard
    st.title("Sales Dashboard by State and Product Type")
    
    # Display DataFrame
    st.subheader("Data Summary:")
    st.write(aggregated_data)
    
    # Bar plot visualizations
    st.subheader("Sales by State and Product Type:")
    fig_sales = plt.figure(figsize=(12, 6))
    sns.barplot(x='state', y='sales_id', hue='product_type', data=aggregated_data, palette='deep')
    plt.title('Jumlah Penjualan Berdasarkan State dan Product Type')
    plt.xlabel('State')
    plt.ylabel('Jumlah Penjualan')
    plt.legend(title='Product Type', bbox_to_anchor=(1.05, 1), loc='upper left')  # Menampilkan legenda di luar plot
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig_sales)
    
    st.subheader("Quantity by State and Product Type:")
    fig_quantity = plt.figure(figsize=(12, 6))
    sns.barplot(x='state', y='quantity_x', hue='product_type', data=aggregated_data, palette='muted')
    plt.title('Jumlah Barang Terjual Berdasarkan State dan Product Type')
    plt.xlabel('State')
    plt.ylabel('Jumlah Barang Terjual')
    plt.legend(title='Product Type', bbox_to_anchor=(1.05, 1), loc='upper left')  # Menampilkan legenda di luar plot
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig_quantity)
    
    st.subheader("Total Price by State and Product Type:")
    fig_price = plt.figure(figsize=(12, 6))
    sns.barplot(x='state', y='total_price', hue='product_type', data=aggregated_data, palette='bright')
    plt.title('Total Omset Berdasarkan State dan Product Type')
    plt.xlabel('State')
    plt.ylabel('Total Omset')
    plt.legend(title='Product Type', bbox_to_anchor=(1.05, 1), loc='upper left')  # Menampilkan legenda di luar plot
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig_price)

# Konten Bagian 2
elif choice == "Month":
    st.header("Visualisasi Data")
    all_df['order_date'] = pd.to_datetime(all_df['order_date'])
    # Extract month from 'order_date'
    bulan = all_df['order_date'].dt.to_period('M').sort_values(ascending=False).unique()
    select_bulan = st.selectbox("Pilih Halaman", bulan)
    all_df['day'] = all_df['order_date'].dt.to_period('D')
    aggregated_data = all_df[all_df['order_date'].dt.to_period('M')==select_bulan].groupby(by='day').agg({
    'sales_id': 'nunique',
    'quantity_x': 'sum',
    'total_price': 'sum'
    }).reset_index()
    aggregated_data['day'] = aggregated_data['day'].astype(str)
    st.write(aggregated_data)
    st.subheader("Sales by Day:")
    st.write(select_bulan)
    fig_sales, ax_sales = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='day', y='sales_id', data=aggregated_data, marker='o', color='b', ax=ax_sales)
    plt.title('Jumlah Penjualan Harian')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Penjualan')
    plt.xticks(rotation=45, ha='right')  # Rotate month labels for readability
    st.pyplot(fig_sales)

    st.subheader("Quantity by Day:")
    fig_quantity, ax_quantity = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='day', y='quantity_x', data=aggregated_data, marker='o', color='r', ax=ax_quantity)
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Barang Terjual')
    plt.xticks(rotation=45, ha='right')  # Rotate day labels for readability
    st.pyplot(fig_quantity)

    st.subheader("Total Price by Day:")
    plt.title('Total Omset Berdasarkan Tanggal')
    fig_price, ax_price = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='day', y='total_price', data=aggregated_data, marker='o', color='g' , ax=ax_price)
    plt.title('Jumlah Barang Terjual Berdasarkan Tanggal')
    plt.xlabel('Tanggal')
    plt.ylabel('Total Omset')
    plt.xticks(rotation=45, ha='right')  # Rotate day labels for readability
    st.pyplot(fig_price)

    gender_data = all_df[all_df['order_date'].dt.to_period('M')==select_bulan].groupby(by="gender").agg({"customer_id": "nunique"}).reset_index()

    # Find the index of the maximum value in the 'customer_id' column
    max_prop_index = gender_data["customer_id"].idxmax()

    # Create explode list for pie chart
    explode = [0.1 if i == max_prop_index else 0 for i in range(len(gender_data))]

    # Streamlit Dashboard
    st.title("Customer Gender Distribution Dashboard")

    # Display DataFrame
    st.subheader("Data Summary:")
    st.write(gender_data)

    # Pie chart visualization
    st.subheader("Customer Gender Distribution:")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(gender_data["customer_id"], labels=gender_data["gender"], autopct="%1.1f%%", startangle=90, explode=explode)
    ax.set_title("Proporsi Jumlah Customer berdasarkan Gender")
    st.pyplot(fig)

    all_df["age_group"] = all_df[all_df['order_date'].dt.to_period('M')==select_bulan].age.apply(lambda x: "Youth" if x <= 25 else ("Seniors" if x > 60 else "Adults"))

    # Group by age_group and calculate the number of unique order_id
    age_group_counts = all_df.groupby(by="age_group").order_id.nunique().sort_values(ascending=False)

    # Streamlit Dashboard
    st.title("Sales Distribution by Age Group Dashboard")

    # Display DataFrame
    st.subheader("Data Summary:")
    st.write(age_group_counts)

    # Pie chart visualization
    st.subheader("Sales Distribution by Age Group:")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(age_group_counts, labels=age_group_counts.index, autopct="%1.1f%%", startangle=90, colors=['lightblue', 'lightcoral', 'lightgreen'])
    ax.set_title("Proporsi Jumlah Penjualan berdasarkan Grup Usia")
    st.pyplot(fig)

    # Aggregating data
    aggregated_data = all_df[all_df['order_date'].dt.to_period('M')==select_bulan].groupby(by="state").agg({
        "order_id": "nunique",
        "total_price": "sum"
    }).sort_values(by='total_price', ascending=False).reset_index()

    # Streamlit Dashboard
    st.title("Sales by State Dashboard")

    # Display DataFrame
    st.subheader("Data Summary:")
    st.write(aggregated_data)

    # Bar plot visualization
    st.subheader("Sales by State:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='state', y='order_id', data=aggregated_data, palette='deep')
    plt.title('Jumlah Penjualan berdasarkan State')
    plt.xlabel('State')
    plt.ylabel('Jumlah Penjualan')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # Bar plot visualization
    st.subheader("Total Sales by State:")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='state', y='total_price', data=aggregated_data, palette='viridis')
    plt.title('Total Penjualan berdasarkan State')
    plt.xlabel('State')
    plt.ylabel('Penjualan')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    aggregated_data = all_df[all_df['order_date'].dt.to_period('M')==select_bulan].groupby(by=['state', 'product_type']).agg({
        'sales_id': 'nunique',
        'quantity_x': 'sum',
        'total_price': 'sum'
    }).sort_values(by=['state', 'total_price'], ascending=False).reset_index()
    
    # Streamlit Dashboard
    st.title("Sales Dashboard by State and Product Type")
    
    # Display DataFrame
    st.subheader("Data Summary:")
    st.write(aggregated_data)
    
    # Bar plot visualizations
    st.subheader("Sales by State and Product Type:")
    fig_sales = plt.figure(figsize=(12, 6))
    sns.barplot(x='state', y='sales_id', hue='product_type', data=aggregated_data, palette='deep')
    plt.title('Jumlah Penjualan Berdasarkan State dan Product Type')
    plt.xlabel('State')
    plt.ylabel('Jumlah Penjualan')
    plt.legend(title='Product Type', bbox_to_anchor=(1.05, 1), loc='upper left')  # Menampilkan legenda di luar plot
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig_sales)
    
    st.subheader("Quantity by State and Product Type:")
    fig_quantity = plt.figure(figsize=(12, 6))
    sns.barplot(x='state', y='quantity_x', hue='product_type', data=aggregated_data, palette='muted')
    plt.title('Jumlah Barang Terjual Berdasarkan State dan Product Type')
    plt.xlabel('State')
    plt.ylabel('Jumlah Barang Terjual')
    plt.legend(title='Product Type', bbox_to_anchor=(1.05, 1), loc='upper left')  # Menampilkan legenda di luar plot
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig_quantity)
    
    st.subheader("Total Price by State and Product Type:")
    fig_price = plt.figure(figsize=(12, 6))
    sns.barplot(x='state', y='total_price', hue='product_type', data=aggregated_data, palette='bright')
    plt.title('Total Omset Berdasarkan State dan Product Type')
    plt.xlabel('State')
    plt.ylabel('Total Omset')
    plt.legend(title='Product Type', bbox_to_anchor=(1.05, 1), loc='upper left')  # Menampilkan legenda di luar plot
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig_price)

    data = all_df[all_df['order_date'].dt.to_period('M')==select_bulan].groupby(by=['day', 'product_type']).agg({
    'sales_id': 'nunique',
    'quantity_x': 'sum',
    'total_price': 'sum'
    }).reset_index()

    data['day'] = data['day'].astype(str)
    # Membuat lineplot menggunakan seaborn
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='day', y='sales_id', hue='product_type', data=data, marker='o')

    # Menambahkan judul dan label sumbu
    plt.title('Line Plot of Sales_id by Day ')
    plt.xlabel('Day')
    plt.ylabel('Number of Sales_id')
    plt.xticks(rotation=45, ha='right')
    # Menampilkan legenda
    plt.legend(title='Product Type')
    st.pyplot(plt)
    

    plt.figure(figsize=(12, 6))
    sns.lineplot(x='day', y='quantity_x', hue='product_type', data=data, marker='o')

    # Menambahkan judul dan label sumbu
    plt.title('Line Plot of Quantity by Day ')
    plt.xlabel('Day')
    plt.ylabel('Number of Quantity')
    plt.xticks(rotation=45, ha='right')
    # Menampilkan legenda
    plt.legend(title='Product Type')

    # Menampilkan plot di Streamlit
    st.pyplot(plt)
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='day', y='total_price', hue='product_type', data=data, marker='o')

    # Menambahkan judul dan label sumbu
    plt.title('Line Plot of Total Price by Day ')
    plt.xlabel('Day')
    plt.ylabel('Number of Total Price')
    plt.xticks(rotation=45, ha='right')
    # Menampilkan legenda
    plt.legend(title='Product Type')

    # Menampilkan plot di Streamlit
    st.pyplot(plt)
    
    # Tambahkan analisis data atau konten lainnya di bagian ini

# Catatan: Anda dapat menambahkan lebih banyak bagian sesuai kebutuhan

# Tambahkan elemen-elemen umum seperti footer, tautan, dll.

# Contoh Tautan
st.markdown("[Tautan ke Dokumentasi Streamlit](https://docs.streamlit.io)")

# Contoh Footer
st.markdown("---")
st.write("© 2023 Zuliansyah . Hak Cipta Dilindungi.")
