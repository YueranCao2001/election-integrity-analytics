import textwrap


RULES_DB = {
    "recount": """
Minnesota provides automatic recounts in certain close contests.
For statewide races, a publicly funded recount may occur when the margin
is very small relative to total votes cast. Candidates may also request
recounts under certain conditions.
""",

    "absentee": """
Minnesota allows no-excuse absentee voting.
Eligible voters may request an absentee ballot before Election Day.
Returned ballots are reviewed for eligibility and signature compliance.
""",

    "audit": """
Minnesota conducts post-election reviews of randomly selected precincts.
These audits compare paper ballots against machine tabulation results
to verify election accuracy.
""",

    "equipment": """
Minnesota primarily uses paper ballots counted by optical scan systems.
This supports recounts and audits because voter-marked paper ballots
remain available for review.
""",

    "registration": """
Minnesota is known for same-day voter registration.
Eligible voters may register or update registration at polling places
with required identification or proof of residence.
""",

    "provisional": """
Minnesota does not use provisional ballots in the same way as many states.
Instead, same-day registration procedures reduce the need for provisional voting.
"""
}


def answer_question(question: str) -> str:
    q = question.lower()

    if "recount" in q:
        return RULES_DB["recount"]

    elif "absentee" in q or "mail" in q:
        return RULES_DB["absentee"]

    elif "audit" in q:
        return RULES_DB["audit"]

    elif "equipment" in q or "machine" in q or "voting system" in q:
        return RULES_DB["equipment"]

    elif "register" in q or "registration" in q:
        return RULES_DB["registration"]

    elif "provisional" in q:
        return RULES_DB["provisional"]

    else:
        return """
Sorry, I do not have a rule for that question yet.

Try asking about:
- recount
- absentee voting
- audits
- equipment
- registration
"""


def main():
    print("=" * 60)
    print("Minnesota Election Rules Assistant")
    print("=" * 60)

    while True:
        question = input("\nAsk a question (or type quit): ")

        if question.lower() in ["quit", "exit"]:
            print("Goodbye.")
            break

        answer = answer_question(question)

        print("\nAnswer:\n")
        print(textwrap.fill(answer.strip(), width=75))


if __name__ == "__main__":
    main()