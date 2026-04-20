import pandas as pd


def generate_explanation(row):
    score = row["anomaly_score"]
    risk = row["risk_level"]

    turnout = row["turnout_rate"]
    absentee = row["absentee_share"]
    provisional = row["provisional_votes"]

    cand_a = row["candidate_a_votes"]
    cand_b = row["candidate_b_votes"]

    total_votes = max(row["total_votes"], 1)

    share_a = cand_a / total_votes
    share_b = cand_b / total_votes

    # --------------------------
    # wording by risk level
    # --------------------------
    if risk == "High":
        turnout_word = "extremely high"
        absentee_word = "extremely high"
        provisional_word = "extreme spike in"
        skew_word = "extreme vote concentration toward"

    elif risk == "Medium":
        turnout_word = "unusually high"
        absentee_word = "unusually high"
        provisional_word = "unusual increase in"
        skew_word = "notable vote concentration toward"

    else:
        turnout_word = "moderately elevated"
        absentee_word = "moderately elevated"
        provisional_word = "mild increase in"
        skew_word = "mild vote concentration toward"

    explanations = []

    # turnout
    if turnout > 0.90:
        explanations.append(
            f"{turnout_word} turnout rate ({turnout:.2f})"
        )

    # absentee
    if absentee > 0.50:
        explanations.append(
            f"{absentee_word} absentee voting share ({absentee:.2f})"
        )

    # provisional
    if provisional > 80:
        explanations.append(
            f"{provisional_word} provisional ballots ({provisional})"
        )

    # vote skew
    if share_a > 0.90:
        explanations.append(
            f"{skew_word} Candidate A ({share_a:.2f})"
        )

    elif share_b > 0.90:
        explanations.append(
            f"{skew_word} Candidate B ({share_b:.2f})"
        )

    # fallback
    if not explanations:
        if risk == "High":
            return "Multiple indicators deviate substantially from normal precinct patterns."
        elif risk == "Medium":
            return "Several indicators appear unusual relative to peer precincts."
        else:
            return "Minor variation observed within generally normal precinct ranges."

    return "; ".join(explanations)


def main():
    df = pd.read_csv("outputs/anomaly_results.csv")

    # Ensure risk level exists
    if "risk_level" not in df.columns:
        def risk(score):
            if score < -0.05:
                return "High"
            elif score < 0:
                return "Medium"
            else:
                return "Low"

        df["risk_level"] = df["anomaly_score"].apply(risk)

    df["explanation"] = df.apply(generate_explanation, axis=1)

    df.to_csv("outputs/anomaly_explanations.csv", index=False)

    print("Saved: outputs/anomaly_explanations.csv")


if __name__ == "__main__":
    main()