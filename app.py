import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from src.rules import answer_question

st.set_page_config(page_title="Election Integrity Dashboard", layout="wide")

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("outputs/anomaly_explanations.csv")

# -----------------------------
# Helper functions
# -----------------------------
def classify_anomaly_type(explanation: str) -> str:
    text = str(explanation).lower()
    if "turnout" in text:
        return "High Turnout"
    elif "absentee" in text:
        return "Absentee Spike"
    elif "provisional" in text:
        return "Provisional Spike"
    elif "candidate a" in text or "candidate b" in text or "vote skew" in text:
        return "Vote Skew"
    else:
        return "Mixed / Other"


def risk_level(row: pd.Series) -> str:
    if row["anomaly_label"] == -1 and row["anomaly_score"] < -0.05:
        return "High"
    elif row["anomaly_label"] == -1:
        return "Medium"
    else:
        return "Low"


df["anomaly_type"] = df["explanation"].apply(classify_anomaly_type)
df["risk_level"] = df.apply(risk_level, axis=1)

flagged_df = df[df["anomaly_label"] == -1].copy().sort_values("anomaly_score")
display_df = df.copy()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Filters")
show_only_flagged = st.sidebar.checkbox("Show only flagged precincts", value=False)

selected_risk = st.sidebar.multiselect(
    "Filter by risk level",
    options=["High", "Medium", "Low"],
    default=["High", "Medium", "Low"],
)

if show_only_flagged:
    display_df = flagged_df.copy()

display_df = display_df[display_df["risk_level"].isin(selected_risk)]

# -----------------------------
# Header
# -----------------------------
st.title("🗳️ Election Integrity Analytics Dashboard")
st.markdown(
    """
This dashboard presents simulated precinct-level election data, anomaly detection results,
interpretable explanations, and a lightweight election rules assistant.
"""
)

# -----------------------------
# KPI Cards
# -----------------------------
total_precincts = len(df)
flagged_precincts = (df["anomaly_label"] == -1).sum()
injected_anomalies = df["is_injected_anomaly"].sum()
avg_turnout = df["turnout_rate"].mean()
avg_absentee = df["absentee_share"].mean()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Precincts", total_precincts)
col2.metric("Flagged Precincts", flagged_precincts)
col3.metric("Injected Anomalies", injected_anomalies)
col4.metric("Avg Turnout", f"{avg_turnout:.1%}")
col5.metric("Avg Absentee Share", f"{avg_absentee:.1%}")

st.divider()

# -----------------------------
# Executive Summary
# -----------------------------
st.subheader("Executive Summary")

if len(flagged_df) > 0:
    most_common_anomaly = flagged_df["anomaly_type"].value_counts().idxmax()
else:
    most_common_anomaly = "None"

summary_text = f"""
This simulated election dataset contains **{total_precincts} precincts**, of which
**{flagged_precincts}** were flagged by the anomaly detection model.
The average turnout rate is **{avg_turnout:.1%}**, and the average absentee voting share is
**{avg_absentee:.1%}**. The most common anomaly type is **{most_common_anomaly}**.

These flagged cases are not treated as evidence of wrongdoing. Instead, they represent
patterns that may warrant closer administrative review within existing oversight mechanisms.
"""
st.markdown(summary_text)

st.divider()

# -----------------------------
# Charts
# -----------------------------
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Turnout Distribution")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.hist(df["turnout_rate"], bins=30)
    ax1.set_xlabel("Turnout Rate")
    ax1.set_ylabel("Precinct Count")
    st.pyplot(fig1)

with right_col:
    st.subheader("Absentee Voting Share Distribution")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.hist(df["absentee_share"], bins=30)
    ax2.set_xlabel("Absentee Vote Share")
    ax2.set_ylabel("Precinct Count")
    st.pyplot(fig2)

left_col2, right_col2 = st.columns(2)

