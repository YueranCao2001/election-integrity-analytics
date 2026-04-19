import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from src.rules import answer_question

st.set_page_config(page_title="Election Integrity Dashboard", layout="wide")

st.title("🗳️ Election Integrity Analytics Dashboard")

st.markdown(
    """
This dashboard presents simulated precinct-level election data, anomaly detection results,
interpretable explanations, and a lightweight election rules assistant.
"""
)

# Load data
df = pd.read_csv("outputs/anomaly_explanations.csv")

# Sidebar
st.sidebar.header("Filters")
show_only_flagged = st.sidebar.checkbox("Show only flagged precincts", value=False)

if show_only_flagged:
    display_df = df[df["anomaly_label"] == -1].copy()
else:
    display_df = df.copy()

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Precincts", len(df))
col2.metric("Flagged Precincts", (df["anomaly_label"] == -1).sum())
col3.metric("Injected Anomalies", df["is_injected_anomaly"].sum())

st.divider()

# Chart 1
st.subheader("Turnout Distribution")
fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.hist(df["turnout_rate"], bins=30)
ax1.set_xlabel("Turnout Rate")
ax1.set_ylabel("Precinct Count")
st.pyplot(fig1)

# Chart 2
st.subheader("Absentee Voting Share Distribution")
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.hist(df["absentee_share"], bins=30)
ax2.set_xlabel("Absentee Vote Share")
ax2.set_ylabel("Precinct Count")
st.pyplot(fig2)

# Flagged precincts table
st.subheader("Precinct Results")
st.dataframe(
    display_df[
        [
            "precinct_id",
            "turnout_rate",
            "absentee_share",
            "provisional_votes",
            "anomaly_score",
            "anomaly_label",
            "explanation",
        ]
    ],
    use_container_width=True,
)

# Search precinct
st.subheader("Search Precinct")
precinct = st.text_input("Enter precinct ID (example: P0001)")

if precinct:
    result = df[df["precinct_id"] == precinct.upper()]
    if len(result) > 0:
        st.write(result.T)
    else:
        st.warning("Precinct not found.")

st.divider()

# Rules assistant
st.subheader("📘 Minnesota Election Rules Assistant")
user_question = st.text_input(
    "Ask a question about recounts, absentee voting, audits, registration, or equipment:"
)

if user_question:
    response = answer_question(user_question)
    st.markdown("**Answer:**")
    st.write(response.strip())