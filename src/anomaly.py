import os
import pandas as pd
from sklearn.ensemble import IsolationForest


FEATURE_COLUMNS = [
    "turnout_rate",
    "absentee_share",
    "early_share",
    "provisional_votes",
    "candidate_a_votes",
    "candidate_b_votes",
    "total_votes",
]


def run_anomaly_detection(input_path: str) -> pd.DataFrame:
    """
    Run anomaly detection on simulated election data.

    Parameters
    ----------
    input_path : str
        Path to the simulated CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame with anomaly predictions and scores.
    """
    df = pd.read_csv(input_path)

    X = df[FEATURE_COLUMNS].copy()

    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42
    )
    model.fit(X)

    df["anomaly_label"] = model.predict(X)   # -1 = anomaly, 1 = normal
    df["anomaly_score"] = model.decision_function(X)

    return df


def main() -> None:
    input_path = os.path.join("data", "simulated_election_data.csv")
    output_path = os.path.join("outputs", "anomaly_results.csv")

    os.makedirs("outputs", exist_ok=True)

    df = run_anomaly_detection(input_path)
    df.to_csv(output_path, index=False)

    flagged = df[df["anomaly_label"] == -1].sort_values("anomaly_score")

    print(f"Saved anomaly results to: {output_path}")
    print("\nTop flagged precincts:")
    print(
        flagged[
            [
                "precinct_id",
                "turnout_rate",
                "absentee_share",
                "provisional_votes",
                "candidate_a_votes",
                "candidate_b_votes",
                "anomaly_score",
                "is_injected_anomaly",
            ]
        ].head(10)
    )


if __name__ == "__main__":
    main()