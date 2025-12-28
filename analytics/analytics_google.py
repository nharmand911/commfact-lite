# analytics/analytics_google.py

import gspread
from datetime import datetime
from typing import Optional
import streamlit as st
import os

# =========================================
# CONFIGURATION
# =========================================
# Gunakan SERVICE_ACCOUNT_JSON dari environment variable jika ada (untuk CI/GitHub Actions)
SERVICE_ACCOUNT_JSON = os.getenv(
    "SERVICE_ACCOUNT_JSON_LOCAL",  # untuk lokal bisa pakai path lokal
    r"C:\Users\nharm\commfact-lite\analytics\service_account.json"
)

SPREADSHEET_ID = os.getenv(
    "SPREADSHEET_ID",
    "111UW8wT-g8F_-1J3ptIzNtI01UBw8vm3XIzMvuhtV8k"
)
SHEET_NAME = "AnalyticsLog"

# Cache client supaya tidak autentikasi setiap kali log
_gc = None
_sh = None
_ws = None

# =========================================
# INIT GOOGLE SHEET
# =========================================
def _get_sheet():
    """
    Autentikasi ke Google Sheet via Service Account dan buka sheet.
    Membuat sheet baru jika SHEET_NAME belum ada, dan menambahkan header lengkap.
    """
    global _gc, _sh, _ws

    if _ws:
        return _ws

    if not _gc:
        _gc = gspread.service_account(filename=SERVICE_ACCOUNT_JSON)
    if not _sh:
        _sh = _gc.open_by_key(SPREADSHEET_ID)

    try:
        _ws = _sh.worksheet(SHEET_NAME)
    except gspread.WorksheetNotFound:
        # Buat sheet baru jika belum ada
        _ws = _sh.add_worksheet(title=SHEET_NAME, rows="1000", cols="25")
        # Tambahkan header lengkap, termasuk 'decision'
        _ws.append_row([
            "timestamp", "session_id", "username", "role", "agency_code",
            "event_type", "object_type", "object_id",
            "content_excerpt", "severity", "triggered_rules",
            "decision", "app_version"
        ])
    return _ws

# =========================================
# LOG EVENT
# =========================================
def log_event_google(
    *,
    event_type: str,
    object_type: str,
    object_id: Optional[str] = None,
    app_version: str = "v0.1-pilot",
    content_excerpt: Optional[str] = None,
    severity: Optional[str] = None,
    triggered_rules: Optional[str] = None,
    decision: Optional[str] = None
):
    """
    Log event ke Google Sheet.
    Otomatis membaca username, role, agency_code, session_id dari st.session_state.
    Selalu menulis 13 kolom.
    """
    if "username" not in st.session_state or "agency_code" not in st.session_state:
        st.warning("Analytics log skipped: user not logged in yet")
        return False

    worksheet = _get_sheet()

    record = [
        datetime.utcnow().isoformat(),
        st.session_state.get("session_id", ""),
        st.session_state.get("username"),
        st.session_state.get("role", ""),
        st.session_state.get("agency_code"),
        event_type,
        object_type,
        object_id or "",
        content_excerpt or "",
        severity or "",
        triggered_rules or "",
        decision or "",
        app_version
    ]

    try:
        worksheet.append_row(record)
        return True
    except Exception as e:
        st.error(f"Failed to log event: {e}")
        return False

# =========================================
# HELPER FUNCTIONS UNTUK TIPE EVENT
# =========================================
def log_login():
    log_event_google(event_type="LOGIN", object_type="SESSION")

def log_logout():
    log_event_google(event_type="LOGOUT", object_type="SESSION")

def log_submit_content(
    content_id: str,
    content_excerpt: str = "",
    severity: str = "",
    triggered_rules: str = ""
):
    log_event_google(
        event_type="SUBMIT_CONTENT",
        object_type="CONTENT",
        object_id=content_id,
        content_excerpt=content_excerpt,
        severity=severity,
        triggered_rules=triggered_rules
    )

def log_submit_decision(
    content_id: str,
    decision: Optional[str] = None,
    content_excerpt: Optional[str] = None,
    severity: Optional[str] = None,
    triggered_rules: Optional[str] = None
):
    log_event_google(
        event_type="SUBMIT_DECISION",
        object_type="DECISION",
        object_id=content_id,
        decision=decision,
        content_excerpt=content_excerpt,
        severity=severity,
        triggered_rules=triggered_rules
    )
