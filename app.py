import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from fpdf import FPDF
import re

# ---------------------------
# 1. Load config & define key
# ---------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------------------
# 2. Define helper functions
# ---------------------------
def clean_text(text):
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # Remove **bold**
    text = re.sub(r"\*(.*?)\*", r"\1", text)      # Remove *italic*
    text = re.sub(r"\*", "", text)                # Remove stray asterisks
    text = text.replace("–", "-")                 # Replace en-dash
    text = text.replace("“", '"').replace("”", '"')
    return text.strip()

def generate_ehr_report():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Electronic Health Record (EHR) Report", ln=True, align="C")
    pdf.ln(10)
    # Patient info
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
    # Diagnosis
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Diagnosis & Recommendations", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    for msg in st.session_state.chat_history:
        if msg["role"] == "assistant":
            clean_content = clean_text(msg["content"])
            pdf.multi_cell(0, 10, f"- {clean_content}")
            pdf.ln(3)
    # Save
    ehr_filename = "EHR_Report.pdf"
    pdf.output(ehr_filename, "F")
    return ehr_filename

# ---------------------------
# 3. Initialize Streamlit State
# ---------------------------
st.title("🩺 MedBot - AI Medical Chatbot 🤖")
st.write("Let's analyze your symptoms step by step and provide accurate medical guidance.")

if "step" not in st.session_state:
    st.session_state.step = "ask_name"
    st.session_state.user_data = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------
# 4. Step-by-Step Inputs
# ---------------------------

if st.session_state.step == "ask_name":
    name = st.text_input("Hi! What's your name?")
    if st.button("Enter Name"):
        if name:
            st.session_state.user_data["name"] = name
            st.session_state.step = "ask_age"
            st.rerun()

elif st.session_state.step == "ask_age":
    age = st.number_input(f"Nice to meet you, {st.session_state.user_data['name']}! How old are you?",
                          min_value=1, max_value=120, value=25)
    if st.button("Enter Age"):
        st.session_state.user_data["age"] = age
        st.session_state.step = "ask_gender"
        st.rerun()

elif st.session_state.step == "ask_gender":
    st.write("Please select your gender:")
    gender = st.radio("Gender", ["Select", "Male", "Female", "Other"], index=0)
    if st.button("Enter Gender"):
        if gender != "Select":
            st.session_state.user_data["gender"] = gender
            st.session_state.step = "ask_symptoms"
            st.rerun()

elif st.session_state.step == "ask_symptoms":
    symptoms = st.text_area("What symptoms are you experiencing? (Separate by commas)")
    if st.button("Enter Symptoms"):
        if symptoms:
            st.session_state.user_data["symptoms"] = symptoms
            st.session_state.step = "ask_medical_history"
            st.rerun()

elif st.session_state.step == "ask_medical_history":
    medical_history = st.text_area("Have you had any previous medical issues? (Type 'No' if none)")
    if st.button("Enter Medical History"):
        if medical_history:
            st.session_state.user_data["medical_history"] = medical_history
            st.session_state.step = "diagnose"
            st.rerun()

# ---------------------------
# 5. Diagnosis Step
# ---------------------------
elif st.session_state.step == "diagnose":
    st.subheader("Diagnosing Your Symptoms...")

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

    response = model.generate_content(prompt)
    diagnosis = response.text.strip()

    st.markdown(f"### Diagnosis:\n{diagnosis}")
    st.session_state.chat_history.append({"role": "assistant", "content": diagnosis})

    st.session_state.step = "chat_with_ai"
    st.rerun()

# ---------------------------
# 6. Chat Phase
# ---------------------------
elif st.session_state.step == "chat_with_ai":
    st.subheader("Chat with MedBot!")
    st.markdown("### Patient Details:")
    st.markdown(f"- Name: {st.session_state.user_data['name']}")
    st.markdown(f"- Age: {st.session_state.user_data['age']}")
    st.markdown(f"- Gender: {st.session_state.user_data['gender']}")
    st.markdown(f"- Symptoms: {st.session_state.user_data['symptoms']}")
    st.markdown(f"- Medical History: {st.session_state.user_data['medical_history']}")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(f"{message['role'].capitalize()}: {message['content']}")

    user_input = st.chat_input("Ask me anything about your health...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f"User: {user_input}")

        conversation_history = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history]
        )
        prompt = f"""
        You are MedBot, an AI medical assistant following Mayo Clinic, CDC, and WHO guidelines.
        You remember past conversations and provide accurate medical guidance.

        Conversation History:
        {conversation_history}

        Patient's Question: "{user_input}"
        AI Doctor's Response: Provide a detailed, medical response based on prior context.
        """
        response = model.generate_content(prompt)
        ai_response = response.text.strip()

        with st.chat_message("assistant"):
            st.markdown(f"MedBot: {ai_response}")

        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

    # EHR Report Button only in chat phase
    if st.button("📄 Generate EHR Report"):
        ehr_file = generate_ehr_report()
        st.download_button("📥 Download EHR Report", data=open(ehr_file, "rb"), file_name=ehr_file, mime="application/pdf")
