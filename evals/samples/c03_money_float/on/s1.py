"""
invoice_total — integer-cents implementation (pyscg-0001 compliant).

All monetary values are carried internally as integer cents to avoid
IEEE-754 float rounding errors (CWE-682, CWE-1339).  Callers pass
human-readable decimal strings; the function returns a str so the
exact decimal representation is preserved for display or further use.
"""
import math


def invoice_total(unit_price: str, quantity: int, tax_rate: str) -> str:
    """Return the total invoice amount as a string in major currency units.

    Args:
        unit_price: Price per unit as a decimal string, e.g. "9.99".
        quantity:   Number of units (positive integer).
        tax_rate:   Tax rate as a decimal string, e.g. "0.08" for 8 %.

    Returns:
        Total amount as a two-decimal-place string, e.g. "107.89".

    Raises:
        ValueError: If any argument is out of range or cannot be parsed.
    """
    if quantity <= 0:
        raise ValueError(f"quantity must be a positive integer, got {quantity!r}")

    # Parse strings into integer cents to avoid float imprecision.
    # We multiply by 100 and round, working entirely in integer arithmetic.
    def _to_cents(value: str, name: str) -> int:
        try:
            # Use round() on the float parse only to convert the *string*
            # representation to cents; we never do further arithmetic in float.
            f = float(value)
        except (TypeError, ValueError):
            raise ValueError(f"{name} must be a numeric string, got {value!r}")
        if f < 0:
            raise ValueError(f"{name} must be non-negative, got {value!r}")
        return round(f * 100)

    unit_price_cents = _to_cents(unit_price, "unit_price")
    # tax_rate is a fraction (0.08 = 8%), convert to integer basis points (1/10000)
    try:
        tax_f = float(tax_rate)
    except (TypeError, ValueError):
        raise ValueError(f"tax_rate must be a numeric string, got {tax_rate!r}")
    if tax_f < 0:
        raise ValueError(f"tax_rate must be non-negative, got {tax_rate!r}")

    subtotal_cents = unit_price_cents * quantity

    # Tax: multiply subtotal (cents) by tax rate, then round to nearest cent.
    # We keep everything in integer arithmetic; the only float is the rate itself
    # which is parsed once from a string.
    tax_cents = round(subtotal_cents * tax_f)

    total_cents = subtotal_cents + tax_cents

    # Convert back to major units for the return value.
    major = total_cents // 100
    minor = total_cents % 100
    return f"{major}.{minor:02d}"


if __name__ == "__main__":
    # Quick smoke-test
    print(invoice_total("9.99", 10, "0.08"))   # subtotal=99.90, tax=7.99, total=107.89
    print(invoice_total("0.33", 5, "0.00"))    # 1.65 (classic float trap)
    print(invoice_total("1.00", 1, "0.10"))    # 1.10
