#!/usr/bin/env python3
"""
generate_book_cover.py
Python helper script to populate and render Academic Book Cover Template (HTML/PDF)
Supports both specialized Asadel Publisher presets (using https://cdn.lensetek.com/logo.png)
and general publishers (University Press, IKAPI/Commercial, Custom without logos).

Usage:
  python generate_book_cover.py --preset asadel-id --title "Buku Ajar Pemrograman AI" --author "Andy Ismail" --output cover.html
"""

import sys
import os
import argparse
import html

# Find repository root path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
TEMPLATE_PATH = os.path.join(REPO_ROOT, "assets", "book_cover_template.html")

PRESET_DEFAULTS = {
    "asadel-id": {
        "publisher_name": "PT. ASADEL LIAMSINDO TEKNOLOGI",
        "publisher_website": "publisher.asadel.co.id | asadel.co.id",
        "show_logo": True
    },
    "asadel-intl": {
        "publisher_name": "ASADEL PUBLISHER",
        "publisher_website": "publisher.asadel.co.id",
        "show_logo": True
    },
    "university-press": {
        "publisher_name": "UI PUBLISHING / UGM PRESS",
        "publisher_website": "press.university.ac.id",
        "show_logo": False
    },
    "general-ikapi": {
        "publisher_name": "PENERBIT DEEPUBLISH / RAJAWALI PERS",
        "publisher_website": "penerbit-akademik.co.id",
        "show_logo": False
    },
    "custom": {
        "publisher_name": "PENERBIT AKADEMIK",
        "publisher_website": "www.penerbit.co.id",
        "show_logo": False
    }
}


def generate_cover_html(title, subtitle, author, affiliation, category, synopsis, isbn, preset, publisher_name, publisher_website, output_path):
    if not os.path.exists(TEMPLATE_PATH):
        print(f"Error: Master cover template not found at {TEMPLATE_PATH}")
        sys.exit(1)
        
    preset_info = PRESET_DEFAULTS.get(preset, PRESET_DEFAULTS["asadel-id"])
    pub_name = publisher_name if publisher_name else preset_info["publisher_name"]
    pub_web = publisher_website if publisher_website else preset_info["publisher_website"]
    show_logo = preset_info["show_logo"]
    
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Set selected preset in dropdown
    content = content.replace('<option value="asadel-id">', f'<option value="{preset}" selected>') if preset != "asadel-id" else content
    
    # Replace default input field values in template
    content = content.replace('value="Buku Ajar Pemrograman Agentic AI"', f'value="{html.escape(title)}"')
    content = content.replace('value="Teori, Arsitektur Modern, dan Praktik Pengembangan AI Mandiri"', f'value="{html.escape(subtitle)}"')
    content = content.replace('value="Andy Ismail, M.Kom."', f'value="{html.escape(author)}"')
    content = content.replace('value="Universitas Indonesia & PT. Asadel Liamsindo Teknologi"', f'value="{html.escape(affiliation)}"')
    content = content.replace('value="PT. ASADEL LIAMSINDO TEKNOLOGI"', f'value="{html.escape(pub_name)}"')
    content = content.replace('value="publisher.asadel.co.id | asadel.co.id"', f'value="{html.escape(pub_web)}"')
    content = content.replace('value="978-623-0000-00-0"', f'value="{html.escape(isbn)}"')
    content = content.replace('Buku ini menyajikan panduan komprehensif mengenai konsep dan praktik pengembangan Agentic AI. Dirancang khusus untuk mahasiswa, dosen, dan praktisi kecerdasan buatan, buku ini membahas integrasi sistem mandiri, pengolahan data terstruktur, dan penerapan standar etika penerbitan ilmiah.', html.escape(synopsis))
    
    # Direct initial DOM text replacement for instant print rendering
    content = content.replace('id="displayTitle">Buku Ajar Pemrograman Agentic AI', f'id="displayTitle">{html.escape(title)}')
    content = content.replace('id="displaySubtitle">Teori, Arsitektur Modern, dan Praktik Pengembangan AI Mandiri', f'id="displaySubtitle">{html.escape(subtitle)}')
    content = content.replace('id="displayAuthor">Andy Ismail, M.Kom.', f'id="displayAuthor">{html.escape(author)}')
    content = content.replace('id="displayAffiliation">Universitas Indonesia & PT. Asadel Liamsindo Teknologi', f'id="displayAffiliation">{html.escape(affiliation)}')
    content = content.replace('id="displayCategory">BUKU AJAR AKADEMIK', f'id="displayCategory">{html.escape(category)}')
    content = content.replace('id="displayISBN">ISBN 978-623-0000-00-0', f'id="displayISBN">ISBN {html.escape(isbn)}')
    content = content.replace('id="displayPublisherName">PT. ASADEL LIAMSINDO TEKNOLOGI', f'id="displayPublisherName">{html.escape(pub_name)}')
    content = content.replace('id="displayPublisherWebsite">publisher.asadel.co.id | asadel.co.id', f'id="displayPublisherWebsite">{html.escape(pub_web)}')

    if not show_logo:
        content = content.replace('id="frontPublisherLogo" class="publisher-logo-img"', 'id="frontPublisherLogo" class="publisher-logo-img" style="display:none;"')
        content = content.replace('id="backPublisherLogo" class="publisher-logo-img"', 'id="backPublisherLogo" class="publisher-logo-img" style="display:none;"')
        content = content.replace('<span id="displayPublisherBrand">Asadel Publisher</span>', '<span id="displayPublisherBrand" style="display:none;">Asadel Publisher</span>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"[+] Book cover HTML generated successfully ({preset} preset): {output_path}")
    print("[+] Open the HTML file in any browser and click 'Cetak / Ekspor Cover ke PDF' to save as print-ready PDF.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Academic Book Cover HTML/PDF")
    parser.add_argument("--preset", "-p", default="asadel-id", choices=list(PRESET_DEFAULTS.keys()), help="Publisher preset")
    parser.add_argument("--title", "-t", default="Buku Ajar Pemrograman Agentic AI", help="Book main title")
    parser.add_argument("--subtitle", "-s", default="Teori, Arsitektur Modern, dan Praktik Pengembangan AI Mandiri", help="Book subtitle")
    parser.add_argument("--author", "-a", default="Andy Ismail, M.Kom.", help="Author name")
    parser.add_argument("--affiliation", default="PT. Asadel Liamsindo Teknologi", help="Author affiliation")
    parser.add_argument("--publisher-name", default=None, help="Custom Publisher Name")
    parser.add_argument("--publisher-website", default=None, help="Custom Publisher Website")
    parser.add_argument("--category", default="BUKU AJAR AKADEMIK", help="Book category")
    parser.add_argument("--synopsis", default="Buku ini menyajikan panduan komprehensif mengenai konsep dan praktik pengembangan Agentic AI.", help="Back cover synopsis")
    parser.add_argument("--isbn", default="978-623-0000-00-0", help="ISBN Perpusnas number")
    parser.add_argument("--output", "-o", default="rendered_cover.html", help="Output HTML file path")
    
    args = parser.parse_args()
    generate_cover_html(
        title=args.title,
        subtitle=args.subtitle,
        author=args.author,
        affiliation=args.affiliation,
        category=args.category,
        synopsis=args.synopsis,
        isbn=args.isbn,
        preset=args.preset,
        publisher_name=args.publisher_name,
        publisher_website=args.publisher_website,
        output_path=args.output
    )
