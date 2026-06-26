import statistics


def average(numbers):
    """Return the arithmetic mean of a list of numbers.

    Args:
        numbers: A non-empty sequence of numeric values.

    Returns:
        The arithmetic mean. Returns a float for int inputs,
        Decimal for Decimal inputs (delegates type to statistics.mean).

    Raises:
        statistics.StatisticsError: If numbers is empty.
        TypeError: If numbers contains non-numeric values.
    """
    return statistics.mean(numbers)
