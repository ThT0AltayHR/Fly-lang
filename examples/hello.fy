## hello.fy - Fly Language Hello World
## Run: fly hello.fy

use sys

fn greet(name):
    say f"Merhaba, {name}! Fly diline hoş geldin."
    say f"Python versiyonu: {sys.version}"

fn main():
    say "=" * 40
    say "  Fly Language v1.0.0"
    say "=" * 40

    greet("Dünya")

    ## Basit matematik
    let x = 10
    let y = 25
    say f"10 + 25 = {x + y}"

    ## Liste örneği
    let tools = ["nmap", "wafw00f", "sqlmap", "nikto", "gobuster"]
    say "\nPopüler güvenlik araçları:"
    for tool in tools:
        say f"  - {tool}"

    ## Şart ifadesi
    let os_type = sys.platform
    if os_type == "linux":
        say "\n[+] Linux sistemi tespit edildi - Kali modu aktif!"
    else:
        say f"\n[?] Platform: {os_type}"

main()
