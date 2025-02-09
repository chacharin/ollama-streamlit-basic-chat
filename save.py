# ฟังก์ชันสำหรับบันทึกประวัติการสนทนาในไฟล์ .txt
def save_conversation_to_file():
    # สร้างเนื้อหาของไฟล์จากประวัติการสนทนา
    conversation_history = ""
    for message in st.session_state["messages"]:
        role = "ผู้ใช้" if message["role"] == "user" else "AI"
        conversation_history += f"{role}: {message['content']}\n\n"

    # บันทึกข้อมูลลงในไฟล์ conversation_history.txt
    with open("conversation_history.txt", "w", encoding="utf-8") as file:
        file.write(conversation_history)

    # แสดงข้อความยืนยันเมื่อบันทึกเสร็จ
    st.success("บันทึกประวัติการสนทนาเรียบร้อยแล้ว!")

# เพิ่มปุ่มบันทึกประวัติการสนทนา
if st.button("Save ประวัติการสนทนา"):
    save_conversation_to_file()
