def invoice_total(unit_price, quantity, tax_rate):
    return (unit_price * quantity) * (1 + tax_rate)
