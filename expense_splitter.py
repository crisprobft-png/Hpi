"""Expense Splitter: who owes whom, with a small number of payments.

Team: Crocosoftware
License: MIT
"""

# ---------------------------------------------------------------
# Segment 0: types and constants
# ---------------------------------------------------------------
# An expense is (payer, amount in EUR, people who share it).
Expense = tuple[str, float, list[str]]
# A transfer is (debtor, creditor, amount in EUR).
Transfer = tuple[str, str, float]

# Balances can be off by a few cents because of rounding.
TOLERANCE = 0.05
# Amounts below half a cent are treated as zero.
EPSILON = 0.005


# ---------------------------------------------------------------
# Segment 1 - Member 1: validate_expenses
# ---------------------------------------------------------------
def validate_expenses(expenses: list[Expense]) -> bool:
    """Check that a list of expenses is valid.

    Raises:
        ValueError: If the list is empty, a payer name is empty, an amount
            is not greater than 0, an expense has no participants, or the
            payer is not one of the participants.

    Example:
        >>> validate_expenses([("Ana", 80.0, ["Ana", "Bea"])])
        True
        >>> validate_expenses([("Ana", -5.0, ["Ana"])])  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: amount must be greater than 0
    """
    if not expenses:
        raise ValueError("the expenses list is empty")

    for payer, amount, participants in expenses:
        if not isinstance(payer, str) or not payer.strip():
            raise ValueError("payer name must be a non-empty string")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("amount must be greater than 0")
        if not participants:
            raise ValueError("an expense needs at least one participant")
        if payer not in participants:
            raise ValueError(f"payer {payer} must be one of the participants")

    return True


# ---------------------------------------------------------------
# Segment 2 - Member 2: compute_balances
# ---------------------------------------------------------------
def compute_balances(expenses: list[Expense]) -> dict[str, float]:
    """Calculate each person's net balance (paid minus owed).

    Positive balance = the person is owed money.
    Negative balance = the person owes money.

    Example:
        >>> compute_balances([
        ...     ("Ana", 80.0, ["Ana", "Bea", "Carlos", "Dani"]),
        ...     ("Bea", 40.0, ["Ana", "Bea", "Carlos", "Dani"]),
        ... ])
        {'Ana': 50.0, 'Bea': 10.0, 'Carlos': -30.0, 'Dani': -30.0}
    """
    balances: dict[str, float] = {}

    for payer, amount, participants in expenses:
        # Each participant owes an equal share of this expense.
        share = amount / len(participants)

        # The payer put in the full amount...
        balances[payer] = balances.get(payer, 0.0) + amount

        # ...and every participant (the payer included) owes their share.
        for person in participants:
            balances[person] = balances.get(person, 0.0) - share

    # Round to cents; "+ 0.0" turns a possible -0.0 into 0.0.
    return {name: round(value, 2) + 0.0 for name, value in balances.items()}


# ---------------------------------------------------------------
# Segment 3 - Member 3: settle_debts
# ---------------------------------------------------------------
def settle_debts(balances: dict[str, float]) -> list[Transfer]:
    """Find a small set of transfers that settles all debts.

    Greedy approach: the person who owes the most pays the person who
    is owed the most, as much as possible. Repeat until nobody owes.

    Raises:
        ValueError: If the balances do not add up to 0 (within TOLERANCE).

    Example:
        >>> settle_debts({"Ana": 50.0, "Bea": 10.0,
        ...               "Carlos": -30.0, "Dani": -30.0})
        [('Carlos', 'Ana', 30.0), ('Dani', 'Ana', 20.0), ('Dani', 'Bea', 10.0)]
    """
    if abs(sum(balances.values())) > TOLERANCE:
        raise ValueError("balances must add up to 0")

    # Lists of [name, amount still to pay / to receive], both positive.
    debtors = [[name, -value] for name, value in balances.items() if value < -EPSILON]
    creditors = [[name, value] for name, value in balances.items() if value > EPSILON]

    transfers: list[Transfer] = []

    while debtors and creditors:
        # Biggest debtor first, biggest creditor first.
        debtors.sort(key=lambda item: item[1], reverse=True)
        creditors.sort(key=lambda item: item[1], reverse=True)
        debtor, creditor = debtors[0], creditors[0]

        # Pay as much as possible in a single transfer.
        amount = min(debtor[1], creditor[1])
        transfers.append((debtor[0], creditor[0], round(amount, 2)))

        debtor[1] -= amount
        creditor[1] -= amount

        # Whoever reaches 0 leaves the list.
        if debtor[1] < EPSILON:
            debtors.pop(0)
        if creditor[1] < EPSILON:
            creditors.pop(0)

    return transfers


# ---------------------------------------------------------------
# Segment 4 - Member 4: format_report and main
# ---------------------------------------------------------------
def format_report(transfers: list[Transfer]) -> str:
    """Turn a list of transfers into a readable report.

    Example:
        >>> print(format_report([("Carlos", "Ana", 30.0)]))
        Carlos pays Ana 30.00 EUR
    """
    if not transfers:
        return "Everyone is settled."

    lines = [f"{debtor} pays {creditor} {amount:.2f} EUR"
             for debtor, creditor, amount in transfers]
    return "\n".join(lines)


def main() -> None:
    """Run the full pipeline on an example."""
    expenses: list[Expense] = [
        ("Ana", 80.0, ["Ana", "Bea", "Carlos", "Dani"]),
        ("Bea", 40.0, ["Ana", "Bea", "Carlos", "Dani"]),
    ]
    validate_expenses(expenses)             # 1. check the data
    balances = compute_balances(expenses)   # 2. who is owed / who owes
    transfers = settle_debts(balances)      # 3. who pays whom
    print(format_report(transfers))         # 4. show the result


if __name__ == "__main__":
    main()
