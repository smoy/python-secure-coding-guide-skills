def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError(f"Withdrawal amount must be positive, got {amount!r}")
    if amount > balance:
        raise ValueError(
            f"Withdrawal amount {amount!r} exceeds balance {balance!r}"
        )
    return balance - amount
