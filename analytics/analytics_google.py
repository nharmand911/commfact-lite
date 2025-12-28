import os
import json
import gspread
from datetime import datetime
from typing import Optional
from google.oauth2.service_account import Credentials

# =========================================
# CONFIGURATION
# =========================================
SERVICE_ACCOUNT_JSON_CONTENT = os.getenv("SERVICE_ACCOUNT_JSON")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")  # WAJIB via secret
SHEET_NAME = "AnalyticsLog"

#if not SPREADSHEET_ID:
#    raise RuntimeError("SPREADSHEET_ID environment variable is not set")

# cache client
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
        # logging non-fatal
        print("[Analytics] SPREADSHEET_ID not set, analytics disabled")
        return None


    try:
        if SERVICE_ACCOUNT_JSON_B64:
            decoded = base64.b64decode(SERVICE_ACCOUNT_JSON_B64).decode("utf-8")
            creds_dict = json.loads(decoded)
        elif SERVICE_ACCOUNT_JSON_CONTENT:
            creds_dict = json.loads(SERVICE_ACCOUNT_JSON_CONTENT)
        else:
            print("[Analytics] No service account secret found, analytics disabled")
            return None
    except Exception as e:
        print(f"[Analytics] Invalid service account secret: {e}")
        return None

    try:
    #if not SERVICE_ACCOUNT_JSON_CONTENT:
    #    raise RuntimeError("SERVICE_ACCOUNT_JSON environment variable is not set")

    # ---- Authorize ----
        if _gc is None:
    #    creds_dict = json.loads(SERVICE_ACCOUNT_JSON_CONTENT)
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
            _sh = _gc.open_by_key(SPREADSHEET_ID)

    # ---- Get / create worksheet ----
        if _sh is None:
            try:
                _ws = _sh.worksheet(SHEET_NAME)
            except gspread.WorksheetNotFound:
                _ws = _sh.add_worksheet(
                    title=SHEET_NAME,
                    rows="1000",
                    cols=str(len(HEADERS)),
                )
                _ws.append_row(HEADERS, value_input_option="RAW")
            
        return _ws


    except Exception as e:
        print(f"[Analytics] Failed to initialize Google Sheet: {e}")
        return None
    
    # ---- Ensure header exists ----
    #first_row = _ws.row_values(1)
    #if first_row != HEADERS:
    #    _ws.insert_row(HEADERS, index=1)

    #return _ws


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
    decision: Optional[str] = None,
):
    """
    Log event ke Google Sheet.
    Mengambil konteks user dari st.session_state jika tersedia.
    """

    # lazy import agar analytics tidak hard-depend ke streamlit
    try:
        import streamlit as st
        session = st.session_state
    except Exception:
        session = {}

    if not session.get("username") or not session.get("agency_code"):
        return False

    ws = _get_sheet()
    if ws is None:
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

    ws.append_row(record, value_input_option="RAW")
    return True


# =========================================
# HELPER FUNCTIONS
# =========================================
def log_login():
    return log_event_google(event_type="LOGIN", object_type="SESSION")


def log_logout():
    return log_event_google(event_type="LOGOUT", object_type="SESSION")


def log_submit_content(
    content_id: str,
    content_excerpt: str = "",
    severity: str = "",
    triggered_rules: str = "",
):
    return log_event_google(
        event_type="SUBMIT_CONTENT",
        object_type="CONTENT",
        object_id=content_id,
        content_excerpt=content_excerpt,
        severity=severity,
        triggered_rules=triggered_rules,
    )


def log_submit_decision(
    content_id: str,
    decision: Optional[str] = None,
    content_excerpt: Optional[str] = None,
    severity: Optional[str] = None,
    triggered_rules: Optional[str] = None,
):
    return log_event_google(
        event_type="SUBMIT_DECISION",
        object_type="DECISION",
        object_id=content_id,
        decision=decision,
        content_excerpt=content_excerpt,
        severity=severity,
        triggered_rules=triggered_rules,
    )
