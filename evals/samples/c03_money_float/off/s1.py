def invoice_total(unit_price, quantity, tax_rate):
    subtotal = unit_price * quantity
    tax = subtotal * tax_rate
    total = subtotal + tax
    return total
