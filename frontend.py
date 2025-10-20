import streamlit as st
import requests
import io

# ---------- CONFIG ----------
BACKEND_URL = "https://your-backend-service.onrender.com/process_class"  # 🔹 replace with your actual Render URL

st.set_page_config(page_title="Classroom Audio Monitor", page_icon="🎙️", layout="centered")

st.title("🎙️ Classroom Audio Monitoring System")

st.markdown("""
Upload or record classroom audio and automatically generate:
- Full transcript
- Summary report
- Email delivery
""")

# ---------- FORM ----------
with st.form("class_form"):
    teacher_name = st.text_input("Teacher Name")
    subject = st.text_input("Subject")
    grade = st.text_input("Class")
    section = st.text_input("Section")
    period_number = st.text_input("Period Number")
    start_time = st.text_input("Start Time")
    email = st.text_input("Email to receive report")

    st.markdown("#### Audio Input")
    record_option = st.radio("Choose Input Method", ["🎤 Record Audio", "📁 Upload Audio"])

    audio_data = None
    if record_option == "🎤 Record Audio":
        audio_data = st.audio_input("Record your class audio")  # Streamlit's recorder
    else:
        audio_data = st.file_uploader("Upload a .wav or .mp3 file", type=["wav", "mp3"])

    submitted = st.form_submit_button("🚀 Generate Report")

# ---------- SUBMIT ----------
if submitted:
    if not audio_data:
        st.error("Please provide an audio file before submitting.")
    else:
        with st.spinner("Uploading and processing audio... ⏳"):
            files = {"audio_file": audio_data}
            data = {
                "teacher_name": teacher_name,
                "subject": subject,
                "grade": grade,
                "section": section,
                "period_number": period_number,
                "start_time": start_time,
                "email": email
            }

            try:
                response = requests.post(BACKEND_URL, data=data, files=files, timeout=600)
                if response.status_code == 200:
                    result = response.json()
                    if result["status"] == "success":
                        st.success("✅ Report generated and emailed successfully!")
                    else:
                        st.error(f"⚠️ Error: {result.get('message', 'Unknown error')}")
                else:
                    st.error(f"❌ Failed! Status code: {response.status_code}")

            except Exception as e:
                st.error(f"Error connecting to backend: {e}")
