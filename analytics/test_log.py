import gspread
from datetime import datetime
import os

SERVICE_ACCOUNT_JSON = os.environ["SERVICE_ACCOUNT_JSON"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]

gc = gspread.service_account(filename=SERVICE_ACCOUNT_JSON)
sh = gc.open_by_key(SPREADSHEET_ID)
ws = sh.sheet1

# Append test row
ws.append_row([
    datetime.utcnow().isoformat(),
    "CI_JOB",
    "github_actions",
    "Workflow",
    "AGENCY-DEMO",
    "TEST_LOG",
    "SCRIPT",
    "12345",
    "Test content",
    "NONE",
    "None",
    "v0.1-pilot",
])
print("✅ Log row appended successfully")
