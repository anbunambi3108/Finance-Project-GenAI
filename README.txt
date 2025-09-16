# 📊 Finance Project — GenAI-Ready Financial Assistant

## 📖 About the Project
This project demonstrates a **GenAI-ready financial assistant**.  
It connects **scraped SEC 10-K financial data** to a chatbot interface that currently provides **rule-based answers** to key financial questions.  

As part of the Global Finance Corp (GFC) scenario, we built an assistant that:  
- Ingests 10-K/10-Q filings  
- Normalizes key metrics (Revenue, Net Income, Assets, Liabilities, Operating Cash Flow)  
- Delivers fast, accurate Q&A through a **Streamlit UI**  

The current MVP ensures reliability and speed with structured data. The **next step** is adding **Retrieval-Augmented Generation (RAG)** so free-text questions can be answered by an LLM, with citations to filing snippets for transparency. The solution is designed to **scale across companies**, support **caching and monitoring**, and significantly **reduce analysis time** while improving confidence in results.

---

## 📂 About the Data
- **Source**: SEC EDGAR API  
- **Format**: 10-K filings scraped, cleaned, and stored as **Excel and CSV**  
- **Coverage**: Last 3 fiscal years of each company  

---

## 🛠️ Tools & Tech Stack
**Languages & Libraries**
- 🐍 **Python** — core programming language  
- 📑 **pandas** — data collection, cleaning, and growth analysis  
- 📈 **matplotlib** — charts and visualizations in the notebook  
- 🌐 **Streamlit** — interactive chatbot interface with a browser-based UI  

---

## ⭐ STAR Framework

**Situation**  
Traditional financial analysis is slow and manual. The goal was to analyze 10-K reports and build an AI-style chatbot to make insights more accessible.  

**Task**  
Extract 3 years of financial data (Microsoft, Apple, Tesla), analyze trends (revenue, net income, balance sheet, cash flow), and design a chatbot that answers key questions.  

**A — Action**  
- Scraped **SEC EDGAR** using Python (`requests`, `pandas`).  
- Extracted **Revenue, Net Income, Assets, Liabilities, Operating Cash Flow**.  
- Cleaned and stored the data in **CSV/Excel**.  
- Performed YoY growth analysis and charts in **Jupyter Notebook**.  
- Built a **rule-based chatbot** accessible via command line and Streamlit UI.  

**Result**  
- Produced a reliable dataset covering 3 years per company.  
- Generated clear insights: Tesla shows volatility, Apple steady growth, Microsoft consistent performance.  
- Delivered a working chatbot that answers 4 key financial queries.  
- End-to-end pipeline achieved: **scraping → analysis → chatbot interface**, laying the foundation for GenAI integration.  

---

## 🔮 Future Scope
- Integrate **LLMs** to move beyond fixed queries:  
- Support **free-text questions**.  
- Provide **generative, conversational explanations** of financials.  
- Enable **comparisons and predictive insights** across companies.  
---
