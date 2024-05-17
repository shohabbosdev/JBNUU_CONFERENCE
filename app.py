import streamlit as st
import re
import json
import os
import pandas as pd
from make_certificate import make_certificates

st.set_page_config(
    page_title="Sertifikatlarni olish",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
    })

st.title('Konferensiya ishtirokchilari uchun sertifikat olish')
st.markdown("<h3 align='center'><i>Ro'yxatga olish formasi</i></h3>", unsafe_allow_html=True)

st.markdown("---")

# Telefon raqam uchun regex
phone_regex = r'^\+998\d{9}$'

# Email uchun regex
email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

directory = "out"
if not os.path.exists(directory):
    os.makedirs(directory)

with st.form("Birinchi formamiz"):
   # FISH maydoni
   fish = st.text_input("F.I.SH", placeholder="Misol: Ulug'murodov Shoh Abbos Baxodir o'g'li", help='Bu maydonda FISH kiritiladi')

   # Maqola matnini kiritish
   maqola = st.text_input("Maqola mavzuingiz", placeholder="Misol: Ma'lumotlar xavfsizligini oshirishda blockchayn texnologiyalarning o'rni", max_chars=20, help="Bu qismda maqola mavzusi lo'nda kiritilishi kerak")

   # Sho'bani tanlash
   shuba = st.selectbox(
       "Sho'bani tanlang",
       options=(
           "1-sho'ba. Ta'lim tizimini takomillashtirish: dolzarb tendensiyalar va strategik yo'nalishlar",
           "2-sho'ba. Biomuhandislik va biotexnologiyalar sohasida innovatsiyalar",
           "3-sho'ba. Raqamli iqtisod va innovatsion axborot-kommunikatsiya texnologiyalarini joriy etishning dolzarb masalalari",
           "4-sho'ba. Psixologiya, tabiiy va aniq fanlar sohasida dolzarb tadqiqotla",
           "5-sho'ba. Zamonaviy jamiyatda filologiya, tilshunoslik va didaktika",
           "6-sho'ba. Zamonaviy gumanitar ta'limning dolzarb muammolari"
       ),
       placeholder="O'z sho'bangizni tanlang...", help="O'z sho'bangizni tanlashda qiynalsangiz konferensiya ma'muriyatiga telefon qilishingizi mumkin: https://t.me/UzMU_JF_conf_1_2_3_shuba, https://t.me/UzMU_JF_conf_4_5_6_shuba")

   # 2 ta columnga bo'lamiz
   col1, col2 = st.columns(2)

   # Email manzilingizni kiritish
   email = col1.text_input("Email manzilingizni kiriting", placeholder="Misol: ushohabbos@gmail.com", help="Elektron manzil barchangizda bo'ladi degan umiddaman")

   # Telefon raqamni kiritish
   phone = col2.text_input("Telefon raqam", placeholder="+998931189988", help="Telefon raqamni kiriting")

   # Kiritilgan ma'lumotlar to'g'ri ekanligiga ishonish
   rozilik = st.checkbox("Yuqoridagi barcha ma'lumotlar to'g'ri va aniq ekanligini tasdiqlaysizmi?")

   # Ma'lumotlarni saqlash
   taqsdiqlash = st.form_submit_button("Tasdiqlash", type='primary')

   # Shartlar
   if rozilik and taqsdiqlash:
       if fish == "" or email == "" or maqola == "":
           st.warning("Iltimos barcha maydonlar bo'sh bo'lmasligini ta'minlang!!", icon='⚠️')
       elif not re.match(phone_regex, phone):
           st.warning("Telefon raqam noto'g'ri formatda kiritildi. Iltimos, +998xxxxxxxx formatida kiriting.", icon='⚠️')
       elif not re.match(email_regex, email):
           st.warning("Email manzil noto'g'ri formatda kiritildi. Iltimos, to'g'ri formatda kiriting.", icon='⚠️')
       else:
           st.success("Ma'lumotlar muvaffaqiyatli saqlandi", icon='✅')

           # Ma'lumotlarni ekranga chiqarish
           table = {
               "F.I.SH": fish,
               "Maqola mavzusi": maqola,
               "Sho'bani nomi": shuba,
               "Email manzil": email,
               "Telefon raqam": phone
           }
           st.table(table)
           
           # Ma'lumotlarni data.json fayliga saqlash
           try:
               with open('out/data.json', 'r') as f:
                   existing_data = json.load(f)
           except (FileNotFoundError, json.decoder.JSONDecodeError):
               existing_data = []

           existing_emails = [entry['Email manzil'] for entry in existing_data]
           existing_phones = [entry['Telefon raqam'] for entry in existing_data]
           existing_fish   = [entry['F.I.SH'] for entry in existing_data]
           existing_maqola = [entry['Maqola mavzusi'] for entry in existing_data]

           if email in existing_emails or phone in existing_phones or fish in existing_fish or maqola in existing_maqola:
               st.warning(f"Siz ro'yxattan o'tgansiz! Sizga sertifikat bera olmaymiz", icon='⚠️')
               st.image(f"out/{fish}.png",caption='Bu sizning sertifikatingiz')
           else:
               existing_data.append(table)
               with open('out/data.json', 'w') as f:
                   json.dump(existing_data, f, indent=4)

               # Make certificate
               make_certificates(fish, maqola)
               st.image(f"out/{fish}.png",caption='Sertifikatingizni yuklab olishingiz mumkin')

   elif taqsdiqlash and not rozilik:
       st.error("Siz ma'lumotlaringiz to'g'ri ekanlgini tasdiqlashingiz kerak!!", icon='❌')