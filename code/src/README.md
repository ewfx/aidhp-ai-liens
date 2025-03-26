# 🚀 FinVasion – Your Smart Finance Partner

## 📌 Table of Contents
- [Introduction](#-introduction)
- [Demo](#-demo)
- [Inspiration](#-inspiration)
- [What It Does](#-what-it-does)
- [How We Built It](#-how-we-built-it)
- [Challenges We Faced](#-challenges-we-faced)
- [How to Run](#-how-to-run)
- [Tech Stack](#-tech-stack)
- [Team](#-team)

---

## 🎯 Introduction

**FinVasion** is a fintech intelligence app designed to help users take control of their financial lives. By combining sentiment analysis, risk profiling, and transaction history, it provides **personalized financial recommendations**—from credit cards to loans and investments. 

We aim to bridge the gap between traditional banking products and hyper-personalized advisory experiences powered by GenAI.

---

## 🎥 Demo

🔗 [Live Demo](#)  
📹 [Video Walkthrough](#)  
🖼️ Screenshots:

![Screenshot 1](link-to-your-image.png)  
![Screenshot 2](link-to-your-image.png)

---

## 💡 Inspiration

We saw a recurring problem—people struggle to find financial products that suit their unique needs, especially when it comes to risk appetite and income behavior. Most platforms offer generic suggestions. We wanted to build a system that is **intelligent, contextual, and adaptive**.

---

## ⚙️ What It Does

- 🔐 **User Authentication** with unique `CUSTXXXX` ID system
- 📊 **Risk Score Calculation** based on income vs. spending patterns
- 🧠 **Sentiment Analysis** using social media cues to infer financial confidence
- 💳 **Personalized Product Recommendations** like loans, cards, and SIPs
- ✅ **Smart Dashboard**: Highlights best-fit offers with recommendation signals
- 🎓 **Context-Aware Matching**: Uses education, occupation, and interests

---

## 🛠️ How We Built It

- Backend with **FastAPI** for modular and fast REST APIs
- Frontend with **React + Material UI** for a modern, responsive UI
- **MongoDB** for user, transaction, and sentiment storage
- **Hugging Face API** for sentiment and LLM-based recommendations
- JWT-based **secure authentication system**
- Custom logic to simulate a **banking partner ecosystem**

---

## 🚧 Challenges We Faced

- Fine-tuning the sentiment model to financial context
- Designing a dynamic UI that reacts to changing user scores
- Generating consistent dummy financial product logic
- Avoiding API rate limits while testing with Hugging Face inference models
- Ensuring proper error handling between frontend-backend calls

---

## 🏃 How to Run

1. **Clone the repository**
```bash
git clone https://github.com/your-username/finvasion.git
cd finvasion

2.Backend
Note: Temporarily move the files inside the venv dir outside and delete the venv directory temporarily before running the commands.

cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
Note: Temporarily move the files inside the venv dir outside temporarily

3.Environment
Note: create `key.env` file in the backend folder inside the venv once it is created with the below structure.
HUGGINGFACE_API_KEY=your_hf_key
SECRET_KEY=your_jwt_secret

4.Run FastAPI server
uvicorn main:app --reload

5.Frontend (From the /code/src directory of the project)
cd frontend
npm install
npm start


TECH-STACK
🔹 Frontend: React, Material UI

🔹 Backend: FastAPI (Python)

🔹 Database: MongoDB

🔹 Models: Hugging Face Transformers (roberta, Mistral 7B, etc.)

🔹 Authentication: JWT (PyJWT)

🔹 Deployment: Uvicorn / Localhost

Team:
Sana, Vikramasimha Reddy - Software Engineer
Lal, Goutham S - Software Engineer
Dixit, Chinmay - Software Engineer
Chanda, Susmitha - Software Engineer
G, Sharan - Intern Analyst
