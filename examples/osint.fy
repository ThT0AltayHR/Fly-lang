## osint.fy - OSINT Script Example
## Run: fly osint.fy
## Bu dosya Fly dilinin OSINT yeteneklerini gösterir

use sys
use socket
use os

fn banner():
    say """
╔══════════════════════════════════╗
║   Fly OSINT Module v1.0          ║
║   Powered by Fly Language        ║
╚══════════════════════════════════╝
"""

fn resolve_domain(domain):
    """Bir domain'in IP adresini çöz."""
    try:
        ip = socket.gethostbyname(domain)
        say f"[+] {domain} -> {ip}"
        return ip
    catch socket.gaierror as e:
        say f"[-] {domain} çözümlenemedi: {e}"
        return null

fn port_check(host, port):
    """Belirtilen port açık mı kontrol et."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex((host, port))
        s.close()
        if result == 0:
            say f"[+] {host}:{port} - AÇIK"
            return true
        else:
            say f"[-] {host}:{port} - KAPALI"
            return false
    catch Exception as e:
        say f"[!] Hata: {e}"
        return false

fn quick_scan(domain):
    """Hızlı OSINT taraması."""
    say f"\n[*] Hedef taranıyor: {domain}"
    say "-" * 40

    ip = resolve_domain(domain)

    if ip:
        say f"\n[*] Popüler portlar kontrol ediliyor..."
        let ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 8080, 8443]
        let open_ports = []

        for port in ports:
            if port_check(ip, port):
                open_ports.append(port)

        say f"\n[+] Özet:"
        say f"    Domain : {domain}"
        say f"    IP     : {ip}"
        say f"    Açık   : {open_ports}"

fn main():
    banner()

    if len(sys.argv) < 2:
        say "Kullanım: fly osint.fy <domain>"
        say "Örnek:    fly osint.fy example.com"
        sys.exit(0)

    let target = sys.argv[1]
    quick_scan(target)

main()
