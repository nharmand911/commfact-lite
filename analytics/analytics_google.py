import os
import json
import gspread
import base64
from datetime import datetime
from typing import Optional
from google.oauth2.service_account import Credentials

# =========================================
# CONFIGURATION
# =========================================
SERVICE_ACCOUNT_JSON_CONTENT = os.getenv("SERVICE_ACCOUNT_JSON")
SERVICE_ACCOUNT_JSON_B64 = os.getenv("SERVICE_ACCOUNT_JSON_B64")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = "AnalyticsLog"

# cache
_gc = None
_sh = None
_ws = None

HEADERS = [
    "timestamp",
    "session_id",
    "username",
    "role",
    "agency_code",
    "event_type",
    "object_type",
    "object_id",
    "content_excerpt",
    "severity",
    "triggered_rules",
    "decision",
    "app_version",
]

# =========================================
# INIT GOOGLE SHEET
# =========================================
def _get_sheet():
    global _gc, _sh, _ws

    if _ws is not None:
        return _ws

    if not SPREADSHEET_ID:
        print("[Analytics] SPREADSHEET_ID not set")
        return None

    # ---- Load service account ----
    try:
        if SERVICE_ACCOUNT_JSON_B64:
            print("[Analytics] Using SERVICE_ACCOUNT_JSON_B64")
            decoded = base64.b64decode(SERVICE_ACCOUNT_JSON_B64).decode("utf-8")
            creds_dict = json.loads(decoded)
        elif SERVICE_ACCOUNT_JSON_CONTENT:
            print("[Analytics] Using SERVICE_ACCOUNT_JSON")
            creds_dict = json.loads(SERVICE_ACCOUNT_JSON_CONTENT)
        else:
            print("[Analytics] No service account secret found")
            return None
    except Exception as e:
        print(f"[Analytics] Invalid service account secret: {e}")
        return None

    try:
        # ---- Authorize ----
        if _gc is None:
            creds = Credentials.from_service_account_info(
                creds_dict,
                scopes=[
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive",
                ],
            )
            _gc = gspread.authorize(creds)

        # ---- Open spreadsheet ----
        if _sh is None:
            print(f"[Analytics] Opening spreadsheet ID: {SPREADSHEET_ID}")
            _sh = _gc.open_by_key(SPREADSHEET_ID)

        # ---- Worksheet ----
        if _ws is None:
            try:
                _ws = _sh.worksheet(SHEET_NAME)
            except gspread.WorksheetNotFound:
                print("[Analytics] Creating worksheet:", SHEET_NAME)
                _ws = _sh.add_worksheet(
                    title=SHEET_NAME,
                    rows="1000",
                    cols=str(len(HEADERS)),
                )
                _ws.append_row(HEADERS, value_input_option="RAW")

        print("[Analytics] Worksheet ready:", SHEET_NAME)
        return _ws

    except Exception as e:
        print(f"[Analytics] Failed to initialize Google Sheet: {e}")
        return None


# =========================================
# LOG EVENT (CORE)
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
    decision: Optional[str] = None,
):
    print("[Analytics] log_event_google called:", event_type, object_type)

    try:
        import streamlit as st
        session = st.session_state
    except Exception:
        session = {}

    print("[Analytics] session:", dict(session))

    if not session.get("username") or not session.get("agency_code"):
        print("[Analytics] missing username or agency_code")
        return False

    ws = _get_sheet()
    if ws is None:
        print("[Analytics] worksheet not available")
        return False

    record = [
        datetime.utcnow().isoformat(),
        session.get("session_id", ""),
        session.get("username", ""),
        session.get("role", ""),
        session.get("agency_code", ""),
        event_type,
        object_type,
        object_id or "",
        content_excerpt or "",
        severity or "",
        triggered_rules or "",
        decision or "",
        app_version,
    ]

    print("[Analytics] appending row:", record)
    ws.append_row(record, value_input_option="RAW")
    print("[Analytics] append success")

    return True


# =========================================
# HIGH-LEVEL EVENTS (WRAPPERS)
# =========================================
def log_login():
    """
    Dipanggil saat user login sukses
    """
    return log_event_google(
        event_type="LOGIN",
        object_type="SESSION",
    )


def log_logout():
    """
    Dipanggil saat user logout
    """
    return log_event_google(
        event_type="LOGOUT",
        object_type="SESSION",
    )
