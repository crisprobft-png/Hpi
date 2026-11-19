"""Expense Splitter - Segment 0 & Segment 2: types, constants, and compute_balances."""

# An expense is (payer, amount in EUR, people who share it).
Expense = tuple[str, float, list[str]]
# A transfer is (debtor, creditor, amount in EUR).
Transfer = tuple[str, str, float]

# Balances can be off by a few cents because of rounding.
TOLERANCE = 0.05
# Amounts below half a cent are treated as zero.
EPSILON = 0.005


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