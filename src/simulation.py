import os
import numpy as np
import pandas as pd


def generate_election_data(
    n_precincts: int = 300,
    anomaly_fraction: float = 0.05,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Generate simulated precinct-level election data.

    Parameters
    ----------
    n_precincts : int
        Number of precincts to simulate.
    anomaly_fraction : float
        Fraction of precincts intentionally injected with unusual patterns.
    random_seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        Simulated election dataset.
    """
    rng = np.random.default_rng(random_seed)

    precinct_ids = [f"P{str(i).zfill(4)}" for i in range(1, n_precincts + 1)]

    # Simulate number of registered voters in each precinct
    registered_voters = rng.integers(800, 5000, size=n_precincts)

    # Simulate turnout rates (mostly normal)
    turnout_rate = rng.normal(loc=0.68, scale=0.08, size=n_precincts)
    turnout_rate = np.clip(turnout_rate, 0.35, 0.95)

    # Simulate voting method shares
    absentee_share = rng.normal(loc=0.22, scale=0.07, size=n_precincts)
    absentee_share = np.clip(absentee_share, 0.02, 0.60)

    early_share = rng.normal(loc=0.18, scale=0.06, size=n_precincts)
    early_share = np.clip(early_share, 0.01, 0.50)

    # Ensure absentee + early does not exceed total reasonable share
    combined = absentee_share + early_share
    too_high = combined > 0.85
    early_share[too_high] = 0.85 - absentee_share[too_high]

    # Simulate candidate A vote share
    candidate_a_share = rng.normal(loc=0.51, scale=0.10, size=n_precincts)
    candidate_a_share = np.clip(candidate_a_share, 0.20, 0.80)

    # Total votes
    total_votes = np.round(registered_voters * turnout_rate).astype(int)

    absentee_votes = np.round(total_votes * absentee_share).astype(int)
    early_votes = np.round(total_votes * early_share).astype(int)

    # Provisional ballots are usually small
    provisional_votes = rng.poisson(lam=3, size=n_precincts)
    provisional_votes = np.minimum(provisional_votes, np.maximum(total_votes // 20, 1))

    # Election-day votes = total - absentee - early
    election_day_votes = total_votes - absentee_votes - early_votes
    election_day_votes = np.maximum(election_day_votes, 0)

    candidate_a_votes = np.round(total_votes * candidate_a_share).astype(int)
    candidate_b_votes = total_votes - candidate_a_votes

    df = pd.DataFrame({
        "precinct_id": precinct_ids,
        "registered_voters": registered_voters,
        "turnout_rate": turnout_rate,
        "total_votes": total_votes,
        "absentee_share": absentee_share,
        "absentee_votes": absentee_votes,
        "early_share": early_share,
        "early_votes": early_votes,
        "election_day_votes": election_day_votes,
        "provisional_votes": provisional_votes,
        "candidate_a_votes": candidate_a_votes,
        "candidate_b_votes": candidate_b_votes,
    })

    # Inject anomalies into a small subset
    n_anomalies = max(1, int(n_precincts * anomaly_fraction))
    anomaly_indices = rng.choice(n_precincts, size=n_anomalies, replace=False)

    for idx in anomaly_indices:
        anomaly_type = rng.choice(["high_turnout", "high_absentee", "vote_skew", "high_provisional"])

        if anomaly_type == "high_turnout":
            df.loc[idx, "turnout_rate"] = rng.uniform(0.93, 0.99)
            df.loc[idx, "total_votes"] = int(df.loc[idx, "registered_voters"] * df.loc[idx, "turnout_rate"])

        elif anomaly_type == "high_absentee":
            df.loc[idx, "absentee_share"] = rng.uniform(0.70, 0.90)
            df.loc[idx, "absentee_votes"] = int(df.loc[idx, "total_votes"] * df.loc[idx, "absentee_share"])

        elif anomaly_type == "vote_skew":
            skew_share = rng.choice([rng.uniform(0.90, 0.98), rng.uniform(0.02, 0.10)])
            df.loc[idx, "candidate_a_votes"] = int(df.loc[idx, "total_votes"] * skew_share)
            df.loc[idx, "candidate_b_votes"] = df.loc[idx, "total_votes"] - df.loc[idx, "candidate_a_votes"]

        elif anomaly_type == "high_provisional":
            df.loc[idx, "provisional_votes"] = rng.integers(50, 150)

        # Recompute dependent columns if needed
        df.loc[idx, "early_votes"] = int(df.loc[idx, "total_votes"] * df.loc[idx, "early_share"])
        df.loc[idx, "absentee_votes"] = int(df.loc[idx, "total_votes"] * df.loc[idx, "absentee_share"])
        df.loc[idx, "election_day_votes"] = max(
            int(df.loc[idx, "total_votes"] - df.loc[idx, "absentee_votes"] - df.loc[idx, "early_votes"]),
            0
        )

    df["is_injected_anomaly"] = 0
    df.loc[anomaly_indices, "is_injected_anomaly"] = 1

    return df


def main() -> None:
    os.makedirs("data", exist_ok=True)

    df = generate_election_data()
    output_path = os.path.join("data", "simulated_election_data.csv")
    df.to_csv(output_path, index=False)

    print(f"Saved simulated data to: {output_path}")
    print(df.head())
    print("\nInjected anomalies:", df["is_injected_anomaly"].sum())


if __name__ == "__main__":
    main()