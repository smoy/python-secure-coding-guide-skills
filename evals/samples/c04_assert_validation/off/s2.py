def withdraw(balance, amount):
    assert amount > 0
    assert amount <= balance
    return balance - amount
