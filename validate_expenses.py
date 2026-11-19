"""Expense Splitter - Segment 1: validate_expenses."""

Expense = tuple[str, float, list[str]]


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