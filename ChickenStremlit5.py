# python -m streamlit run ChickenStremlit5.py

import streamlit as st
import pandas as pd
import datetime
import os

# 1. ตั้งค่าพื้นฐาน
st.set_page_config(page_title="Vongsone Small Restaurant", layout="wide")

# ฟังก์ชันบันทึกข้อมูล (ปรับปรุงรูปแบบให้ตรงกับ Excel ตามภาพ)
def save_order_to_csv(customer_name, order_details, total_price, discount_val, final_price, cash_received, change):
    if not os.path.exists('data'):
        os.makedirs('data')
        
    filename = "data/sales_history.csv"
    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    new_records = []
    # วนลูปเพื่อแยกแต่ละเมนูเป็นบรรทัด
    for index, item in enumerate(order_details):
        record = {
            "Date_Time": current_time,
            "Customer_Name": customer_name if customer_name else "ທົ່ວໄປ",
            "Menu": item["menu"],
            "Quantity": item["quantity"],
            "Subtotal_Kip": item["subtotal"],
            # บันทึกยอดรวมเฉพาะบรรทัดแรกของบิล เพื่อให้แสดงผลใน Excel ได้ถูกต้อง
            "Total_Bill": total_price if index == 0 else "",
            "Discount": discount_val if index == 0 else "",
            "Net_Total": final_price if index == 0 else "",
            "Cash_In": cash_received if index == 0 else "",
            "Change": change if index == 0 else ""
        }
        new_records.append(record)
        
    df_new = pd.DataFrame(new_records)
    
    if os.path.exists(filename):
        df_new.to_csv(filename, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        df_new.to_csv(filename, mode='w', header=True, index=False, encoding='utf-8-sig')

# ข้อมูลเมนู
if 'menu_data' not in st.session_state:
    st.session_state.menu_data = [
        {"id": 1, "name": "ເຂົ້າມັນໄກ", "price": 25000, "img": "Chicken1.jpeg", "type": "Food"},
        {"id": 2, "name": "ເຝີງົວຖ້ວຍນ້ອຍ", "price": 30000, "img": "CowBeefNoodles2.jpg", "type": "Food"},
        {"id": 3, "name": "ເຂົ້າປຽກໝູກັອບ", "price": 25000, "img": "PigImage1.jpeg", "type": "Food"},
        {"id": 4, "name": "ເຂົ້າພັດໝູ", "price": 20000, "img": "PigImage2.jpeg", "type": "Food"},
        {"id": 5, "name": "ຕໍາເຂົ້າປຸ້ນ", "price": 20000, "img": "ImagesTum1.jpg", "type": "Food"},
        {"id": 6, "name": "ຕໍາກຸ້ງ", "price": 25000, "img": "ImagesTumShrimp.jpg", "type": "Food"},
        {"id": 7, "name": "ຕໍາປາມຶກ", "price": 20000, "img": "Shell.jpg", "type": "Food"},
        {"id": 8, "name": "ນໍ້າຫວານ", "price": 15000, "img": "SauceImage.jpeg", "type": "Food"},
        {"id": 9, "name": "ນໍ້າດື່ມຫົວເສືອຕຸກກາງ", "price": 10000, "img": "TigerHead waterImage.jpeg", "type": "Drink"},
        {"id": 10, "name": "ເບຍລາວປ໋ອງນ້ອຍ", "price": 20000, "img": "BeerLao.jpg", "type": "Drink"},
        {"id": 11, "name": "ແປັບຊີຕຸກນ້ອຍ", "price": 10000, "img": "Pepsi.jpg", "type": "Drink"},
        {"id": 12, "name": "ຊາຂຽວ", "price": 10000, "img": "OishiGreenTea2.jpg", "type": "Drink"}
    ]

if 'orders' not in st.session_state: st.session_state.orders = {}
if 'discount_val' not in st.session_state: st.session_state.discount_val = 0.0

# --- ส่วนที่ 1: หน้า Admin ---
with st.sidebar:
    st.header("⚙️ ຈັດການເມນູ / ເບິ່ງຍອດຂາຍ")
    edit_mode = st.checkbox("ເປີດໂໝດ Admin")
    
    if edit_mode:
        tab_edit, tab_report = st.tabs(["✏️ ແກ້ໄຂເມນູ", "📊 ຍອດຂາຍ"])
        
        # --- วางโค้ดส่วนแก้ไขรูปภาพไว้ตรงนี้ครับ ---
        with tab_edit:
            selected_item = st.selectbox("ເລືອກເມນູທີ່ຕ້ອງການແກ້ໄຂ", [m["name"] for m in st.session_state.menu_data])
            
            for item in st.session_state.menu_data:
                if item["name"] == selected_item:
                    # 1. แก้ไขราคา
                    item["price"] = st.number_input(f"ແກ້ໄຂລາຄາ {item['name']}", value=item["price"], step=500)
                    
                    # 2. เพิ่มปุ่มอัปโหลดรูปภาพ
                    uploaded_file = st.file_uploader(f"ອັບໂຫຼດຮູບໃໝ່ສຳລັບ {item['name']}", type=['jpg', 'jpeg', 'png'])
                    
                    if uploaded_file is not None:
                        # แสดงรูปตัวอย่างที่กำลังจะอัปโหลด
                        st.image(uploaded_file, caption="ຮູບຕົວຢ່າງທີ່ຈະປ່ຽນ", width=150)
                    
                    if st.button("ບັນທຶກການແກ້ໄຂ"):
                        # ถ้ามีการอัปโหลดไฟล์ใหม่ ให้ทำการบันทึกทับไฟล์เดิม
                        if uploaded_file is not None:
                            # ใช้ชื่อไฟล์เดิมที่ระบุใน menu_data เพื่อบันทึกทับ
                            image_path = item["img"]
                            with open(image_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            st.success(f"ອັບເດດຮູບພາບ {item['name']} สำເລັດ!")
                        
                        st.success("ອັບເດດຂໍ້ມູນຮຽບຮ້ອຍແລ້ວ!")
                        st.rerun()
        # ----------------------------------------
        
        with tab_report:
            if os.path.exists("data/sales_history.csv"):
                df_sales = pd.read_csv("data/sales_history.csv")
                st.dataframe(df_sales)
            else:
                st.info("ຍັງບໍ່ມີຂໍ້ມູນ")

# --- ส่วนที่ 2: หน้าสั่งอาหาร ---
st.title("🍜 Vongsone Small Restaurant")
col1, col2 = st.columns([2, 1])

with col1:
    tab_f, tab_d = st.tabs(["🍲 ອາຫານ", "🥤 ເຄື່ອງດື່ມ"])
    
    def show_items(items):
        g = st.columns(3)
        for i, item in enumerate(items):
            with g[i % 3]:
                st.markdown(f"**{item['name']}**")
                
                # ตรวจสอบว่ามีไฟล์รูปอยู่จริงหรือไม่
                if os.path.exists(item["img"]):
                    st.image(item["img"], use_container_width=True)
                else:
                    # ถ้ารูปไม่มี ให้แสดงกล่องข้อความแทน
                    st.info(f"ບໍ່ມີຮູບ ({item['img']})")
                
                st.write(f"{item['price']:,} ກີບ")
                if st.button(f"ເພີ່ມ", key=f"btn_{item['id']}"):
                    st.session_state.orders[item['name']] = st.session_state.orders.get(item['name'], 0) + 1
                    st.toast(f"ເພີ່ມ {item['name']}")

    with tab_f: show_items([i for i in st.session_state.menu_data if i['type'] == "Food"])
    with tab_d: show_items([i for i in st.session_state.menu_data if i['type'] == "Drink"])

# --- ส่วนที่ 3: ตะกร้าและชำระเงิน ---
with col2:
    st.header("🛒 ກະຕ່າ")
    cust = st.text_input("👤 ຊື່ລູກຄ້າ:")
    total = 0
    details = []

    if not st.session_state.orders:
        st.write("ວ່າງເປົ່າ")
    else:
        for n, q in st.session_state.orders.items():
            p = next(i["price"] for i in st.session_state.menu_data if i["name"] == n)
            sub = p * q
            total += sub
            st.write(f"• {n} x {q} = {sub:,}")
            details.append({"menu": n, "quantity": q, "subtotal": sub})

        st.divider()
        st.subheader(f"ລວມ: {total:,} ກີບ")

        # --- ระบบส่วนลด ---
        st.write("### 🎁 ສ່ວນຫຼຸດ (Discount)")
        d_type = st.selectbox("ປະເພດສ່ວນຫຼຸດ:", ["ບໍ່ມີ", "ຫຼຸດເປັນເງິນ (ກີບ)", "ຫຼຸດເປັນເປີເຊັນ (%)"])
        
        if d_type == "ຫຼຸດເປັນເງິນ (ກີບ)":
            st.session_state.discount_val = st.number_input("ລະບຸຈຳນວນເງິນ:", value=float(st.session_state.discount_val), step=1000.0)
        elif d_type == "ຫຼຸດເປັນເປີເຊັນ (%)":
            pct = st.number_input("ລະບຸ %:", min_value=0, max_value=100, step=1)
            st.session_state.discount_val = (total * pct) / 100
        else:
            st.session_state.discount_val = 0

        if st.button("🔄 ເຄຍສ່ວນຫຼຸດໃຫ້ເປັນ 0"):
            st.session_state.discount_val = 0
            st.rerun()

        final = total - st.session_state.discount_val
        st.markdown(f"## ຍອດສຸດທິ: {final:,} ກີບ")
        
        st.write("---")
        cash = st.number_input("💵 ຮັບເງິນມາ:", min_value=0, step=500)
        
        if cash >= final and final > 0:
            change = cash - final
            st.success(f"💰 ເງິນທອນ: {change:,} ກີບ")
            if st.button("✅ ຢືນຢັນການຂາຍ"):
                save_order_to_csv(cust, details, total, st.session_state.discount_val, final, cash, change)
                st.balloons()
                st.session_state.orders = {}
                st.session_state.discount_val = 0
                st.rerun()
        elif cash > 0:
            st.error("ເງິນບໍ່ພໍ!")
            
        if st.button("🗑️ ລ້າງລາຍການທັງໝົດ"):
            st.session_state.orders = {}
            st.rerun()