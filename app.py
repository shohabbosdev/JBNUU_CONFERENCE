import streamlit as st
import pandas as pd
import json
import os
import asyncio
from datetime import datetime, timezone
from utils import validate_input, make_certificates
import pytz

async def main():
    st.set_page_config(
        page_title="Sertifikatlarni olish",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="auto")

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

    with st.form("Birinchi formamiz", clear_on_submit=True):
        fish = st.text_input("F.I.SH", placeholder="Misol: Ulug'murodov Shoh Abbos Baxodir o'g'li", help='Bu maydonda FISH kiritiladi')
        maqola = st.text_input("Maqola mavzuingiz", placeholder="Misol: Ma'lumotlar xavfsizligini oshirishda blockchayn texnologiyalarning o'rni", max_chars=500, help="Bu qismda maqola mavzusi lo'nda kiritilishi kerak")
        shuba = st.selectbox(
            "Sho'bani tanlang",
            options=(
                "1-sho'ba. Ta'lim tizimini takomillashtirish: dolzarb tendensiyalar va strategik yo'nalishlar",
                "2-sho'ba. Biomuhandislik va biotexnologiyalar sohasida innovatsiyalar",
                "3-sho'ba. Raqamli iqtisod va innovatsion axborot-kommunikatsiya texnologiyalarini joriy etishning dolzarb masalalari",
                "4-sho'ba. Psixologiya, tabiiy va aniq fanlar sohasida dolzarb tadqiqotlar",
                "5-sho'ba. Zamonaviy jamiyatda filologiya, tilshunoslik va didaktika",
                "6-sho'ba. Zamonaviy gumanitar ta'limning dolzarb muammolari"
            ),
            placeholder="O'z sho'bangizni tanlang...", help="O'z sho'bangizni tanlashda qiynalsangiz konferensiya ma'muriyatiga telefon qilishingiz mumkin: https://t.me/UzMU_JF_conf_1_2_3_shuba, https://t.me/UzMU_JF_conf_4_5_6_shuba")
        ustun_1, ustun_2 = st.columns(2)
        email = ustun_1.text_input("Email manzilingizni kiriting", placeholder="Misol: ushohabbos@gmail.com", help="Elektron manzil barchangizda bo'ladi degan umiddaman")
        phone = ustun_2.text_input("Telefon raqam", placeholder="+998931189988", help="Telefon raqamni kiriting")
        rozilik = st.checkbox("Yuqoridagi barcha ma'lumotlar to'g'ri va aniq ekanligini tasdiqlaysizmi?")
        taqsdiqlash = st.form_submit_button("Sertifikat olish", type='primary')

        if taqsdiqlash and rozilik:

            is_valid, error_message = validate_input(fish, email, maqola, phone)
            if is_valid:
                try:
                    with open('out/data.json', 'r') as f:
                        existing_data = json.load(f)
                except (FileNotFoundError, json.decoder.JSONDecodeError):
                    existing_data = []

                # Ma'lumotlar mavjudligini tekshirish
                exact_match = next((item for item in existing_data if item["F.I.SH"] == fish or item["Email"] == email or item["Telefon raqam"] == phone or item["Maqola mavzusi"] == maqola or item["Sho'ba"] == shuba), None)
                
                if exact_match:
                    certificate_link = exact_match["Sertifikat manzili"]
                    sertifikat_vaqt_utc = datetime.strptime(exact_match["Sertifikat olingan vaqt"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                    sertifikat_vaqt = sertifikat_vaqt_utc.astimezone(pytz.timezone('Asia/Tashkent'))
                    st.warning(f"Siz ro'yxatdan o'tgansiz! Pastda siz olgan sertifikat nusxasi mavjud. Sertifikat olgan sana: {sertifikat_vaqt.strftime('%Y-%m-%d %H:%M:%S')}", icon='⚠️')
                    st.markdown(f"[{fish}ning sertifikat fayli]({certificate_link})")
                else:
                    sertifikat_vaqt = datetime.now(pytz.timezone('Asia/Tashkent')).strftime("%Y-%m-%d %H:%M:%S")
                    certificate_link = await make_certificates(fish, maqola)
                    st.success("Ma'lumotlar muvaffaqiyatli saqlandi", icon='💾')
                    existing_data.append({
                        "F.I.SH": fish,
                        "Maqola mavzusi": maqola,
                        "Sho'ba": shuba,
                        "Email": email,
                        "Telefon raqam": phone,
                        "Sertifikat manzili": certificate_link,
                        "Sertifikat olingan vaqt": sertifikat_vaqt
                    })
                    with open('out/data.json', 'w') as f:
                        json.dump(existing_data, f, indent=4)
                    st.markdown(f"[{fish}ning sertifikat fayli]({certificate_link})")

                table = {
                    "F.I.SH": fish,
                    "Maqola mavzusi": maqola,
                    "Sho'ba": shuba,
                    "Email": email,
                    "Telefon raqam": phone,
                    "Sertifikat manzili": certificate_link,
                    "Sertifikat olingan vaqt": sertifikat_vaqt
                }
                with st.expander("Siz kiritgan ma'lumotlar bilan tanishing👇👇👇"):
                    st.table(table)

                # Barcha ro'yxatdan o'tganlar ma'lumotlarini ko'rsatish
                df = pd.DataFrame(existing_data)
                with st.expander("Umumiy ro'yxat"):
                    # Telefon raqamlarni qisqartirib olish
                    df['Telefon raqam'] = df['Telefon raqam'].apply(lambda x: f"+998***{x[-4:]}")
                    st.dataframe(df)

            else:
                st.error(f"Xatolik nomi: {error_message}", icon='❌')
        elif taqsdiqlash and not rozilik:
            st.error("Ma'lumotlarni to'g'ri kiritilganligini tasdiqlang", icon='✅')

if __name__ == "__main__":
    asyncio.run(main())

