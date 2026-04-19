import os
import pandas as pd


def explain_row(row: pd.Series) -> str:
    """
    Generate a human-readable explanation for why a precinct
    may have been flagged as anomalous.
    """
    reasons = []

    # Threshold-based interpretations
    if row["turnout_rate"] > 0.90:
        reasons.append(f"very high turnout rate ({row['turnout_rate']:.2f})")

    if row["absentee_share"] > 0.60:
        reasons.append(f"unusually high absentee vote share ({row['absentee_share']:.2f})")

    if row["provisional_votes"] > 40:
        reasons.append(f"unusually high provisional ballot count ({int(row['provisional_votes'])})")

    total_votes = max(row["total_votes"], 1)
    candidate_a_share = row["candidate_a_votes"] / total_votes
    candidate_b_share = row["candidate_b_votes"] / total_votes

    if candidate_a_share > 0.90:
        reasons.append(f"extreme vote skew toward Candidate A ({candidate_a_share:.2f})")

    if candidate_b_share > 0.90:
        reasons.append(f"extreme vote skew toward Candidate B ({candidate_b_share:.2f})")

    if row["anomaly_score"] < 0:
        reasons.append(f"very low anomaly score ({row['anomaly_score']:.4f})")

    if not reasons:
        reasons.append("combination of unusual voting patterns across multiple variables")

    return "; ".join(reasons)


def build_explanations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add explanation text for anomalous precincts.
    """
    df = df.copy()
    df["explanation"] = df.apply(explain_row, axis=1)
    return df


def main() -> None:
    input_path = os.path.join("outputs", "anomaly_results.csv")
    output_path = os.path.join("outputs", "anomaly_explanations.csv")

    df = pd.read_csv(input_path)

    explained_df = build_explanations(df)

    # Save full results
    explained_df.to_csv(output_path, index=False)

    # Show top flagged precincts
    flagged = explained_df[explained_df["anomaly_label"] == -1].sort_values("anomaly_score")

    print(f"Saved explanations to: {output_path}")
    print("\nTop flagged precincts with explanations:\n")

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
                "explanation",
            ]
        ].head(10).to_string(index=False)
    )


if __name__ == "__main__":
    main()