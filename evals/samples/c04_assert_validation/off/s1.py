def withdraw(balance, amount):
    assert amount > 0, "Amount must be positive"
    assert amount <= balance, "Amount must not exceed balance"
    return balance - amount
