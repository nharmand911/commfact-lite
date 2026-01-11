"""
COMMFACT Tier-0 Rule Definitions (HARD LAW)
------------------------------------------
Tier-0 rules represent non-negotiable legal / ethical prohibitions.

Characteristics:
- Severity is FIXED (HIGH)
- Cannot be downgraded by policy or UI
- Violation = governance red flag

This module defines non-negotiable validation constraints.
Tier-0 rules:
- Are evaluated before any Tier-1 rules
- Do not use scoring or severity
- Cannot be overridden or configured via CSV
- Result in immediate STOP when violated
"""

from rules.rule_base import Rule
import re


# =========================================================
# ABSOLUTE CLAIM RULE (TIER-0)
# =========================================================

class AbsoluteClaimRule(Rule):
    def __init__(self):
        super().__init__(
            rule_id="LGL-ABS-01",
            category="Legal & Compliance",
            severity="HIGH",
            description="Deteksi klaim absolut tanpa pengecualian dalam konten",
            rationale=(
                "Klaim absolut dilarang oleh BPOM, EPI, dan Kominfo "
                "karena berpotensi menyesatkan dan menurunkan kapasitas kritis audiens"
            )
        )

    def detect(self, text: str) -> bool:
        if not text:
            return False

        text_lower = text.lower()

        # Keyword absolut eksplisit
        keywords = [
            "100%",
            "100 persen",
            "seratus persen",
            "tanpa risiko",
            "tanpa resiko",
            "tanpa cacat",
            "tanpa kegagalan",
            "selalu berhasil",
            "selalu sukses",
            "mutlak",
            "pasti aman",
            "sempurna",
            "tak mungkin gagal"
        ]

        if any(k in text_lower for k in keywords):
            return True

        # Pola absolut implisit (basic regex, deterministic)
        patterns = [
            r"tanpa\s+(sama sekali|sedikitpun|sedikit pun)",
            r"tidak ada\s+(risiko|resiko|bahaya|kegagalan)",
            r"jamin\s+(aman|aman\s*100%|aman\s*seratus\s*persen)"
        ]

        for pattern in patterns:
            if re.search(pattern, text_lower):
                return True

        return False


# =========================================================
# GUARANTEE CLAIM RULE (TIER-0)
# =========================================================

class GuaranteeClaimRule(Rule):
    def __init__(self):
        super().__init__(
            rule_id="LGL-GUA-01",
            category="Legal & Compliance",
            severity="HIGH",
            description="Deteksi klaim yang menjanjikan hasil pasti atau kepastian outcome",
            rationale=(
                "Klaim jaminan dilarang oleh BPOM, Kemenkes, dan UU Perlindungan Konsumen; "
                "merupakan red flag tertinggi dan sering menjadi sumber risiko hukum"
            )
        )

    def detect(self, text: str) -> bool:
        if not text:
            return False

        text_lower = text.lower()

        # Keyword jaminan eksplisit
        keywords = [
            "dijamin",
            "jaminan",
            "pasti sembuh",
            "pasti berhasil",
            "pasti sukses",
            "100% efektif",
            "seratus persen efektif",
            "tanpa efek samping",
            "jamin kesembuhan",
            "jamin keberhasilan",
            "jamin kepuasan",
            "jaminan uang kembali",
            "money back guarantee",
            "kepastian hasil",
            "hasil terjamin",
            "jamin aman"
        ]

        if any(k in text_lower for k in keywords):
            return True

        # Klaim jaminan medis spesifik
        medical_guarantees = [
            "pasti sehat",
            "jamin pulih",
            "sembuh total",
            "sembuh 100%"
        ]

        if any(m in text_lower for m in medical_guarantees):
            return True

        return False
