## scanner.fy - Port Scanner Example
## Run: fly scanner.fy <host> <start_port> <end_port>

use sys
use socket
use concurrent.futures as futures
use datetime

fn banner():
    say """
╔═══════════════════════════════╗
║   Fly Port Scanner v1.0       ║
╚═══════════════════════════════╝"""

fn check_port(args):
    """Tek bir port kontrol eder."""
    host, port = args
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((host, port))
        s.close()
        return port if result == 0 else null
    catch:
        return null

fn get_service(port):
    """Port numarasına göre servis adı döndür."""
    let services = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
        5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
        8443: "HTTPS-Alt", 27017: "MongoDB"
    }
    return services.get(port, "unknown")

fn scan(host, start, end):
    """Çoklu thread ile port tara."""
    say f"\n[*] Tarama başlıyor: {host}"
    say f"[*] Port aralığı: {start}-{end}"
    
    let start_time = datetime.datetime.now()
    let port_range = list(range(start, end + 1))
    let args_list = [(host, p) for p in port_range]
    let open_ports = []

    with futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(check_port, args_list))

    for result in results:
        if result is not null:
            open_ports.append(result)

    let elapsed = (datetime.datetime.now() - start_time).seconds

    say f"\n{'='*45}"
    say f"  TARAMA SONUÇLARI - {host}"
    say f"{'='*45}"

    if open_ports:
        for port in sorted(open_ports):
            let service = get_service(port)
            say f"  [AÇIK] {port:<6} {service}"
    else:
        say "  Açık port bulunamadı."

    say f"{'='*45}"
    say f"  Toplam: {len(open_ports)} açık port | Süre: {elapsed}s"
    say f"{'='*45}"

fn main():
    banner()

    if len(sys.argv) < 2:
        say "\nKullanım: fly scanner.fy <host> [başlangıç] [bitiş]"
        say "Örnek:    fly scanner.fy 192.168.1.1 1 1000"
        sys.exit(0)

    let host = sys.argv[1]
    let start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    let end = int(sys.argv[3]) if len(sys.argv) > 3 else 1024

    try:
        let ip = socket.gethostbyname(host)
        say f"[+] {host} -> {ip}"
        scan(ip, start, end)
    catch socket.gaierror:
        say f"[-] Host çözümlenemedi: {host}"
        sys.exit(1)

main()
