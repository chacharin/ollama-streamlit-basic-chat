# นำเข้าไลบรารีที่ใช้ในโปรแกรม
import streamlit as st  # ไลบรารีสำหรับสร้างเว็บแอปพลิเคชันแบบโต้ตอบ
import ollama  # ไลบรารีสำหรับติดต่อกับโมเดล AI ของ Ollama

# ตั้งค่าหน้าเว็บของ Streamlit เช่น ชื่อและการจัดวางองค์ประกอบ
st.set_page_config(page_title="AI Chatbot", layout="centered")
st.title("ระบบสนทนากับ AI")  # แสดงหัวข้อของหน้าเว็บ

# ตรวจสอบว่ามีประวัติข้อความใน session state หรือไม่ ถ้าไม่มีให้สร้างค่าว่าง
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # เก็บข้อความสนทนาไว้ใน session state

# ดึงรายชื่อโมเดล AI ที่มีอยู่จาก Ollama
models = [model["name"] for model in ollama.list()["models"]]  # สร้างรายการชื่อโมเดล
# แสดงเมนูแบบเลือก (dropdown) ให้ผู้ใช้เลือกโมเดลที่ต้องการ
st.session_state["model"] = st.selectbox("เลือกโมเดล AI", models)

# ฟังก์ชันสำหรับรับข้อความตอบกลับจาก AI ทีละส่วน (streaming response)
def model_response_generator():
    # สนทนากับโมเดลโดยส่งข้อความที่มีอยู่ไปให้ AI
    stream = ollama.chat(
        model=st.session_state["model"],  # โมเดลที่ผู้ใช้เลือก
        messages=st.session_state["messages"],  # ประวัติข้อความในการสนทนา
        stream=True,  # เปิดใช้งานการสตรีมข้อมูลทีละส่วน
    )
    # ส่งคืนข้อความทีละส่วนที่ได้จากการสตรีม
    for chunk in stream:
        yield chunk["message"]["content"]

# แสดงประวัติการสนทนาบนหน้าจอ 
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):  # แสดงข้อความตามบทบาท เช่น ผู้ใช้หรือผู้ช่วย AI
        st.markdown(message["content"])  # แสดงข้อความในรูปแบบ Markdown

# รับข้อความใหม่จากผู้ใช้ผ่านช่องป้อนข้อมูล
prompt = st.chat_input("ป้อนข้อความที่คุณต้องการถาม AI:")  # ให้ผู้ใช้ป้อนคำถามหรือข้อความ
if prompt:  # ตรวจสอบว่าผู้ใช้ได้ป้อนข้อความหรือไม่
    # เพิ่มข้อความที่ผู้ใช้ป้อนเข้ามาในประวัติข้อความ
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # แสดงข้อความที่ผู้ใช้ป้อนบนหน้าจอ
    with st.chat_message("user"):
        st.markdown(prompt)

    # เตรียพร้อมการแสดงผลลัพธ์จาก AI
    with st.chat_message("assistant"):
        status_placeholder = st.empty()  # ช่องว่างสำหรับแสดงสถานะการทำงานของ AI
        response_placeholder = st.empty()  # ช่องว่างสำหรับแสดงข้อความตอบกลับ
        status_placeholder.markdown("🤔 **AI กำลังคิด...**")  # แสดงสถานะขณะรอคำตอบจาก AI

        # สตรีมข้อความตอบกลับจาก AI และแสดงข้อความบนหน้าจอ
        streamed_response = ""  # ตัวแปรสำหรับเก็บข้อความที่ได้รับ
        for chunk in model_response_generator():
            status_placeholder.empty()  # ลบข้อความสถานะเมื่อ AI เริ่มตอบกลับ
            streamed_response += chunk  # รวมข้อความที่ได้รับทีละส่วนเข้าด้วยกัน
            response_placeholder.markdown(streamed_response)  # แสดงข้อความที่ได้รับทั้งหมดจนถึงปัจจุบัน

        # บันทึกข้อความตอบกลับจาก AI ลงในประวัติข้อความ
        st.session_state["messages"].append({"role": "assistant", "content": streamed_response})

