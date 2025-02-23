import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from fpdf import FPDF
import re
# Load API Key Securely
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI
st.title("🩺 MedBot - AI Medical Chatbot 🤖")
st.write("Let's analyze your symptoms step by step and provide accurate medical guidance.")

# Initialize Chat State
if "step" not in st.session_state:
    st.session_state.step = "ask_name"
    st.session_state.user_data = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Question Flow (Bot Asks First)
if st.session_state.step == "ask_name":
    name = st.text_input("Hi! What's your name?")
    if name:
        st.session_state.user_data["name"] = name
        st.session_state.step = "ask_age"
        st.rerun()

elif st.session_state.step == "ask_age":
    age = st.number_input(f"Nice to meet you, {st.session_state.user_data['name']}! How old are you?", min_value=1, max_value=120, value=25)
    if st.button("Confirm Age"):
        st.session_state.user_data["age"] = age
        st.session_state.step = "ask_gender"
        st.rerun()

elif st.session_state.step == "ask_gender":
    st.write("Please select your gender:")
    gender = st.radio("Gender", ["Select", "Male", "Female", "Other"], index=0)

    if gender != "Select":  # Ensures user must select before moving on
        st.session_state.user_data["gender"] = gender
        st.session_state.step = "ask_symptoms"
        st.rerun()

elif st.session_state.step == "ask_symptoms":
    symptoms = st.text_area("What symptoms are you experiencing? (Separate by commas)")
    if symptoms:
        st.session_state.user_data["symptoms"] = symptoms
        st.session_state.step = "ask_medical_history"
        st.rerun()

elif st.session_state.step == "ask_medical_history":
    medical_history = st.text_area("Have you had any previous medical issues? (Type 'No' if none)")
    if medical_history:
        st.session_state.user_data["medical_history"] = medical_history
        st.session_state.step = "diagnose"
        st.rerun()

# Diagnosis Phase (After Collecting Info)
elif st.session_state.step == "diagnose":
    st.subheader("Diagnosing Your Symptoms...")

    # Construct AI Prompt
    prompt = f"""
    You are a medical AI assistant following guidelines from Mayo Clinic, CDC, and WHO.
    Based on the patient's symptoms, age, gender, and medical history, suggest possible medical conditions.

    Patient Info:
    Name: {st.session_state.user_data['name']}
    Age: {st.session_state.user_data['age']}
    Gender: {st.session_state.user_data['gender']}
    Symptoms: {st.session_state.user_data['symptoms']}
    Medical History: {st.session_state.user_data['medical_history']}

    Diagnosis: Provide a list of possible conditions along with recommendations.
    """

    # Generate AI Diagnosis
    response = model.generate_content(prompt)
    diagnosis = response.text.strip()

    st.markdown(f"### Diagnosis:\n{diagnosis}")

    # Store in Chat History
    st.session_state.chat_history.append({"role": "assistant", "content": diagnosis})

    # Move to Chat Phase
    st.session_state.step = "chat_with_ai"

# Chat Phase (After Diagnosis)
elif st.session_state.step == "chat_with_ai":
    st.subheader("Chat with MedBot!")

    # Display User Info
    st.markdown("### Patient Details:")
    st.markdown(f"- Name: {st.session_state.user_data['name']}")
    st.markdown(f"- Age: {st.session_state.user_data['age']}")
    st.markdown(f"- Gender: {st.session_state.user_data['gender']}")
    st.markdown(f"- Symptoms: {st.session_state.user_data['symptoms']}")
    st.markdown(f"- Medical History: {st.session_state.user_data['medical_history']}")

    # Show Chat History
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(f"{message['role'].capitalize()}: {message['content']}")

    # Chat Input
    user_input = st.chat_input("Ask me anything about your health...")
    if user_input:
        # Store User Message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f"User: {user_input}")

        # Construct AI Prompt With Chat History
        conversation_history = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history])
        prompt = f"""
        You are MedBot, an AI medical assistant following Mayo Clinic, CDC, and WHO guidelines.
        You remember past conversations and provide accurate medical guidance.

        Conversation History:
        {conversation_history}

        Patient's Question: "{user_input}"
        AI Doctor's Response: Provide a detailed, medical response based on prior context.
        """

        # Generate AI Response
        response = model.generate_content(prompt)
        ai_response = response.text.strip()

        with st.chat_message("assistant"):
            st.markdown(f"MedBot: {ai_response}")

        # Store AI Response
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

# ✅ Function to clean AI-generated content (Removes Unicode issues)
def clean_text(text):
    
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # Removes **bold**
    text = re.sub(r"\*(.*?)\*", r"\1", text)  # Removes *italic*
    text = re.sub(r"\*", "", text)  # ✅ Remove any stray asterisks
    text = text.replace("–", "-")  # ✅ Replace en-dash with a regular hyphen
    text = text.replace("“", '"').replace("”", '"')  # ✅ Convert smart quotes to normal quotes
    return text.strip()  # ✅ Ensures clean, trimmed text

# ✅ EHR Report Function (Now Completely Clean & Properly Formatted)
def generate_ehr_report():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ✅ Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Electronic Health Record (EHR) Report", ln=True, align="C")
    pdf.ln(10)

    # ✅ Patient Information Section
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Patient Information", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"- Name: {st.session_state.user_data['name']}", ln=True)
    pdf.cell(200, 10, f"- Age: {st.session_state.user_data['age']}", ln=True)
    pdf.cell(200, 10, f"- Gender: {st.session_state.user_data['gender']}", ln=True)
    pdf.cell(200, 10, f"- Symptoms: {st.session_state.user_data['symptoms']}", ln=True)
    pdf.cell(200, 10, f"- Medical History: {st.session_state.user_data['medical_history']}", ln=True)
    pdf.ln(5)

    # ✅ Diagnosis & Recommendations Section
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Diagnosis & Recommendations", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    for msg in st.session_state.chat_history:
        if msg["role"] == "assistant":
            clean_content = clean_text(msg["content"])  # ✅ Ensure all asterisks are removed
            pdf.multi_cell(0, 10, f"- {clean_content}")
            pdf.ln(3)

    ehr_filename = "EHR_Report.pdf"
    pdf.output(ehr_filename, "F")  # ✅ Save the file correctly
    return ehr_filename

# ✅ EHR Report Button
if st.button("📄 Generate EHR Report"):
    ehr_file = generate_ehr_report()
    st.download_button("📥 Download EHR Report", data=open(ehr_file, "rb"), file_name=ehr_file, mime="application/pdf")
