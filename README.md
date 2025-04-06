# 🚀 SHL Assessment Recommender

This project recommends SHL assessments based on a job description or slug/URL using OpenAI and FastAPI, with a Streamlit frontend for easy interaction.

---

## 🧠 How It Works

1. **Input**: SHL job description URL or slug (e.g., `account-manager-solution`)
2. **Scraping**: The backend fetches and cleans the job page content
3. **AI Parsing**: OpenAI analyzes the content and recommends relevant SHL assessments
4. **Output**: A structured table with assessment details (name, type, duration, etc.)
![image](https://github.com/user-attachments/assets/f092128e-8174-4afe-9a7e-0786b703194e)

---

## 🛠 Tech Stack

- **Backend**: FastAPI, OpenAI API
- **Frontend**: Streamlit
- **Scraping**: BeautifulSoup + Selenium (optional)
- **LLM Parsing**: LangChain + Markdown Table Parser

---



  
