# 🗳️ Election Integrity Analytics Dashboard

An interactive analytics platform that simulates precinct-level election data, detects unusual voting patterns, and provides interpretable explanations aligned with election administration procedures.

Built using **Python**, **Pandas**, **Scikit-learn**, **Matplotlib**, and **Streamlit**.

---

# 📌 Project Motivation

Election systems rely on transparency, audits, recount procedures, and administrative safeguards to maintain public trust.

This project explores how lightweight data analytics tools may help identify **unusual precinct-level patterns** that could justify closer administrative review.

Importantly, the system is **not designed to detect fraud or make legal accusations**.  
Instead, it demonstrates how analytics can support oversight, explainability, and policy understanding.

---

# 🚀 Key Features

### 📊 Simulated Election Dataset

Generates realistic precinct-level election data including:

- Registered voters
- Turnout rate
- Election Day voting
- Early voting
- Absentee/mail voting
- Provisional ballots
- Candidate vote totals

---

### 🤖 Anomaly Detection Engine

Uses unsupervised anomaly detection to flag precincts with unusual patterns such as:

- Extremely high turnout
- Elevated absentee voting share
- Provisional ballot spikes
- Rare combinations of voting behavior
- Extreme vote concentration

---

### 🧠 Explainable Analytics

Each flagged precinct receives a human-readable explanation.

Examples:

- Mild vote concentration toward Candidate B (93%)
- Unusually high absentee voting share relative to peer precincts
- Extreme provisional ballot spike requiring review

---

### 📘 Election Rules Assistant

A lightweight rule-based assistant that explains Minnesota election procedures:

- Recount rules
- Absentee voting procedures
- Post-election audits
- Voter registration
- Voting equipment types

Interactive rule lookup system supporting questions such as:

- What triggers recount in Minnesota?
- How does absentee voting work?
- What audits are required?

---

### 📈 Interactive Dashboard Overview

The project includes a Streamlit-based interactive dashboard that allows users to explore simulated election data, anomaly detection results, and election procedure rules in a visual and user-friendly format.

Key dashboard functions include:

- **Election Summary Metrics**: Displays total precincts, flagged anomalies, average turnout, and absentee voting share.
- **Distribution Analysis**: Visualizes turnout rates and absentee voting behavior across precincts.
- **Outlier Detection View**: Highlights flagged precincts that deviate from normal voting patterns.
- **Scatter Plot Exploration**: Compares turnout and absentee share to identify unusual combinations.
- **Anomaly Type Breakdown**: Summarizes the categories of detected anomalies (turnout spikes, absentee spikes, provisional ballot spikes, etc.).
- **Precinct Search Tool**: Allows users to inspect detailed statistics for any selected precinct.
- **Rules Assistant**: Provides quick natural-language explanations of Minnesota election procedures such as recounts, absentee voting, and audits.

The dashboard demonstrates how data analytics and interpretable AI tools can support election transparency, administrative review, and policy understanding.

![Dashboard](outputs/dashboard_screenshot2.png)
![Dashboard](outputs/dashboard_screenshot1.png)
![Dashboard](outputs/dashboard3.png)
![Dashboard](outputs/dashboard4.png)
![Dashboard](outputs/dashboard5.png)
![Dashboard](outputs/dashboard6.png)
![Dashboard](outputs/dashboard7.png)
![Dashboard](outputs/dashboard8.png)
![Dashboard](outputs/dashboard_screenshot9.png)
![Dashboard](outputs/dashboard9.png)
![Dashboard](outputs/dashboard10.png)
![Dashboard](outputs/dashboard_screenshot10.png)

---

## 📊 Example Insights

### Turnout vs Absentee Share

Most precincts cluster within normal administrative ranges.

Flagged precincts appear as outliers with unusual turnout, absentee voting, or combined behaviors.

### Flagged Anomaly Types

Detected anomalies commonly involve:

- Turnout spikes
- Absentee spikes
- Provisional ballot spikes
- Vote concentration patterns

These signals are designed for administrative review rather than enforcement.

---

## 🏗️ System Architecture

```
Simulation Engine
      ↓
Election Dataset
      ↓
Anomaly Detection
      ↓
Explanation Layer
      ↓
Dashboard + Rules Assistant
```

