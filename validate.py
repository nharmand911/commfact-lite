import sys
from core.validation import validate_content

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate.py \"content text\"")
        sys.exit(1)

    text = sys.argv[1]
    result = validate_content(text)

    print("\n=== COMMFACT VALIDATION RESULT ===")
    print(f"Final Severity: {result['final_severity']}\n")

    if not result["triggered_rules"]:
        print("No rules triggered.")
        return

    print("Triggered Rules:")
    for r in result["triggered_rules"]:
        print(
            f"- {r['rule_id']} | {r['severity']} | {r['category']}\n"
            f"  {r['description']}"
        )

if __name__ == "__main__":
    main()
