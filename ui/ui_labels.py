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
        "AbsoluteClaimRule": "Klaim absolut tanpa batasan",
        "SuperiorityClaimRule": "Klaim superioritas",
        "GuaranteeClaimRule": "Pernyataan jaminan hasil",
        "HealthBenefitClaimRule": "Klaim manfaat kesehatan tanpa bukti",
        "RiskFramingRule": "Framing risiko berpotensi menyesatkan",
        "NeutralInformationRule": "Informasi bersifat netral",
        "AmbiguousMarketingRule": "Klaim marketing ambigu",
        "BeforeAfterImprovementRule": "Perbandingan sebelum-sesudah tanpa data jelas"
    }

    # =========================
    # ACTION HINTS (STATIC)
    # =========================
#    ACTION_HINTS = {
#        "FLAG": (
#            "Pertimbangkan meninjau ulang wording klaim, "
#            "menambahkan konteks, atau memperjelas batasan."
#        ),
#        "STOP": (
#            "Konten sebaiknya direvisi sebelum dipublikasikan. "
#            "Hindari klaim absolut, jaminan hasil, atau superioritas tanpa dasar."
#        )
#    }

    # =========================
    # VALIDATION / SUMMARY DISCLAIMERS
    # =========================
    VALIDATION_DISCLAIMER = (
        "Hasil ini merupakan sinyal validasi otomatis sistem COMMFACT "
        "dan bukan merupakan keputusan, persetujuan, atau penolakan konten."
    )

    REVIEW_SUMMARY_DISCLAIMER = (
        "Ringkasan ini ditujukan untuk mendukung proses review manusia "
        "selama fase pilot dan bukan merupakan artefak keputusan sistem."
    )

    # =========================
    # DECISION SUMMARY DISCLAIMER
    # =========================
#    SUMMARY_DISCLAIMER = (
#        "Ringkasan ini bersifat informatif untuk membantu pemahaman pengguna. "
#        "Audit log teknis tetap menjadi sumber akuntabilitas utama."
#    )
    

    # =========================
    # CREATOR PAGE
    # =========================
    CONTENT_SUBMISSION_TITLE = "Content Submission"
    CONTENT_SUBMISSION_CAPTION = "Submit content for automated risk validation prior to review"
    CONTENT_PLACEHOLDER = "Enter caption, press release, or public statement..."

    VALIDATION_RESULT_TITLE = "Validation Signal (System Advisory)"
    NO_RULE_VIOLATION = "✅ Tidak terdeteksi indikasi pelanggaran aturan"
    TRIGGERED_RULES_LABEL = "Indikasi aturan terdeteksi:"
    SUBMIT_SUCCESS_MSG = "✅ Konten berhasil dikirim ke antrian review"
    SUBMIT_BUTTON = "📤 Submit for Human Review"

    # =========================
    # REVIEWER PAGE
    # =========================
    REVIEW_TITLE = "Content Review"
    REVIEW_CAPTION = "Human governance review panel"
    CONTENT_UNDER_REVIEW = "📄 Content Under Review"

    REVIEWER_DECISION_TITLE = "📝 Reviewer Decision (Human Judgment)"
    DECISION_SELECT_LABEL = "Reviewer Decision"
    DECISION_REASON_PLACEHOLDER = "Jelaskan pertimbangan dan justifikasi keputusan..."
    DECISION_REASON_ERROR = "🚨 Alasan keputusan wajib diisi."
    DECISION_SUBMIT_SUCCESS = "✅ Keputusan reviewer tercatat dan konten dikunci"

    # =========================
    # AUDIT LOG
    # =========================
    AUDIT_LOG_TITLE = "📜 Audit Log (Read-Only)"
    AUDIT_LOG_CAPTION = "Permanent system record for governance accountability"
    AUDIT_LOG_EMPTY = "Audit log is empty."
