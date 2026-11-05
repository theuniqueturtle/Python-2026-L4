"""Query module: run user-written conditions on a pandas DataFrame.

Examples of conditions (join several with 'and'):
    name = "Mr. Volunteers"
    name contains "an" and dob > 2000
Operators: =  !=  >  <  >=  <=  contains      (text comparisons ignore case)
"""
import re

import pandas as pd

OPERATORS = ("!=", ">=", "<=", "==", "=", ">", "<", "contains")

CONDITION = re.compile(
    r"""\s*(\w+)\s*(!=|>=|<=|==|=|>|<|contains)\s*("[^"]*"|'[^']*'|\S+)\s*(?:\band\b|$)""",
    re.IGNORECASE,
)


def parse_conditions(text):
    """Turn 'name = "An" and dob > 2000' into [(field, op, value), ...]."""
    text = text.strip()
    if not text:
        raise ValueError("Please enter a condition.")
    conditions, pos = [], 0
    while pos < len(text):
        m = CONDITION.match(text, pos)
        if m is None:
            raise ValueError(f"Cannot understand: {text[pos:].strip()!r}")
        field, op, value = m.group(1), m.group(2).lower(), m.group(3)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        conditions.append((field, op, value))
        pos = m.end()
    return conditions


def run_query(df, conditions):
    """Return the rows of the DataFrame that satisfy ALL conditions."""
    columns = {c.lower(): c for c in df.columns}
    mask = pd.Series(True, index=df.index)
    for field, op, value in conditions:
        if field.lower() not in columns:
            raise ValueError(f"Unknown field {field!r}. Fields: {', '.join(df.columns)}")
        col = df[columns[field.lower()]].astype(str)
        low, value_low = col.str.lower(), value.lower()
        if op in ("=", "=="):
            mask &= low == value_low
        elif op == "!=":
            mask &= low != value_low
        elif op == "contains":
            mask &= low.str.contains(value_low, regex=False)
        elif op == ">":
            mask &= col > value
        elif op == "<":
            mask &= col < value
        elif op == ">=":
            mask &= col >= value
        elif op == "<=":
            mask &= col <= value
    return df[mask]
