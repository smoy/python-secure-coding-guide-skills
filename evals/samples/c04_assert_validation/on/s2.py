from decimal import Decimal


def withdraw(balance, amount):
    if not isinstance(amount, (int, float, Decimal)):
        raise TypeError(f"amount must be numeric, got {type(amount).__name__!r}")
    if not isinstance(balance, (int, float, Decimal)):
        raise TypeError(f"balance must be numeric, got {type(balance).__name__!r}")
    if amount <= 0:
        raise ValueError("amount must be greater than zero")
    if amount > balance:
        raise ValueError("amount must not exceed balance")
    return balance - amount
