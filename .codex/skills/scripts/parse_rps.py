#!/usr/bin/env python3
"""
parse_rps.py - Syllabus & RPS Parser Helper
Extracts CPMK, Sub-CPMK, weekly course topics, learning outcomes, and assessment plans into structured JSON.
"""

import sys
import json
import re
from typing import Dict, Any, List

def parse_rps_text(text: str) -> Dict[str, Any]:
    cpmks = re.findall(r"(CPMK[- ]?\d*[:\s][^\n]+)", text, re.IGNORECASE)
    sub_cpmks = re.findall(r"(Sub[- ]?CPMK[- ]?\d*[:\s][^\n]+)", text, re.IGNORECASE)
    weeks = re.findall(r"(Minggu\s*\d+|Week\s*\d+|Pertemuan\s*\d+)[:\s]*([^\n]+)", text, re.IGNORECASE)

    parsed_weeks = []
    for w in weeks:
        parsed_weeks.append({
            "week": w[0].strip(),
            "topic": w[1].strip()
        })

    return {
        "status": "PARSED",
        "cpmk_count": len(cpmks),
        "cpmks": [c.strip() for c in cpmks],
        "sub_cpmks": [s.strip() for s in sub_cpmks],
        "weekly_topics": parsed_weeks
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_rps.py <rps_file_or_text>")
        sys.exit(1)

    arg = sys.argv[1]
    text = ""
    try:
        with open(arg, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception:
        text = arg

    res = parse_rps_text(text)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
