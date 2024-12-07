






















































import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

# Modelni yuklash
with open('food_quality_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# LabelEncoderni qayta yuklash (ma'lumotlarni kodlash uchun)
le_product_name = LabelEncoder()
le_brand = LabelEncoder()
le_packaging = LabelEncoder()
le_storage_condition = LabelEncoder()

# Mahsulot nomlari ro'yxatini yaratish (masalan)
product_names = ["Mahsulot 1", "Mahsulot 2", "Mahsulot 3", "Mahsulot 4", "Mahsulot 5"]  # Bu ro'yxatni kerakli nomlar bilan to'ldiring

# Streamlit interfeysini yaratish
st.title("Oziq-ovqat Mahsulotining Sifatini Bashorat Qilish")

st.header("Mahsulot haqida ma'lumotlarni kiriting:")

# Foydalanuvchidan ma'lumotlarni olish
product_name = st.selectbox("Mahsulot nomini tanlang:", product_names)
manufacturing_date = st.date_input("Ishlab chiqarilgan sana:")
expiration_date = st.date_input("Tugash sanasi:")
brand = st.text_input("Mahsulot brendini kiriting:")
price = st.number_input("Mahsulot narxini kiriting ($):", min_value=0.0, format="%.2f")
packaging_type = st.selectbox("Mahsulot qadoqlanish turi:", ["Plastik", "Shisha", "Qog'oz", "Metall"])
storage_condition = st.selectbox("Mahsulotni saqlash shartlari:", ["Sovuqda saqlash", "Quruqlikda saqlash", "Maxsus sharoitda saqlash"])

# Kirish ma'lumotlarini modelga moslashtirish
if st.button('Sifatni bashorat qilish'):
    try:
        # Mahsulot nomlarini kodlash
        product_name_encoded = le_product_name.fit_transform([product_name])[0]
        brand_encoded = le_brand.fit_transform([brand])[0]
        packaging_encoded = le_packaging.fit_transform([packaging_type])[0]
        storage_condition_encoded = le_storage_condition.fit_transform([storage_condition])[0]

        # Sana va yil ajratish
        manufacturing_year = manufacturing_date.year
        manufacturing_month = manufacturing_date.month
        manufacturing_day = manufacturing_date.day
        expiration_year = expiration_date.year
        expiration_month = expiration_date.month
        expiration_day = expiration_date.day

        # Xususiyatlarni formatlash
        input_features = [
            product_name_encoded,
            manufacturing_year,
            manufacturing_month,
            manufacturing_day,
            expiration_year,
            expiration_month,
            expiration_day,
            brand_encoded,
            price,
            packaging_encoded,
            storage_condition_encoded
        ]

        # Mahsulot sifatini bashorat qilish
        prediction = model.predict([input_features])
        quality = "Yaxshi" if prediction[0] == 0 else ("O'rtacha" if prediction[0] == 1 else "Sifatsiz")
        st.write(f"Bashorat qilingan mahsulot sifati: **{quality}**")
    except Exception as e:
        st.error(f"Xato yuz berdi: {e}")
