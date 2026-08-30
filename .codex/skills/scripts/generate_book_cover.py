#!/usr/bin/env python3
"""
generate_book_cover.py
Python helper script to populate and render Academic Book Cover Template (HTML/PDF)
Target Publisher: PT. Asadel Liamsindo Teknologi / Asadel Publisher (logo: https://cdn.lensetek.com/logo.png)

Usage:
  python generate_book_cover.py --title "Buku Ajar Pemrograman AI" --author "Andy Ismail" --isbn "978-623-1234-56-7" --output my_cover.html
"""

import sys
import os
import argparse
import html

# Find repository root path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
TEMPLATE_PATH = os.path.join(REPO_ROOT, "assets", "book_cover_template.html")

def generate_cover_html(title, subtitle, author, affiliation, category, synopsis, isbn, output_path):
    if not os.path.exists(TEMPLATE_PATH):
        print(f"Error: Master cover template not found at {TEMPLATE_PATH}")
        sys.exit(1)
        
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace default input field values in template
    content = content.replace('value="Buku Ajar Pemrograman Agentic AI"', f'value="{html.escape(title)}"')
    content = content.replace('value="Teori, Arsitektur Modern, dan Praktik Pengembangan AI Mandiri"', f'value="{html.escape(subtitle)}"')
    content = content.replace('value="Andy Ismail, M.Kom."', f'value="{html.escape(author)}"')
    content = content.replace('value="Universitas Indonesia & PT. Asadel Liamsindo Teknologi"', f'value="{html.escape(affiliation)}"')
    content = content.replace('value="978-623-0000-00-0"', f'value="{html.escape(isbn)}"')
    content = content.replace('Buku ini menyajikan panduan komprehensif mengenai konsep dan praktik pengembangan Agentic AI. Dirancang khusus untuk mahasiswa, dosen, dan praktisi kecerdasan buatan, buku ini membahas integrasi sistem mandiri, pengolahan data terstruktur, dan penerapan standar etika penerbitan ilmiah.', html.escape(synopsis))
    
    # Direct initial DOM text replacement for instant print rendering
    content = content.replace('id="displayTitle">Buku Ajar Pemrograman Agentic AI', f'id="displayTitle">{html.escape(title)}')
    content = content.replace('id="displaySubtitle">Teori, Arsitektur Modern, dan Praktik Pengembangan AI Mandiri', f'id="displaySubtitle">{html.escape(subtitle)}')
    content = content.replace('id="displayAuthor">Andy Ismail, M.Kom.', f'id="displayAuthor">{html.escape(author)}')
    content = content.replace('id="displayAffiliation">Universitas Indonesia & PT. Asadel Liamsindo Teknologi', f'id="displayAffiliation">{html.escape(affiliation)}')
    content = content.replace('id="displayCategory">BUKU AJAR AKADEMIK', f'id="displayCategory">{html.escape(category)}')
    content = content.replace('id="displayISBN">ISBN 978-623-0000-00-0', f'id="displayISBN">ISBN {html.escape(isbn)}')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"[+] Book cover HTML generated successfully: {output_path}")
    print("[+] Open the HTML file in any browser and click 'Cetak / Ekspor Cover ke PDF' to save as print-ready PDF.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Academic Book Cover HTML/PDF")
    parser.add_argument("--title", "-t", default="Buku Ajar Pemrograman Agentic AI", help="Book main title")
    parser.add_argument("--subtitle", "-s", default="Teori, Arsitektur Modern, dan Praktik Pengembangan AI Mandiri", help="Book subtitle")
    parser.add_argument("--author", "-a", default="Andy Ismail, M.Kom.", help="Author name")
    parser.add_argument("--affiliation", default="PT. Asadel Liamsindo Teknologi", help="Author affiliation")
    parser.add_argument("--category", default="BUKU AJAR AKADEMIK", help="Book category")
    parser.add_argument("--synopsis", default="Buku ini menyajikan panduan komprehensif mengenai konsep dan praktik pengembangan Agentic AI.", help="Back cover synopsis")
    parser.add_argument("--isbn", default="978-623-0000-00-0", help="ISBN Perpusnas number")
    parser.add_argument("--output", "-o", default="rendered_cover.html", help="Output HTML file path")
    
    args = parser.parse_args()
    generate_cover_html(args.title, args.subtitle, args.author, args.affiliation, args.category, args.synopsis, args.isbn, args.output)
