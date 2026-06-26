def reverse_words(sentence: str) -> str:
    """Return sentence with the order of its words reversed.

    Args:
        sentence: A string whose words are to be reversed.

    Returns:
        A new string with the words in reverse order.

    Raises:
        TypeError: If sentence is not a str (pyscg-0034, CWE-476).
    """
    # pyscg-0034 (CWE-476): guard against None and wrong types before use.
    # pyscg-0037 (CWE-617): use an explicit raise, not assert, for real checks.
    if not isinstance(sentence, str):
        raise TypeError(
            f"reverse_words() expects a str, got {type(sentence).__name__!r}"
        )

    words = sentence.split()
    words.reverse()
    return " ".join(words)