with left_col2:
    st.subheader("Turnout vs. Absentee Share")
    fig3, ax3 = plt.subplots(figsize=(8, 4))

    normal = df[df["anomaly_label"] == 1]
    anomalous = df[df["anomaly_label"] == -1]

    ax3.scatter(
        normal["turnout_rate"],
        normal["absentee_share"],
        alpha=0.6,
        label="Normal"
    )
    ax3.scatter(
        anomalous["turnout_rate"],
        anomalous["absentee_share"],
        alpha=0.9,
        label="Flagged"
    )

    ax3.set_xlabel("Turnout Rate")
    ax3.set_ylabel("Absentee Share")
    ax3.legend()
    st.pyplot(fig3)

with right_col2:
    st.subheader("Flagged Anomaly Types")
    if len(flagged_df) > 0:
        anomaly_counts = flagged_df["anomaly_type"].value_counts()
        fig4, ax4 = plt.subplots(figsize=(8, 4))
        ax4.pie(
            anomaly_counts.values,
            labels=anomaly_counts.index,
            autopct="%1.1f%%"
        )
        st.pyplot(fig4)
    else:
        st.info("No flagged anomalies to display.")

st.divider()

# -----------------------------
# Top Flagged Precincts
# -----------------------------
st.subheader("🚨 Top Flagged Precincts")

if len(flagged_df) > 0:
    st.dataframe(
        flagged_df[
            [
                "precinct_id",
                "risk_level",
                "turnout_rate",
                "absentee_share",
                "provisional_votes",
                "anomaly_score",
                "anomaly_type",
                "explanation",
            ]
        ].head(10),
        use_container_width=True,
    )
else:
    st.info("No flagged precincts available.")

st.divider()

# -----------------------------
# Precinct Results Table
# -----------------------------
st.subheader("Precinct Results")

st.dataframe(
    display_df[
        [
            "precinct_id",
            "risk_level",
            "turnout_rate",
            "absentee_share",
            "provisional_votes",
            "anomaly_score",
            "anomaly_label",
            "anomaly_type",
            "explanation",
        ]
    ],
    use_container_width=True,
)

st.divider()

# -----------------------------
# Search Precinct
# -----------------------------
st.subheader("Search Precinct")
precinct = st.text_input("Enter precinct ID (example: P0001)")

if precinct:
    result = df[df["precinct_id"] == precinct.upper()]

    if len(result) > 0:
        row = result.iloc[0]

        avg_turnout_dataset = df["turnout_rate"].mean()
        avg_absentee_dataset = df["absentee_share"].mean()

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Risk Level", row["risk_level"])
        col_b.metric("Turnout", f"{row['turnout_rate']:.1%}")
        col_c.metric("Absentee Share", f"{row['absentee_share']:.1%}")

        col_d, col_e = st.columns(2)
        col_d.metric(
            "Turnout vs Avg",
            f"{(row['turnout_rate'] - avg_turnout_dataset):+.1%}"
        )
        col_e.metric(
            "Absentee vs Avg",
            f"{(row['absentee_share'] - avg_absentee_dataset):+.1%}"
        )

        st.markdown("**Explanation**")
        st.write(row["explanation"])

        st.markdown("**Detailed Record**")
        st.dataframe(result.T, use_container_width=True)
    else:
        st.warning("Precinct not found.")

st.divider()

# -----------------------------
# Rules Assistant
# -----------------------------
st.subheader("📘 Minnesota Election Rules Assistant")

button_col1, button_col2, button_col3, button_col4 = st.columns(4)

preset_question = None
with button_col1:
    if st.button("Recount Rules"):
        preset_question = "What triggers recount in Minnesota?"
with button_col2:
    if st.button("Absentee Voting"):
        preset_question = "How does absentee voting work?"
with button_col3:
    if st.button("Audits"):
        preset_question = "What audits are required?"
with button_col4:
    if st.button("Registration"):
        preset_question = "How does voter registration work?"

user_question = st.text_input(
    "Ask a question about recounts, absentee voting, audits, registration, or equipment:",
    value=preset_question if preset_question else ""
)

if user_question:
    response = answer_question(user_question)
    st.markdown("**Answer:**")
    st.write(response.strip())