import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_turnout_distribution(df: pd.DataFrame, output_dir: str) -> None:
    plt.figure(figsize=(8, 5))
    plt.hist(df["turnout_rate"], bins=30)
    plt.xlabel("Turnout Rate")
    plt.ylabel("Number of Precincts")
    plt.title("Distribution of Turnout Rates")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "turnout_distribution.png"))
    plt.close()


def plot_absentee_distribution(df: pd.DataFrame, output_dir: str) -> None:
    plt.figure(figsize=(8, 5))
    plt.hist(df["absentee_share"], bins=30)
    plt.xlabel("Absentee Vote Share")
    plt.ylabel("Number of Precincts")
    plt.title("Distribution of Absentee Voting Share")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "absentee_distribution.png"))
    plt.close()


def plot_anomaly_scores(df: pd.DataFrame, output_dir: str) -> None:
    plt.figure(figsize=(8, 5))
    plt.hist(df["anomaly_score"], bins=30)
    plt.xlabel("Anomaly Score")
    plt.ylabel("Number of Precincts")
    plt.title("Distribution of Anomaly Scores")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "anomaly_score_distribution.png"))
    plt.close()


def main() -> None:
    input_path = os.path.join("outputs", "anomaly_results.csv")
    output_dir = "outputs"

    df = pd.read_csv(input_path)

    plot_turnout_distribution(df, output_dir)
    plot_absentee_distribution(df, output_dir)
    plot_anomaly_scores(df, output_dir)

    print("Saved plots to outputs/")


if __name__ == "__main__":
    main()