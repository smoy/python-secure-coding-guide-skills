# pyscg-0010: Prevent SQL Injection

> Adapted from the OpenSSF Secure Coding Guide for Python (CC-BY-4.0 / MIT).
> CWE-707 (pillar), CWE-89 (Improper Neutralization of Special Elements used in an SQL Command).

*Overlaps the security-guidance plugin (the reactive/detective layer); this is the proactive Python-idiom complement.*

## Rule

Always use **parameterized queries** (`cursor.execute(sql, params_tuple)`) to separate SQL logic from data. Never build SQL strings by string concatenation or f-string formatting, and never use `executescript()` with user-supplied data.

## Why

Concatenating user data into an SQL string lets an attacker terminate the current statement and inject arbitrary SQL (e.g., `'); DROP TABLE students;--`). `executescript()` allows multi-statement execution and is intended for back-end initialization only. Parameterized queries pass values to the database driver separately, so special characters are never interpreted as SQL syntax. SQL injection consistently ranks in CWE Top 25 and OWASP Top 10.

## Non-compliant

```python
import sqlite3

class Records:
    def __init__(self):
        self.connection = sqlite3.connect("school.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Students(student TEXT)")
        self.connection.commit()

    def add_record(self, name: str = ""):
        add_values = "INSERT INTO Students(student) VALUES('{name}');"
        add_values_query = add_values.format(name=name)   # attacker-controlled
        self.cursor.executescript(add_values_query)        # multi-statement, injectable
        self.connection.commit()

records = Records()
records.add_record("Robert'); DROP TABLE students;--")    # drops the table
```

## Compliant

```python
import sqlite3

class Records:
    def __init__(self):
        self.connection = sqlite3.connect("school.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Students(student TEXT)")
        self.connection.commit()

    def add_record(self, name: str):
        data_tuple = (name,)
        add_values = "INSERT INTO Students VALUES (?)"    # placeholder, not f-string
        self.cursor.execute(add_values, data_tuple)       # driver handles escaping
        self.connection.commit()

    def get_record(self, name: str):
        data_tuple = (name,)
        get_values = "SELECT * FROM Students WHERE student = ?"
        self.cursor.execute(get_values, data_tuple)
        return self.cursor.fetchall()
```

The `?` placeholder causes the driver to transmit the value out-of-band; `'); DROP TABLE students;--` is stored as a literal string, not executed as SQL.
