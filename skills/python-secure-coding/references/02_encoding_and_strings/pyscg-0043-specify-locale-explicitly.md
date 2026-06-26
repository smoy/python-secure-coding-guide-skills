# pyscg-0043: Specify Locale Explicitly

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-707 (pillar), CWE-175 (Improper Handling of Mixed Encoding).

## Rule

Always **set the locale explicitly** before performing locale-dependent operations (date formatting, number parsing, string comparison). Never rely on the ambient system locale, which may differ between developer and production environments.

## Why

Python's `str` methods (`upper()`, `lower()`) follow Unicode rules, not locale rules, so they can produce wrong results for locale-sensitive characters (e.g. Turkish dotted-i, German ß). Functions like `strftime("%B")` return locale-specific strings that cannot be compared across different locales without explicit control. Number parsing via `locale.atof()` interprets separators differently per locale (`.` vs `,`), causing silent data corruption or security bypasses if the locale is not fixed.

## Non-compliant

```python
import datetime
import locale

dt = datetime.datetime(2022, 3, 9, 12, 55, 35, 000000)


def get_date(date):
    # Returns locale-dependent month name — breaks cross-locale comparison
    return date.strftime("%Y"), date.strftime("%B"), date.strftime("%d")


CURRENT_LOCALE = 'en_IE.utf8'
OTHER_LOCALE = 'uk_UA.utf8'

locale.setlocale(locale.LC_ALL, CURRENT_LOCALE)
curryear, currmonth, currdate = get_date(dt)  # "March"

locale.setlocale(locale.LC_ALL, OTHER_LOCALE)
otheryear, othermonth, otherdate = get_date(dt)  # "березень"

if currmonth == othermonth:
    print("Locale-dependent months are equal")
else:
    print("Locale-dependent months are not equal")  # always prints this
```

## Compliant

```python
import datetime
import locale

dt = datetime.datetime(2022, 3, 9, 12, 55, 35, 000000)

CURRENT_LOCALE = 'en_IE.utf8'
OTHER_LOCALE = 'uk_UA.utf8'

locale.setlocale(locale.LC_ALL, CURRENT_LOCALE)
currmonth = dt.month          # locale-independent integer

locale.setlocale(locale.LC_ALL, OTHER_LOCALE)
othermonth = dt.month         # locale-independent integer

if currmonth == othermonth:
    print("Locale-independent months are equal")  # correctly prints this
```

> Cross-ref: pyscg-0044 (canonicalize before validating), pyscg-0045 (consistent encoding). When using `setlocale()`, do not call it inside libraries or multiple times in multi-threaded programs.
