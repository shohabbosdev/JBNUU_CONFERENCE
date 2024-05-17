import streamlit as st
import pandas as pd
import json
import os
from utils import validate_input, make_certificates

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

st.markdown("""
<div style='text-align: center;'>
    <h1>Konferensiya ishtirokchilari uchun sertifikat tayyorlash sahifasi</h1>
</div>
""", unsafe_allow_html=True)
st.markdown("<h3 align='center'><i>Ro'yxatga olish formasi</i></h3>", unsafe_allow_html=True)

st.markdown("---")

directory = "out"
if not os.path.exists(directory):
    os.makedirs(directory)

with st.form("Birinchi formamiz"):
    fish = st.text_input("F.I.SH", placeholder="Misol: Ulug'murodov Shoh Abbos Baxodir o'g'li", help='Bu maydonda FISH kiritiladi')
    maqola = st.text_input("Maqola mavzuingiz", placeholder="Misol: Ma'lumotlar xavfsizligini oshirishda blockchayn texnologiyalarning o'rni", max_chars=500, help="Bu qismda maqola mavzusi lo'nda kiritilishi kerak")
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
    email = st.text_input("Email manzilingizni kiriting", placeholder="Misol: ushohabbos@gmail.com", help="Elektron manzil barchangizda bo'ladi degan umiddaman")
    phone = st.text_input("Telefon raqam", placeholder="+998931189988", help="Telefon raqamni kiriting")
    rozilik = st.checkbox("Yuqoridagi barcha ma'lumotlar to'g'ri va aniq ekanligini tasdiqlaysizmi?")
    taqsdiqlash = st.form_submit_button("Tasdiqlash", type='primary')

    if taqsdiqlash:
        is_valid, error_message = validate_input(fish, email, maqola, phone)

        if is_valid:
            st.success("Ma'lumotlar muvaffaqiyatli saqlandi", icon='✅')

            table = {
                "F.I.SH": fish,
                "Maqola mavzusi": maqola,
                "Sho'bani nomi": shuba,
                "Email manzil": email,
                "Telefon raqam": phone
            }
            with st.expander("Siz kiritgan ma'lumotlar bilan tanishing👇👇👇"):
                st.table(table)

            try:
                with open('out/data.json', 'r') as f:
                    existing_data = json.load(f)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                existing_data = []

            df = pd.DataFrame(existing_data)

            existing_emails = df['Email manzil'].tolist()
            existing_phones = df['Telefon raqam'].tolist()
            existing_fish = df['F.I.SH'].tolist()
            existing_maqola = df['Maqola mavzusi'].tolist()

            if email in existing_emails or phone in existing_phones or fish in existing_fish or maqola in existing_maqola:
                st.warning(f"Siz ro'yxattan o'tgansiz! Pastda siz olgan sertifikat nusxasi mavjud", icon='⚠️')
                with st.expander("Sertifikatingiz👉👉👉"):
                    st.image(f"out/{fish}.png", caption='Bu sizning sertifikatingiz')
            else:
                existing_data.append(table)
                df = pd.DataFrame(existing_data)
                with open('out/data.json', 'w') as f:
                    json.dump(existing_data, f, indent=4)

                make_certificates(fish, maqola)
                st.image(f"out/{fish}.png", caption='Sertifikatingizni yuklab olishingiz mumkin')

            # Barcha ro'yxatdan o'tganlar ma'lumotlarini ko'rsatish
            with st.expander("Barcha ro'yxatdan o'tganlar ma'lumotlari"):
                # Telefon raqamlarni qisqartirib olish
                df['Telefon raqam'] = df['Telefon raqam'].apply(lambda x: f"+998***{x[-4:]}")
                st.dataframe(df)

        else:
            st.error(f"Xatolik nomi: {error_message}", icon='❌')