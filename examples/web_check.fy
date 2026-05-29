## web_check.fy - Web güvenlik kontrolü örneği
## Run: fly web_check.fy <url>
## Gerekli: pip install requests

use sys

try:
    use requests
catch ImportError:
    say "[-] requests kütüphanesi gerekli: pip install requests"
    sys.exit(1)

fn banner():
    say """
╔══════════════════════════════════╗
║   Fly Web Checker v1.0           ║
╚══════════════════════════════════╝"""

fn check_headers(url):
    """HTTP güvenlik başlıklarını kontrol et."""
    say f"\n[*] Hedef: {url}"
    say "-" * 50

    let security_headers = [
        "X-Frame-Options",
        "X-XSS-Protection",
        "X-Content-Type-Options",
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "Referrer-Policy",
        "Permissions-Policy",
    ]

    try:
        let r = requests.get(url, timeout=10, verify=false, allow_redirects=true)
        say f"[+] Durum Kodu: {r.status_code}"
        say f"[+] Sunucu    : {r.headers.get('Server', 'Gizli')}"
        say f"[+] İçerik    : {r.headers.get('Content-Type', '?')}"

        say f"\n[*] Güvenlik Başlıkları:"
        let found = 0
        let missing = 0

        for header in security_headers:
            if header in r.headers:
                say f"  [✓] {header}"
                found += 1
            else:
                say f"  [✗] {header} - EKSİK"
                missing += 1

        say f"\n[+] Skor: {found}/{len(security_headers)} başlık mevcut"

        if missing > 3:
            say "[!] Uyarı: Birçok güvenlik başlığı eksik!"
        elif missing == 0:
            say "[+] Tebrikler: Tüm güvenlik başlıkları mevcut!"

    catch requests.exceptions.SSLError:
        say "[!] SSL hatası - verify=False ile yeniden deneniyor"
    catch requests.exceptions.ConnectionError as e:
        say f"[-] Bağlantı hatası: {e}"
    catch Exception as e:
        say f"[-] Hata: {e}"

fn main():
    banner()

    if len(sys.argv) < 2:
        say "Kullanım: fly web_check.fy <url>"
        say "Örnek:    fly web_check.fy https://example.com"
        sys.exit(0)

    let url = sys.argv[1]
    if not url.startswith("http"):
        url = "http://" + url

    check_headers(url)

main()
