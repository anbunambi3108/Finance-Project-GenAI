"""
Simple financial chatbot (rule-based)
-----------------------------------
- Loads your `financial_data.csv`
- Answers a few predefined queries per the project brief
"""

import pandas as pd

CSV_PATH = r'C:\Users\anbun\Desktop\Portfolio projects\Finance-Project-GenAI\sec_outputs\financials.csv'  

def load_data(path=CSV_PATH):
    df = pd.read_csv(path)
    # make a simple (company -> latest year row) lookup
    df['Fiscal Year'] = pd.to_numeric(df['Fiscal Year'], errors='coerce')
    latest = df.sort_values(['Company', 'Fiscal Year']).dropna(subset=['Fiscal Year']).groupby('Company').tail(1)
    latest_lookup = latest.set_index('Company').to_dict(orient='index')
    return latest_lookup

def simple_chatbot(user_query, data_lookup):
    q = user_query.strip().lower()

    if q == "what is the total revenue?":
        # report latest by company for brevity
        lines = []
        for company, row in data_lookup.items():
            val = row.get('Total Revenue', 'N/A')
            year = int(row.get('Fiscal Year', 0)) if pd.notna(row.get('Fiscal Year')) else 'N/A'
            lines.append(f"{company}: {val} (FY {year})")
        return "Total Revenue (latest fiscal year):\n" + "\n".join(lines)

    elif q == "how has net income changed over the last year?":
        # This requires YoY % which is computed in the notebook.
        # For this simple example, we just echo latest Net Income values.
        lines = []
        for company, row in data_lookup.items():
            val = row.get('Net Income', 'N/A')
            year = int(row.get('Fiscal Year', 0)) if pd.notna(row.get('Fiscal Year')) else 'N/A'
            lines.append(f"{company}: {val} (FY {year})")
        return "Net Income (latest fiscal year):\n" + "\n".join(lines)

    elif q == "what are total assets and liabilities?":
        lines = []
        for company, row in data_lookup.items():
            assets = row.get('Total Assets', 'N/A')
            liab = row.get('Total Liabilities', 'N/A')
            year = int(row.get('Fiscal Year', 0)) if pd.notna(row.get('Fiscal Year')) else 'N/A'
            lines.append(f"{company}: Assets={assets}, Liabilities={liab} (FY {year})")
        return "Balance Sheet snapshot (latest fiscal year):\n" + "\n".join(lines)

    elif q == "what is cash flow from operating activities?":
        lines = []
        for company, row in data_lookup.items():
            cfo = row.get('Cash Flow from Operating Activities', 'N/A')
            year = int(row.get('Fiscal Year', 0)) if pd.notna(row.get('Fiscal Year')) else 'N/A'
            lines.append(f"{company}: CFOA={cfo} (FY {year})")
        return "Operating Cash Flow (latest fiscal year):\n" + "\n".join(lines)

    else:
        return "Sorry, I can only answer these predefined queries:\n" \
               "- What is the total revenue?\n" \
               "- How has net income changed over the last year?\n" \
               "- What are total assets and liabilities?\n" \
               "- What is cash flow from operating activities?"

if __name__ == "__main__":
    data = load_data()
    print("Type a query (or 'quit' to exit).")
    while True:
        user = input("> ")
        if user.strip().lower() in ("quit", "exit"):
            break
        print(simple_chatbot(user, data))
