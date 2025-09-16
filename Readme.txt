# 📊 Finance Project — GenAI-Ready Financial Assistant

## 📖 About the Project
This project showcases a **GenAI-ready financial assistant**.  
It connects **scraped SEC 10-K financial data** to a chatbot interface.  
Currently, the chatbot provides **rule-based answers** to key finance questions, but the design is extendable — it can be integrated with **Large Language Models (LLMs)** to enable **natural language understanding** and **generative financial insights**.

---

## 📂 About the Data
- **Source**: SEC EDGAR API  
- **Format**: Collected 10-K filings → cleaned & stored in **Excel and CSV**  
- **Companies**: Microsoft, Apple, Tesla  
- Covers the **last 3 fiscal years** of each company

---

## 🛠️ Tools & Tech Stack
**Languages & Libraries**
- 🐍 **Python** — core programming language  
- 📑 **pandas** — data collection, cleaning, and analysis (YoY growth, metrics)  
- 📈 **matplotlib** — charts and trend visualization in the notebook  
- 🌐 **Streamlit** — interactive chatbot interface with a browser-based UI  

---

## ⭐ STAR Framework

**S — Situation**  
Analyzing real company financials from SEC 10-K reports and building a simple AI-style chatbot to answer financial questions.  

**T — Task**  
Extract the last 3 years of financial data (Microsoft, Apple, Tesla), analyze key metrics, and design a chatbot for predefined queries.  

**A — Action**  
- Scraped **SEC EDGAR** with Python (`requests`, `pandas`).  
- Extracted **Total Revenue, Net Income, Assets, Liabilities, Cash Flow**.  
- Cleaned and stored results in **CSV/Excel** for analysis.  
- Used **Jupyter Notebook** for YoY growth calculations and charts.  
- Built a **rule-based chatbot** (command-line + Streamlit UI).  

**R — Result**  
- Delivered a structured dataset covering 3 fiscal years per company.  
- Identified key insights: Tesla’s volatility, Apple’s steady growth, Microsoft’s stability.  
- Built a functional chatbot that answers 4 finance questions via CLI and UI.  
- End-to-end pipeline: **data scraping → analysis → chatbot interface**, ready for GenAI extension.  

---

## 🔮 Future Scope
- Extend chatbot with **LLMs (Large Language Models)** for:  
  - Free-text queries (not just predefined).  
  - Generative explanations of financial performance.  
  - Comparative and predictive insights.  

---
