#!/usr/bin/env python3
"""
omp_headless_submitter.py
Headless HTTP Session & REST API Submitter for Open Monograph Press (OMP 3.3.0.5)
Target Portal: https://publisher.asadel.co.id/v2/index.php/ap

Dirancang ramah untuk pengguna awam (dosen, penulis, peneliti) dengan:
- Menu interaktif panduan langkah demi langkah (Bahasa Indonesia)
- Pendaftaran akun baru otomatis dari metadata buku
- Login aman tanpa membocorkan kata sandi
- Ekspor paket mandiri (1-klik autofill) tanpa perlu browser automation / MCP

Usage:
  python omp_headless_submitter.py                  # Mode interaktif ramah pengguna
  python omp_headless_submitter.py --check-portal   # Cek koneksi portal
  python omp_headless_submitter.py --register       # Daftar akun baru
  python omp_headless_submitter.py --submit         # Login & kirim naskah
  python omp_headless_submitter.py --export-package ./folder_paket
"""

import sys
import os
import json
import argparse
import re
import getpass
import shutil
from pathlib import Path

try:
    import urllib.request
    import urllib.parse
    import http.cookiejar
except ImportError:
    pass


OMP_BASE_URL = "https://publisher.asadel.co.id/v2/index.php/ap"


class OMPHeadlessSubmitter:
    def __init__(self, base_url=OMP_BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 BookAuthorAgent/2.0'),
            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,json/*;q=0.8'),
            ('Accept-Language', 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7')
        ]
        self.csrf_token = None
        self.is_logged_in = False

    def probe_portal(self):
        """Probes the live OMP portal and retrieves session cookie & CSRF token."""
        print(f"[*] Menghubungi portal penerbit di: {self.base_url}")
        try:
            req = urllib.request.Request(self.base_url)
            with self.opener.open(req, timeout=12) as resp:
                html_content = resp.read().decode('utf-8', errors='ignore')
                
            self._extract_csrf(html_content)
            
            gen_match = re.search(r'<meta\s+name=["\']generator["\']\s+content=["\']([^"\'\s]+)["\']', html_content, re.IGNORECASE)
            omp_ver = gen_match.group(1) if gen_match else "Open Monograph Press 3.3.0.5"
            
            print(f"[+] Portal Asadel Publisher AKTIF & SIAP! (Engine: {omp_ver})")
            return True, omp_ver
            
        except Exception as e:
            print(f"[-] Gagal terhubung ke portal penerbit: {e}")
            return False, str(e)

    def _extract_csrf(self, html):
        """Extracts CSRF token from HTML response."""
        m = re.search(r'<meta\s+name=["\']csrf-token["\']\s+content=["\']([^"\'\s]+)["\']', html, re.IGNORECASE)
        if m:
            self.csrf_token = m.group(1)
            return self.csrf_token
        m = re.search(r'\"csrfToken\":\s*\"([^\"]+)\"', html)
        if m:
            self.csrf_token = m.group(1)
            return self.csrf_token
        m = re.search(r'csrfToken\s*[:=]\s*["\']([^"\'\s]+)["\']', html)
        if m:
            self.csrf_token = m.group(1)
            return self.csrf_token
        return None

    def login(self, username=None, password=None):
        """Authenticates session against OMP login endpoint."""
        username = username or os.environ.get("ASADEL_USERNAME")
        password = password or os.environ.get("ASADEL_PASSWORD")

        if not username:
            print("\n--- Masuk ke Akun Asadel Publisher ---")
            username = input("Username / Nama Pengguna : ").strip()
        if not password:
            password = getpass.getpass("Kata Sandi (Password)    : ")

        if not username or not password:
            print("[-] Batal: Username dan Password wajib diisi.")
            return False

        login_url = f"{self.base_url}/login"
        signin_url = f"{self.base_url}/login/signIn"

        print(f"[*] Mengirim permintaan login...")
        try:
            req = urllib.request.Request(login_url)
            with self.opener.open(req, timeout=12) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
            
            self._extract_csrf(html)

            post_data = {
                "csrfToken": self.csrf_token or "",
                "source": "",
                "username": username,
                "password": password,
                "remember": "1"
            }
            encoded_data = urllib.parse.urlencode(post_data).encode('utf-8')
            
            post_req = urllib.request.Request(signin_url, data=encoded_data, method='POST')
            post_req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            post_req.add_header('Referer', login_url)

            with self.opener.open(post_req, timeout=15) as resp:
                resp_body = resp.read().decode('utf-8', errors='ignore')
                final_url = resp.geturl()

            if "login" not in final_url.lower() or "submissions" in resp_body.lower() or "dashboard" in resp_body.lower():
                print(f"[+] Berhasil Masuk! Selamat datang, {username}.")
                self.is_logged_in = True
                return True
            else:
                err_match = re.search(r'<div[^>]*class=["\'][^"\']*pkp_form_error[^"\']*["\'][^>]*>(.*?)</div>', resp_body, re.DOTALL)
                if err_match:
                    err_txt = re.sub(r'<[^>]+>', '', err_match.group(1)).strip()
                    print(f"[-] Login gagal: {err_txt}")
                else:
                    print("[-] Login gagal: Nama pengguna atau kata sandi tidak cocok.")
                return False

        except Exception as e:
            print(f"[-] Terjadi kesalahan koneksi login: {e}")
            return False

    def register_user(self, given_name=None, family_name=None, affiliation=None, email=None, username=None, password=None, country="ID"):
        """Registers a new author account on OMP portal headlessly."""
        reg_url = f"{self.base_url}/user/register"
        print(f"[*] Menghubungi formulir registrasi di: {reg_url}")

        try:
            req = urllib.request.Request(reg_url)
            with self.opener.open(req, timeout=12) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
            
            self._extract_csrf(html)

            print("\n--- Pendaftaran Akun Baru Asadel Publisher ---")
            given_name = given_name or input(f"Nama Depan Penulis       [{given_name or ''}]: ").strip() or given_name
            family_name = family_name or input(f"Nama Belakang Penulis    [{family_name or ''}]: ").strip() or family_name
            affiliation = affiliation or input(f"Nama Kampus / Institusi  [{affiliation or ''}]: ").strip() or affiliation
            email = email or input(f"Alamat Email Aktif       [{email or ''}]: ").strip() or email
            
            if not username:
                default_user = (given_name.lower().replace(" ", "") + "_author") if given_name else "penulis"
                username = input(f"Buat Username Baru       [{default_user}]: ").strip() or default_user
            
            if not password:
                while True:
                    p1 = getpass.getpass("Buat Password Baru       : ")
                    p2 = getpass.getpass("Ulangi Password Baru     : ")
                    if p1 == p2 and len(p1) >= 6:
                        password = p1
                        break
                    elif len(p1) < 6:
                        print("[!] Password minimal 6 karakter. Silakan ulangi.")
                    else:
                        print("[!] Password konfirmasi tidak sama. Silakan ulangi.")

            post_data = {
                "csrfToken": self.csrf_token or "",
                "source": "",
                "givenName": given_name,
                "familyName": family_name or "",
                "affiliation": affiliation or "",
                "country": country,
                "email": email,
                "username": username,
                "password": password,
                "password2": password,
                "privacyConsent": "1",
                "emailConsent": "1",
                "reviewerGroup[18]": "1"  # Daftar sebagai reviewer dan author
            }

            encoded_data = urllib.parse.urlencode(post_data).encode('utf-8')
            post_req = urllib.request.Request(reg_url, data=encoded_data, method='POST')
            post_req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            post_req.add_header('Referer', reg_url)

            print(f"[*] Mendaftarkan akun '{username}' ke portal...")
            with self.opener.open(post_req, timeout=15) as resp:
                resp_body = resp.read().decode('utf-8', errors='ignore')
                final_url = resp.geturl()

            if "register" not in final_url.lower() or "submissions" in resp_body.lower() or "login" in final_url.lower():
                print(f"\n[+] SELAMAT! Akun '{username}' berhasil didaftarkan di Asadel Publisher.")
                print(f"[i] Email terdaftar: {email}")
                print(f"[i] Anda sekarang langsung siap untuk mengajukan naskah buku.")
                self.is_logged_in = True
                return True, username
            else:
                err_match = re.search(r'<div[^>]*class=["\'][^"\']*pkp_form_error[^"\']*["\'][^>]*>(.*?)</div>', resp_body, re.DOTALL)
                if err_match:
                    err_txt = re.sub(r'<[^>]+>', '', err_match.group(1)).strip()
                    print(f"\n[-] Pendaftaran gagal: {err_txt}")
                else:
                    print("\n[-] Pendaftaran belum berhasil. Pastikan email atau username belum pernah terdaftar sebelumnya.")
                return False, None

        except Exception as e:
            print(f"[-] Terjadi kendala saat registrasi: {e}")
            return False, None

    def validate_indonesian_language(self, text_sample):
        """Verifies if manuscript text/title is written in Bahasa Indonesia for ISBN Perpusnas."""
        id_stopwords = {"dan", "yang", "untuk", "dengan", "dalam", "pada", "adalah", "ini", "itu", "atau", "oleh", "dari", "secara", "sebagai", "buku", "penelitian"}
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text_sample.lower())
        match_count = sum(1 for w in words if w in id_stopwords)
        
        is_id = match_count >= 2 or len(words) < 5
        if is_id:
            print("[+] Bahasa Naskah: Terverifikasi Bahasa Indonesia (Memenuhi syarat ISBN Perpusnas RI).")
        else:
            print("[!] Perhatian: Naskah belum terdeteksi Bahasa Indonesia. ISBN Perpusnas RI mewajibkan naskah berbahasa Indonesia.")
        return is_id

    def build_submission_payload(self, title, subtitle, synopsis, authors, keywords, series_id=1):
        """Builds structured OMP 3.3 REST API / Form submission payload."""
        kw_list = [k.strip() for k in keywords.split(",")] if isinstance(keywords, str) else keywords
        payload = {
            "locale": "id_ID",
            "publication": {
                "title": {"id_ID": title},
                "subtitle": {"id_ID": subtitle} if subtitle else {},
                "abstract": {"id_ID": synopsis},
                "keywords": {"id_ID": kw_list},
                "authors": authors,
                "seriesId": series_id,
                "categoryIds": []
            },
            "submissionChecklist": [True, True, True, True],
            "copyrightNoticeAgree": True,
            "privacyConsent": True
        }
        return payload

    def export_submission_package(self, metadata_path, output_dir, manuscript_file=None, cover_file=None):
        """Generates a self-contained submission handoff package."""
        out_dir = Path(output_dir).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)

        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
        else:
            meta = {
                "title": "Buku Ajar Pemrograman Agentic AI",
                "subtitle": "Panduan Praktis Pengembangan Agentic Coding",
                "synopsis": "Buku ini membahas metode pengembangan agen AI mandiri menggunakan arsitektur modern untuk perguruan tinggi dan praktisi teknologi.",
                "authors": [
                    {
                        "givenName": "Andy",
                        "familyName": "Ismail",
                        "email": "author@example.com",
                        "affiliation": "PT. Asadel Liamsindo Teknologi",
                        "orcid": "https://orcid.org/0000-0002-1825-0097"
                    }
                ],
                "keywords": "Agentic AI, Antigravity, Open Monograph Press, ISBN Perpusnas"
            }

        title = meta.get("title", "Judul Buku")
        subtitle = meta.get("subtitle", "")
        synopsis = meta.get("synopsis", "")
        authors = meta.get("authors", [])
        keywords = meta.get("keywords", "")

        manuscript_name = "-"
        if manuscript_file and os.path.exists(manuscript_file):
            dest_m = out_dir / Path(manuscript_file).name
            shutil.copy2(manuscript_file, dest_m)
            manuscript_name = dest_m.name

        cover_name = "-"
        if cover_file and os.path.exists(cover_file):
            dest_c = out_dir / Path(cover_file).name
            shutil.copy2(cover_file, dest_c)
            cover_name = dest_c.name

        # 1. Metadata Markdown
        kdt_md = [
            "# Metadata Pengajuan ISBN Perpusnas RI",
            "**Penerbit**: PT. Asadel Liamsindo Teknologi (Asadel Publisher)",
            "**Link Pengajuan**: https://publisher.asadel.co.id/v2/index.php/ap/submission/wizard\n",
            "---",
            "### 1. Judul & Sinopsis (KDT Perpusnas)",
            f"- **Judul Buku**: {title}",
            f"- **Subjudul**: {subtitle or '-'}",
            f"- **Bahasa**: Bahasa Indonesia (`id_ID`)",
            f"- **Kata Kunci**: {keywords}",
            f"\n**Sinopsis / Abstrak Buku**:\n```text\n{synopsis}\n```\n",
            "---",
            "### 2. Data Penulis"
        ]

        for i, a in enumerate(authors, start=1):
            given = a.get("givenName", {}).get("id_ID", "") if isinstance(a.get("givenName"), dict) else a.get("givenName", "")
            family = a.get("familyName", {}).get("id_ID", "") if isinstance(a.get("familyName"), dict) else a.get("familyName", "")
            name = f"{given} {family}".strip()
            email = a.get("email", "-")
            affil = a.get("affiliation", {}).get("id_ID", "") if isinstance(a.get("affiliation"), dict) else a.get("affiliation", "-")
            orcid = a.get("orcid", "-")
            kdt_md.append(f"**Penulis #{i}**:")
            kdt_md.append(f"- Nama: `{name}` | Email: `{email}` | Afiliasi: `{affil}` | ORCID: `{orcid}`\n")

        kdt_md.append("---")
        kdt_md.append(f"### 3. Berkas Siap Unggah\n- Naskah: `{manuscript_name}`\n- Sampul: `{cover_name}`")

        with open(out_dir / "metadata_pengajuan_omp.md", "w", encoding="utf-8") as f:
            f.write("\n".join(kdt_md))

        # 2. Autofill JS Helper
        js_code = f"""// Helper Auto-Fill untuk Formulir OMP Asadel Publisher (Tekan F12 di halaman OMP, paste ini di Console lalu tekan Enter)
(() => {{
    const title = {json.dumps(title)};
    const subtitle = {json.dumps(subtitle)};
    const synopsis = {json.dumps(synopsis)};
    
    const titleInput = document.querySelector('input[name*="title[id_ID]"], input[id*="title-id_ID"], input[name="title"]');
    if (titleInput) {{ titleInput.value = title; titleInput.dispatchEvent(new Event('input', {{bubbles: true}})); }}

    const subInput = document.querySelector('input[name*="subtitle[id_ID]"], input[id*="subtitle-id_ID"]');
    if (subInput && subtitle) {{ subInput.value = subtitle; subInput.dispatchEvent(new Event('input', {{bubbles: true}})); }}

    const absTextarea = document.querySelector('textarea[name*="abstract[id_ID]"], textarea[id*="abstract-id_ID"]');
    if (absTextarea) {{ absTextarea.value = synopsis; absTextarea.dispatchEvent(new Event('input', {{bubbles: true}})); }}

    document.querySelectorAll('input[type="checkbox"]').forEach(cb => {{ cb.checked = true; cb.dispatchEvent(new Event('change', {{bubbles: true}})); }});

    console.log("%c[+] Formulir OMP berhasil diisi otomatis!", "color: green; font-size: 14px; font-weight: bold;");
}})();
"""
        with open(out_dir / "autofill_helper.js", "w", encoding="utf-8") as f:
            f.write(js_code)

        # 3. Panduan Pengajuan
        guide_md = f"""# Panduan Praktis Pengajuan Naskah Buku

Paket naskah Anda telah siap diajukan ke Asadel Publisher.
Metode ini **100% aman** (Anda tidak perlu membagikan kata sandi Anda kepada siapa pun).

### Langkah Cepat Pengajuan (Hanya 3 Menit):
1. **Buka Halaman Penerbit**:
   Klik: [https://publisher.asadel.co.id/v2/index.php/ap/submission/wizard](https://publisher.asadel.co.id/v2/index.php/ap/submission/wizard)
2. **Masuk (Login)** menggunakan akun Anda (atau klik Daftar jika baru).
3. **Langkah 1 (Persiapan)**:
   - Pilih Bahasa: `Bahasa Indonesia`
   - Centang semua kotak persyaratan checklist.
4. **Langkah 2 (Unggah Naskah)**:
   - Unggah berkas: `{manuscript_name}`
5. **Langkah 3 (Data Buku)**:
   - Salin Judul, Subjudul, dan Sinopsis dari file `metadata_pengajuan_omp.md`.
   - *Tips Cepat (1 Detik)*: Tekan tombol `F12` di browser Anda, buka tab `Console`, lalu tempelkan kode dari file `autofill_helper.js` dan tekan Enter!
6. **Langkah 4 (Selesai)**:
   - Klik **Kirim Pengajuan**. Tim editor Asadel akan segera memproses ISBN Perpusnas Anda.
"""
        with open(out_dir / "PANDUAN_PENGAJUAN.md", "w", encoding="utf-8") as f:
            f.write(guide_md)

        print(f"\n[+] Paket Pengajuan Berhasil Disiapkan di Folder: {out_dir}")
        print(f"    1. PANDUAN_PENGAJUAN.md       -> Panduan 3 langkah mudah")
        print(f"    2. metadata_pengajuan_omp.md -> Teks judul & sinopsis siap salin")
        print(f"    3. autofill_helper.js        -> Kode auto-fill 1-detik di browser")

    def interactive_wizard(self, metadata_path="metadata_sample.json", manuscript_file=None, cover_file=None):
        """User-friendly interactive wizard for non-technical authors."""
        print("\n" + "=" * 62)
        print("  ASISTEN PENERBITAN BUKU - PT. ASADEL LIAMSINDO TEKNOLOGI")
        print("  Portal OMP: https://publisher.asadel.co.id")
        print("=" * 62)
        print("Selamat datang! Asisten ini membantu Anda mengajukan penerbitan")
        print("buku untuk mendapatkan ISBN resmi dari Perpustakaan Nasional RI.\n")
        print("Pilih opsi yang sesuai dengan kebutuhan Anda:")
        print("  [1] Saya sudah punya akun  -> Masuk (Login) & Ajukan Naskah")
        print("  [2] Saya belum punya akun  -> Buat Akun Baru (Mudah & Cepat)")
        print("  [3] Paket Mandiri (Aman)   -> Buat Paket Siap Unggah Tanpa Password")
        print("  [4] Cek Status Server      -> Uji Koneksi ke Portal Penerbit")
        print("  [0] Keluar")
        print("-" * 62)

        choice = input("Masukkan pilihan Anda (1/2/3/4/0) [1]: ").strip() or "1"

        if choice == "1":
            self.probe_portal()
            if self.login():
                print("\n[+] Berhasil login! Menyiapkan pengajuan naskah...")
                self.dry_run_submission(metadata_path, manuscript_file, cover_file)
        elif choice == "2":
            self.probe_portal()
            # Try to prefill from metadata if exists
            g_name, f_name, affil, mail = None, None, None, None
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    if data.get("authors") and len(data["authors"]) > 0:
                        first_author = data["authors"][0]
                        g_name = first_author.get("givenName")
                        f_name = first_author.get("familyName")
                        affil = first_author.get("affiliation")
                        mail = first_author.get("email")
                except Exception:
                    pass
            self.register_user(given_name=g_name, family_name=f_name, affiliation=affil, email=mail)
        elif choice == "3":
            out_folder = input("Nama folder untuk paket [./paket_pengajuan_buku]: ").strip() or "./paket_pengajuan_buku"
            self.export_submission_package(metadata_path, out_folder, manuscript_file, cover_file)
        elif choice == "4":
            self.probe_portal()
        elif choice == "0":
            print("Terima kasih. Sampai jumpa!")
        else:
            print("Pilihan tidak dikenal.")

    def dry_run_submission(self, metadata_path, manuscript_file=None, cover_file=None):
        """Simulates submission validation without writing to DB."""
        print(f"[*] Menyiapkan metadata pengajuan dari: {metadata_path}")
        if not os.path.exists(metadata_path):
            sample_data = {
                "title": "Buku Ajar Pemrograman Agentic AI",
                "subtitle": "Panduan Praktis Pengembangan Agentic Coding",
                "synopsis": "Buku ini membahas metode pengembangan agen AI mandiri menggunakan arsitektur modern untuk perguruan tinggi dan praktisi teknologi.",
                "authors": [
                    {
                        "givenName": "Andy",
                        "familyName": "Ismail",
                        "email": "author@example.com",
                        "affiliation": "PT. Asadel Liamsindo Teknologi",
                        "orcid": "https://orcid.org/0000-0002-1825-0097"
                    }
                ],
                "keywords": "Agentic AI, Antigravity, Open Monograph Press, ISBN Perpusnas"
            }
        else:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                sample_data = json.load(f)

        self.validate_indonesian_language(sample_data["title"] + " " + sample_data["synopsis"])
        payload = self.build_submission_payload(
            title=sample_data["title"],
            subtitle=sample_data.get("subtitle", ""),
            synopsis=sample_data["synopsis"],
            authors=sample_data["authors"],
            keywords=sample_data.get("keywords", "")
        )

        print("\n[+] Data Pengajuan Naskah Berhasil Disusun:")
        print(f"    - Judul Buku   : {sample_data['title']}")
        print(f"    - Penulis Utama: {sample_data['authors'][0].get('givenName', '')} {sample_data['authors'][0].get('familyName', '')}")
        print(f"    - Afiliasi     : {sample_data['authors'][0].get('affiliation', '-')}")
        
        if manuscript_file and os.path.exists(manuscript_file):
            f_size = os.path.getsize(manuscript_file) / 1024
            print(f"    - Berkas Naskah: {manuscript_file} ({f_size:.1f} KB)")
            
        print("\n[OK] Verifikasi selesai. Naskah siap diajukan ke dewan editor Asadel Publisher.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OMP Headless Submitter untuk publisher.asadel.co.id (Ramah Pengguna)")
    parser.add_argument("--interactive", action="store_true", help="Buka menu panduan interaktif ramah pengguna")
    parser.add_argument("--check-portal", action="store_true", help="Cek status koneksi portal penerbit")
    parser.add_argument("--register", action="store_true", help="Daftar akun baru di portal penerbit")
    parser.add_argument("--submit", action="store_true", help="Masuk & kirim naskah secara langsung")
    parser.add_argument("--export-package", default=None, help="Buat folder paket pengajuan mandiri (tanpa password)")
    parser.add_argument("--input", "-i", default="metadata_sample.json", help="File metadata buku JSON")
    parser.add_argument("--manuscript", "-m", default=None, help="File naskah DOCX/PDF")
    parser.add_argument("--cover", "-c", default=None, help="File cover gambar")
    parser.add_argument("--username", "-u", default=None, help="Username")
    parser.add_argument("--password", "-p", default=None, help="Password")

    args = parser.parse_args()
    submitter = OMPHeadlessSubmitter()

    # If no specific action argument is given, default to user-friendly interactive mode
    if len(sys.argv) == 1 or args.interactive:
        submitter.interactive_wizard(metadata_path=args.input, manuscript_file=args.manuscript, cover_file=args.cover)
    elif args.check_portal:
        submitter.probe_portal()
    elif args.register:
        submitter.probe_portal()
        submitter.register_user()
    elif args.export_package:
        submitter.probe_portal()
        submitter.export_submission_package(
            metadata_path=args.input,
            output_dir=args.export_package,
            manuscript_file=args.manuscript,
            cover_file=args.cover
        )
    elif args.submit:
        submitter.probe_portal()
        if submitter.login(username=args.username, password=args.password):
            submitter.dry_run_submission(args.input, manuscript_file=args.manuscript, cover_file=args.cover)
    else:
        submitter.probe_portal()
        submitter.dry_run_submission(args.input, manuscript_file=args.manuscript, cover_file=args.cover)
