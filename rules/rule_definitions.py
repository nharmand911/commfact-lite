from rules.rule_base import Rule

class AbsoluteClaimRule(Rule):
    def __init__(self):
        super().__init__(
            rule_id="LGL-ABS-01",  # Diperbarui sesuai mapping
            category="Legal & Compliance",  # Diperbarui
            severity="HIGH",  # Diperbarui sesuai mapping (HIGH)
            description="Deteksi klaim absolut tanpa pengecualian dalam konten",
            rationale="Klaim absolut dilarang oleh BPOM, EPI, dan Kominfo karena berpotensi menyesatkan dan menurunkan kapasitas kritis audiens"
        )

    def detect(self, text: str) -> bool:
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
        # Tambahan: deteksi pola absolut umum
        patterns = [
            "tanpa (sama sekali|sedikitpun|sedikit pun)",
            "tidak ada (risiko|resiko|bahaya|kegagalan)",
            "jamin (aman|aman 100%|aman seratus persen)"
        ]
        
        text_lower = text.lower()
        
        # Deteksi keyword sederhana
        if any(k in text_lower for k in keywords):
            return True
            
        # Deteksi pola (basic pattern matching)
        for pattern in patterns:
            import re
            if re.search(pattern, text_lower):
                return True
                
        return False

class SuperiorityClaimRule(Rule):
    def __init__(self):
        super().__init__(
            rule_id="LGL-SUP-01",  # Diperbarui sesuai mapping
            category="Brand & Message Consistency",  # Tetap (sesuai konteks klaim)
            severity="HIGH",  # Diperbarui (MEDIUM-HIGH → HIGH untuk konservatif)
            description="Deteksi klaim keunggulan relatif tanpa dasar pembanding yang jelas",
            rationale="Klaim superioritas harus dapat dibuktikan menurut EPI, KPI, dan Kominfo; berisiko tinggi secara reputasi dan rawan dipersoalkan kompetitor"
        )

    def detect(self, text: str) -> bool:
        keywords = [
            "terbaik",
            "nomor satu",
            "no. 1",
            "no 1",
            "paling direkomendasikan",
            "paling unggul",
            "paling baik",
            "lebih baik dari",
            "unggul daripada",
            "top of the line",
            "premium",
            "terhebat",
            "terdepan",
            "paling laris",
            "paling banyak dipakai",
            "paling banyak digunakan"
        ]
        return any(k.lower() in text.lower() for k in keywords)

class GuaranteeClaimRule(Rule):
    def __init__(self):
        super().__init__(
            rule_id="LGL-GUA-01",  # Diperbarui sesuai mapping
            category="Legal & Compliance",  # Tetap
            severity="HIGH",  # Tetap sesuai mapping
            description="Deteksi klaim yang menjanjikan hasil pasti, jaminan, atau kepastian outcome",
            rationale="Klaim jaminan dilarang oleh BPOM, Kemenkes, dan UU Perlindungan Konsumen; merupakan red flag tertinggi dan sering jadi sumber krisis hukum"
        )

    def detect(self, text: str) -> bool:
        keywords = [
            "dijamin",
            "jaminan",
            "pasti sembuh",
            "pasti berhasil",
            "pasti sukses",
            "100% efektif",
            "seratus persen efektif",
            "efektifitas absolut",
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
        
        # Tambahan: deteksi klaim medis yang dijamin
        medical_guarantee_phrases = [
            "jamin kesembuhan",
            "pasti sehat",
            "jamin pulih",
            "sembuh total",
            "sembuh 100%"
        ]
        
        text_lower = text.lower()
        
        # Deteksi keyword dasar
        if any(k in text_lower for k in keywords):
            return True
            
        # Deteksi kombinasi "jamin" + outcome medis
        for phrase in medical_guarantee_phrases:
            if phrase in text_lower:
                return True
                
        return False
