"""Expense Splitter - Segment 3: settle_debts."""

Transfer = tuple[str, str, float]

# Balances can be off by a few cents because of rounding.
TOLERANCE = 0.05
# Amounts below half a cent are treated as zero.
EPSILON = 0.005


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