def average(numbers):
    """Return the arithmetic mean of a list of numbers.

    Args:
        numbers: A non-empty sequence of numeric values.

    Returns:
        The arithmetic mean as a float.

    Raises:
        TypeError: If numbers is not iterable or contains non-numeric values.
        ValueError: If numbers is empty.
    """
    if not hasattr(numbers, "__iter__"):
        raise TypeError("numbers must be iterable")

    total = 0
    count = 0
    for value in numbers:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"all elements must be numeric, got {type(value).__name__!r}"
            )
        total += value
        count += 1

    if count == 0:
        raise ValueError("average() requires at least one element")

    return total / count