## 📂 Project Architecture

```
election-analytics/
│── data/
│   └── simulated_election_data.csv
│
│── outputs/
│   ├── anomaly_results.csv
│   ├── anomaly_explanations.csv
│   ├── turnout_distribution.png
│   ├── absentee_distribution.png
│   ├── anomaly_score_distribution.png
│   └── dashboard_screenshot.png
│
│── src/
│   ├── simulation.py
│   ├── anomaly.py
│   ├── explain.py
│   ├── rules.py
│   └── visualization.py
│
│── app.py
│── requirements.txt
│── README.md
```

## ⚙️ Tech Stack

- Python 3.10
- Anaconda
- pandas
- numpy
- scikit-learn
- matplotlib
- streamlit

## 🖥️ Quick Start

Create Environment

```
conda create -n election-ai python=3.10 -y
conda activate election-ai
pip install pandas numpy scikit-learn matplotlib streamlit
```

Run Modules
```
python src/simulation.py
python src/anomaly.py
python src/explain.py
streamlit run app.py
```

## 📈 Example Outputs

- Turnout distribution
- Absentee voting histogram
- Flagged precinct table
- Search precinct records
- Election procedure Q&A

## 🎯 Use Cases

- Election administration research
- Audit workflow simulation
- Policy education
- Data anomaly detection case study
- Explainable AI demonstration

## 📊 Experimental Results & Interpretation

### 1. Turnout Rate Distribution

![Turnout](outputs/turnout_distribution.png)

The simulated turnout rates are centered around typical participation levels, with most precincts falling between **60% and 80% turnout**. A small number of precincts exhibit unusually high turnout, which may warrant further review in anomaly detection workflows.

---

### 2. Absentee Voting Share Distribution

![Absentee](outputs/absentee_distribution.png)

Most precincts display absentee voting shares between **15% and 35%**, reflecting normal variation in mail voting usage. A few extreme outliers show significantly elevated absentee shares, representing potential irregular patterns for administrative review.

---

### 3. Anomaly Score Distribution

![Anomaly Score](outputs/anomaly_score_distribution.png)

The Isolation Forest model assigns anomaly scores across precincts. Most precincts cluster in the normal range, while a smaller subset receives substantially lower scores and is flagged as anomalous.

These anomalies may correspond to:

- unusually high turnout
- abnormal absentee ballot concentration
- extreme candidate vote imbalance
- elevated provisional ballot counts

---

### 4. Explainable Flagging

Example flagged precinct explanations:

```
P0021 – turnout rate significantly exceeds peer precinct average
P0047 – absentee voting share unusually high relative to county norm
P0113 – provisional ballot volume exceeds expected operational range
```

This improves transparency by showing why a precinct was flagged rather than relying solely on black-box model outputs.

---

### 5. Governance Relevance

This project does not attempt to detect fraud or assign misconduct.

Instead, it demonstrates how interpretable analytics may assist:

- post-election audits
- recount prioritization
- operational anomaly review
- public-sector transparency workflows
- election administration research

---

###  6. Results Interpretation

![result](outputs/dashboard_screenshot1.png)

#### Turnout vs. Absentee Share

Most precincts fall within normal turnout and absentee voting ranges.  
Flagged precincts appear as outliers with unusually high turnout, elevated absentee shares, or rare combinations of voting behavior.

#### Flagged Anomaly Types

Among flagged precincts, the most common categories involve turnout spikes, provisional ballot spikes, and absentee voting anomalies.

These results illustrate how data analytics may support election oversight by identifying cases for additional review.

---

## Key Findings

- Simulated and analyzed 300 precinct-level election records
- Detected 15 statistically unusual precinct patterns via Isolation Forest
- Built an interactive Streamlit dashboard for public-sector analytics
- Added explainable AI outputs for transparent anomaly interpretation
- Integrated rule-based election policy assistant for Minnesota procedures

---

## ⚖️ Disclaimer

This project does not detect or claim election fraud.

It demonstrates how analytical tools may support existing election oversight mechanisms.

---

## Future Work

- Integrate real public election datasets
- Multi-state policy comparison
- Additional anomaly detection models
- Natural language legal QA module
- Public deployment
