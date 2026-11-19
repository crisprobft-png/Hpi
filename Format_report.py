"""Expense Splitter - Segment 4: format_report and main."""

Expense = tuple[str, float, list[str]]
Transfer = tuple[str, str, float]


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