"""
ui_labels.py
-----------------
UI-only label & hint mapping untuk Decision Summary View dan seluruh UI COMMFACT Lite.

⚠️ IMPORTANT GOVERNANCE NOTE
- File ini HANYA untuk lapisan presentasi (UX).
- Tidak mengandung logic keputusan, rule engine, atau audit.
- Aman untuk diubah tanpa memengaruhi akuntabilitas sistem.
"""

class UI:
    # =========================
    # APP TITLE & CAPTIONS
    # =========================
    APP_TITLE = "COMMFACT Lite"
    APP_SUBTITLE = "Communication Governance Validator"
    PILOT_WARNING = "⚠️ Pilot Version – Governance Simulation Only"

    # =========================
    # LOGIN PAGE
    # =========================
    LOGIN_TITLE = "Login"
    LOGIN_USERNAME = "Username"
    LOGIN_ROLE = "Role"
    ROLES = ["Creator", "Reviewer"]
    LOGIN_AGENCY = "Agency Code"
    LOGIN_AGENCY_HELP = "Digunakan untuk analitik dan audit per agency"
    LOGIN_BUTTON = "Login"
    LOGIN_SUCCESS = "Logged in as {username} ({role}) – {agency}"
    LOGIN_ERROR = "Invalid login credentials"

    # =========================
    # SIDEBAR
    # =========================
    SIDEBAR_SESSION = "👤 Session"
    SIDEBAR_USER = "{username} ({role})"
    SIDEBAR_AGENCY = "🏢 Agency: {agency}"
    LOGOUT_BUTTON = "Logout"
    INVALID_ROLE = "Invalid role in session"

    # =========================
    # STATUS ICONS & LABELS (Decision Summary)
    # =========================
    STATUS_ICONS = {
        "ALLOW": "✅",
        "FLAG": "⚠️",
        "STOP": "⛔"
    }

    STATUS_LABELS = {
        "ALLOW": "Diizinkan",
        "FLAG": "Perlu Review",
        "STOP": "Tidak Disarankan"
    }

    RISK_LABELS = {
        "LOW": "Rendah",
        "MEDIUM": "Sedang",
        "HIGH": "Tinggi"
    }

    # =========================
    # RULE → HUMAN-READABLE LABEL
    # =========================
    RULE_LABELS = {
        "AbsoluteClaimRule": "Mengandung klaim absolut tanpa batasan",
        "SuperiorityClaimRule": "Mengandung klaim superioritas",
        "GuaranteeClaimRule": "Menyatakan jaminan hasil",
        "HealthBenefitClaimRule": "Mengklaim manfaat kesehatan tanpa bukti",
        "RiskFramingRule": "Menyajikan risiko secara menyesatkan",
        "NeutralInformationRule": "Informasi netral",
        "AmbiguousMarketingRule": "Klaim marketing ambigu",
        "BeforeAfterImprovementRule": "Membandingkan sebelum-sesudah tanpa data jelas"
    }

    # =========================
    # ACTION HINTS (STATIC)
    # =========================
    ACTION_HINTS = {
        "FLAG": (
            "Pertimbangkan meninjau ulang wording klaim, "
            "menambahkan konteks, atau memperjelas batasan."
        ),
        "STOP": (
            "Konten sebaiknya direvisi sebelum dipublikasikan. "
            "Hindari klaim absolut, jaminan hasil, atau superioritas tanpa dasar."
        )
    }

    # =========================
    # DECISION SUMMARY DISCLAIMER
    # =========================
    SUMMARY_DISCLAIMER = (
        "Ringkasan ini bersifat informatif untuk membantu pemahaman pengguna. "
        "Audit log teknis tetap menjadi sumber akuntabilitas utama."
    )

    # =========================
    # CREATOR PAGE
    # =========================
    CONTENT_SUBMISSION_TITLE = "Content Submission"
    CONTENT_SUBMISSION_CAPTION = "Submit content for pre-publication risk validation"
    CONTENT_PLACEHOLDER = "Enter caption, press release, or public statement..."
    VALIDATION_RESULT_TITLE = "Validation Result"
    NO_RULE_VIOLATION = "✅ No rule violations detected"
    TRIGGERED_RULES_LABEL = "Triggered Rules:"
    SUBMIT_SUCCESS_MSG = "✅ Content successfully submitted to reviewer queue"
    SUBMIT_BUTTON = "📤 Submit for Review"

    # =========================
    # REVIEWER PAGE
    # =========================
    REVIEW_TITLE = "Review & Decision"
    REVIEW_CAPTION = "Governance decision panel"
    CONTENT_UNDER_REVIEW = "📄 Content Under Review"
    REVIEWER_DECISION_TITLE = "📝 Reviewer Decision"
    DECISION_SELECT_LABEL = "Decision"
    DECISION_REASON_PLACEHOLDER = "Explain the decision and justification..."
    DECISION_REASON_ERROR = "🚨 Decision reason is mandatory."
    DECISION_SUBMIT_SUCCESS = "✅ Decision recorded and content locked"

    # =========================
    # AUDIT LOG
    # =========================
    AUDIT_LOG_TITLE = "📜 Audit Log (Read-Only)"
    AUDIT_LOG_CAPTION = "Permanent governance record"
    AUDIT_LOG_EMPTY = "Audit log is empty."
