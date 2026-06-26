"""
invoice_total — decimal.Decimal implementation (pyscg-0001 compliant).

Uses decimal.Decimal constructed from strings to avoid IEEE-754 float
rounding errors (CWE-682, CWE-1339).  ROUND_HALF_UP is applied at the
final step to match conventional financial rounding.
"""
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


def invoice_total(unit_price: str, quantity: int, tax_rate: str) -> Decimal:
    """Return the total invoice amount as a Decimal rounded to two places.

    Args:
        unit_price: Price per unit as a decimal string, e.g. "9.99".
        quantity:   Number of units (positive integer).
        tax_rate:   Tax rate as a decimal string, e.g. "0.08" for 8 %.

    Returns:
        Total amount as a Decimal quantized to two decimal places,
        e.g. Decimal("107.89").

    Raises:
        ValueError: If any argument is out of range or cannot be parsed.
    """
    if not isinstance(quantity, int) or quantity <= 0:
        raise ValueError(f"quantity must be a positive integer, got {quantity!r}")

    # Construct Decimal from strings — never from floats — to preserve precision.
    try:
        d_unit_price = Decimal(unit_price)
    except InvalidOperation:
        raise ValueError(f"unit_price must be a numeric string, got {unit_price!r}")

    try:
        d_tax_rate = Decimal(tax_rate)
    except InvalidOperation:
        raise ValueError(f"tax_rate must be a numeric string, got {tax_rate!r}")

    if d_unit_price < 0:
        raise ValueError(f"unit_price must be non-negative, got {unit_price!r}")
    if d_tax_rate < 0:
        raise ValueError(f"tax_rate must be non-negative, got {tax_rate!r}")

    subtotal = d_unit_price * quantity
    tax = subtotal * d_tax_rate
    total = subtotal + tax

    # Quantize to exactly two decimal places using conventional rounding.
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


if __name__ == "__main__":
    # Quick smoke-test
    print(invoice_total("9.99", 10, "0.08"))   # subtotal=99.90, tax=7.99, total=107.89
    print(invoice_total("0.33", 5, "0.00"))    # 1.65 (classic float trap)
    print(invoice_total("1.00", 1, "0.10"))    # 1.10
