# 🩺 MedBot - AI Medical Chatbot 🤖
An AI-powered medical chatbot that diagnoses symptoms, provides recommendations, and generates an Electronic Health Record (EHR) report. Built with Gemini AI and Streamlit.

## 🚀 Features
- ✅ Step-by-step patient intake process (Name → Age → Gender → Symptoms → Medical History)
- ✅ AI-generated diagnosis based on Mayo Clinic, CDC, and WHO guidelines
- ✅ Conversational AI doctor for medical queries
- ✅ EHR Report Generation (Downloadable PDF with structured medical details)
- ✅ Bulletproof Formatting – No asterisks, proper bolding, and spacing in both UI & PDF

## 🛠️ Tech Stack
- **Streamlit** (UI Framework)
- **Google Gemini 1.5 API** (Medical AI)
- **FPDF** (Generates EHR reports)
- **Python 3.10+**

## 📂 Project Structure
\`\`\`
📦 MedBot-AI
 ┣ 📜 app.py                # Main AI Chatbot Code
 ┣ 📜 .env                   # API Key (DO NOT SHARE)
 ┣ 📜 requirements.txt       # Required Libraries
 ┣ 📜 README.md              # This Document
\`\`\`

## 📌 Installation
### 1️⃣ Clone the Repo

\`\`\`bash
git clone https://github.com/YOUR_GITHUB_USERNAME/MedBot-AI.git
cd MedBot-AI
\`\`\`

### 2️⃣ Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3️⃣ Set Up Environment Variables
1. **Create a \`.env\` file** in the project folder.
2. **Add your API key**:
   \`\`\`
   GEMINI_API_KEY=your_api_key_here
   \`\`\`

### 4️⃣ Run the Chatbot
\`\`\`bash
streamlit run app.py
\`\`\`

## 📄 Example EHR Report Output
**Patient Information:**  
- **Name:** Leonardo  
- **Age:** 25  
- **Gender:** Male  
- **Symptoms:** Cold, Headache, Cough  
- **Medical History:** No  

**Diagnosis & Recommendations:**  
- **Common Cold (Viral Upper Respiratory Infection)**
  - Rest, fluids, over-the-counter pain relievers
- **Flu (Influenza)**
  - If symptoms worsen, consult a doctor
- **COVID-19**
  - Testing should be considered if exposure is suspected

⚠️ **Disclaimer:**  
This information is **for educational purposes only** and does not constitute medical advice. Consult a healthcare professional for accurate diagnosis and treatment.

## 📤 Deploying on Streamlit Cloud
### 1️⃣ Push to GitHub
\`\`\`bash
git add .
git commit -m \"Added MedBot AI Chatbot\"
git push origin main
\`\`\`

### 2️⃣ Deploy on Streamlit
1. **Go to** [Streamlit Cloud](https://share.streamlit.io/)
2. **Click \"New App\"** and select your GitHub repo
3. **Set Secrets**:
   - Go to **Settings > Secrets**
   - Add:
     \`\`\`
     GEMINI_API_KEY = your_api_key_here
     \`\`\`
4. **Click Deploy 🚀**

## 🙌 Contributing
If you’d like to contribute:
1. **Fork the repo**
2. **Create a new branch:** \`git checkout -b feature-name\`
3. **Commit your changes:** \`git commit -m \"Added a new feature\"\`
4. **Push to GitHub:** \`git push origin feature-name\`
5. **Open a Pull Request**

## 📜 License
This project is licensed under the **MIT License**. Feel free to use and modify!

## 📞 Contact
If you have any issues or suggestions, feel free to **open an issue** or contact me:
📧 **Email:** \`your-email@example.com\`  
🔗 **GitHub:** [https://github.com/YOUR_GITHUB_USERNAME](https://github.com/YOUR_GITHUB_USERNAME)

🚀 **Now Your Project is Fully Documented!**" > README.md
