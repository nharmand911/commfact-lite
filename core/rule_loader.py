"""
COMMFACT Rule Loader
-------------------
Loads and validates Tier 1 CSV rules.

Responsibilities:
- Read rules.csv
- Validate required schema
- Normalize rule values
- Fail fast on malformed rules

NON-RESPONSIBILITIES:
- Rule evaluation
- Logging / audit
- Business logic
"""

import csv
from typing import List, Dict


# =========================================================
# CONFIG
# =========================================================

REQUIRED_FIELDS = {
    "rule_id",
    "category",
    "severity",
    "score",
    "pattern",
    "message"
}

ALLOWED_SEVERITIES = {"LOW", "MEDIUM", "HIGH"}


# =========================================================
# LOADER
# =========================================================

def load_rules(csv_path: str) -> List[Dict]:
    """
    Load and validate rules from CSV file.

    Args:
        csv_path (str): Path to rules.csv

    Returns:
        list[dict]: Validated rule dictionaries

    Raises:
        ValueError: if rule schema is invalid
    """

    rules: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        # Validate header
        header_fields = set(reader.fieldnames or [])
        missing_fields = REQUIRED_FIELDS - header_fields
        if missing_fields:
            raise ValueError(
                f"CSV missing required fields: {sorted(missing_fields)}"
            )

        for row_number, row in enumerate(reader, start=2):
            rule = _validate_and_normalize_row(row, row_number)
            rules.append(rule)

    if not rules:
        raise ValueError("No valid rules loaded from CSV")

    return rules


# =========================================================
# ROW VALIDATION
# =========================================================

def _validate_and_normalize_row(row: Dict, row_number: int) -> Dict:
    """
    Validate and normalize a single CSV row.

    Raises:
        ValueError with precise location on failure
    """

    # Trim whitespace
    row = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}

    # Required field presence & non-empty
    for field in REQUIRED_FIELDS:
        if not row.get(field):
            raise ValueError(
                f"Row {row_number}: field '{field}' is empty or missing"
            )

    # Score validation
    try:
        score = int(row["score"])
        if score < 0:
            raise ValueError
    except ValueError:
        raise ValueError(
            f"Row {row_number}: invalid score '{row['score']}'"
        )

    # Severity validation
    severity = row["severity"].upper()
    if severity not in ALLOWED_SEVERITIES:
        raise ValueError(
            f"Row {row_number}: invalid severity '{row['severity']}'"
        )

    # Pattern normalization (Tier 1 literal match)
    pattern = row["pattern"].lower()

    return {
        "rule_id": row["rule_id"],
        "category": row["category"],
        "severity": severity,
        "score": score,
        "pattern": pattern,
        "message": row["message"]
    }
