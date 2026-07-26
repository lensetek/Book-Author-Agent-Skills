#!/usr/bin/env python3
"""
build_cpmk_matrix.py - CPMK-to-Chapter Matrix Builder
Transforms parsed RPS data into a Markdown matrix mapping CPMKs to textbook chapters, learning objectives, and exercises.
"""

import sys
import json
import os
from typing import Dict, Any, List

def build_matrix(parsed_data: Dict[str, Any], output_path: str = "cpmk_matrix.md") -> str:
    cpmks = parsed_data.get("cpmks", [])
    topics = parsed_data.get("weekly_topics", [])

    lines = [
        "# Matriks Pemetaan CPMK ke Bab Buku Ajar\n",
        "| No | CPMK / Sub-CPMK | Pokok Bahasan / Topik | Rencana Bab Buku Ajar | Bentuk Asesmen / Latihan |",
        "|---|---|---|---|---|",
    ]

    if not cpmks and not topics:
        lines.append("| 1 | CPMK 1 (Umum) | Topik Utama | Bab 1: Pengantar | Latihan Soal & Quizz |")
    else:
        for idx, t in enumerate(topics, 1):
            cpmk_ref = cpmks[(idx - 1) % len(cpmks)] if cpmks else f"CPMK {(idx + 1) // 2}"
            lines.append(f"| {idx} | {cpmk_ref} | {t.get('topic', 'Topik')} | Bab {idx}: {t.get('topic', 'Topik')} | Tugas & Latihan Bab {idx} |")

    content = "\n".join(lines) + "\n"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python build_cpmk_matrix.py <parsed_rps_json_or_file> [output_path.md]")
        sys.exit(1)

    input_arg = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "cpmk_matrix.md"

    parsed = {}
    try:
        if os.path.exists(input_arg):
            with open(input_arg, "r", encoding="utf-8") as f:
                parsed = json.load(f)
        else:
            parsed = json.loads(input_arg)
    except Exception:
        parsed = {"cpmks": [], "weekly_topics": [{"topic": input_arg}]}

    built = build_matrix(parsed, out_path)
    print(json.dumps({"status": "SUCCESS", "matrix_file": built}, indent=2))

if __name__ == "__main__":
    main()
