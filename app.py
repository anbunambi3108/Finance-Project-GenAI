import pandas as pd
import streamlit as st

st.set_page_config(page_title="Financial Chatbot", page_icon="💬", layout="wide")
st.title("💬 Financial Chatbot")

# ---------- Load data ----------
CSV_PATH = r'C:\Users\anbun\Desktop\Portfolio projects\Finance-Project-GenAI\sec_outputs\financials.csv'  # make sure this file is in the same folder

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # Normalize column names (strip spaces)
    df.columns = [c.strip() for c in df.columns]

    # Support either column name: "Operating Cash Flow" or "Cash Flow from Operating Activities"
    if "Operating Cash Flow" in df.columns:
        ocf_col = "Operating Cash Flow"
    elif "Cash Flow from Operating Activities" in df.columns:
        ocf_col = "Cash Flow from Operating Activities"
    else:
        ocf_col = None

    # Ensure expected columns exist
    required = {"Company", "Fiscal Year", "Total Revenue", "Net Income", "Total Assets", "Total Liabilities"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing columns: {missing}. Edit your CSV or script to include them.")

    # Coerce numerics
    num_cols = ["Fiscal Year", "Total Revenue", "Net Income", "Total Assets", "Total Liabilities"]
    if ocf_col:
        num_cols.append(ocf_col)
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Add YoY growth if not present (just for Revenue/Net Income)
    if "Revenue Growth (%)" not in df.columns:
        df["Revenue Growth (%)"] = df.groupby("Company")["Total Revenue"].pct_change() * 100
    if "Net Income Growth (%)" not in df.columns:
        df["Net Income Growth (%)"] = df.groupby("Company")["Net Income"].pct_change() * 100

    # Round for pretty display
    for c in ["Revenue Growth (%)", "Net Income Growth (%)"]:
        if c in df.columns:
            df[c] = df[c].round(2)

    return df, ocf_col

try:
    df, OCF_COL = load_data(CSV_PATH)
except Exception as e:
    st.error(f"Could not load '{CSV_PATH}'. Error:\n{e}")
    st.stop()

# Sidebar: pick a question
st.sidebar.header("Ask a predefined question")
question = st.sidebar.selectbox(
    "Choose a question",
    [
        "What is the total revenue?",
        "How has net income changed over the last year?",
        "What are total assets and liabilities?",
        "What is cash flow from operating activities?",
    ],
)

# Also let user filter to a single company (or All)
companies = ["All"] + sorted(df["Company"].unique().tolist())
company_choice = st.sidebar.selectbox("Company filter (optional)", companies)
if company_choice != "All":
    data = df[df["Company"] == company_choice].copy()
else:
    data = df.copy()

# Compute latest-year snapshot per company
latest = (
    data.sort_values(["Company", "Fiscal Year"])
        .dropna(subset=["Fiscal Year"])
        .groupby("Company")
        .tail(1)
        .reset_index(drop=True)
)

# ---------- Answer the question ----------
st.subheader("Answer")

def fmt(n):
    # Format large ints nicely, leave N/A as-is
    return "N/A" if pd.isna(n) else f"{int(n):,}"

if question == "What is the total revenue?":
    show = latest[["Company", "Fiscal Year", "Total Revenue"]].copy()
    show["Total Revenue"] = show["Total Revenue"].apply(fmt)
    st.write("**Total Revenue (latest fiscal year):**")
    st.dataframe(show, use_container_width=True)

elif question == "How has net income changed over the last year?":
    # If YoY is present, show YoY; otherwise show latest value
    if "Net Income YoY (%)" in latest.columns:
        # If your CSV from the script already has this
        show = latest[["Company", "Fiscal Year", "Net Income", "Net Income YoY (%)"]].copy()
        show["Net Income"] = show["Net Income"].apply(fmt)
    else:
        # Fallback to computed growth column in this app
        # Need the previous year; so show full company table
        show = data.sort_values(["Company", "Fiscal Year"])[["Company", "Fiscal Year", "Net Income", "Net Income Growth (%)"]].copy()
        show["Net Income"] = show["Net Income"].apply(fmt)
    st.write("**Net Income (latest and YoY where available):**")
    st.dataframe(show, use_container_width=True)

elif question == "What are total assets and liabilities?":
    show = latest[["Company", "Fiscal Year", "Total Assets", "Total Liabilities"]].copy()
    show["Total Assets"] = show["Total Assets"].apply(fmt)
    show["Total Liabilities"] = show["Total Liabilities"].apply(fmt)
    st.write("**Balance Sheet (latest fiscal year):**")
    st.dataframe(show, use_container_width=True)

elif question == "What is cash flow from operating activities?":
    if OCF_COL is None:
        st.info("Operating cash flow column not found in CSV.")
        show = latest[["Company", "Fiscal Year"]].copy()
    else:
        show = latest[["Company", "Fiscal Year", OCF_COL]].copy()
        show[OCF_COL] = show[OCF_COL].apply(fmt)
    st.write("**Operating Cash Flow (latest fiscal year):**")
    st.dataframe(show, use_container_width=True)

# ---------- Charts ----------
st.markdown("---")
st.subheader("Trends (3 years)")

left, right = st.columns(2, gap="large")

with left:
    st.markdown("**Total Revenue by Fiscal Year**")
    rev_pivot = (
        data.pivot_table(index="Fiscal Year", columns="Company", values="Total Revenue", aggfunc="sum")
        .sort_index()
    )
    st.line_chart(rev_pivot)

with right:
    st.markdown("**Net Income by Fiscal Year**")
    ni_pivot = (
        data.pivot_table(index="Fiscal Year", columns="Company", values="Net Income", aggfunc="sum")
        .sort_index()
    )
    st.line_chart(ni_pivot)


