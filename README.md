# Fly Language 🚀

> A professional Python-powered scripting language with built-in Kali Linux tool integration.

```
  ███████╗██╗  ██╗   ██╗
  ██╔════╝██║  ╚██╗ ██╔╝
  █████╗  ██║   ╚████╔╝ 
  ██╔══╝  ██║    ╚██╔╝  
  ██║     ███████╗██║   
  ╚═╝     ╚══════╝╚═╝   
```

## Kurulum

### PyPI üzerinden (önerilen)
```bash
pip install fly-lang
```

### Kaynaktan
```bash
git clone https://github.com/ThT0AltayHR/Fly-lang.git
cd fly-lang
pip install -e .
```

---

## Hızlı Başlangıç

Bir dosya oluştur:
```bash
fly new myscript.fy
```

Çalıştır:
```bash
fly myscript.fy
# veya
fly run myscript.fy
```

---

## Syntax — Fly vs Python

| Fly            | Python          | Açıklama                  |
|----------------|-----------------|---------------------------|
| `fn`           | `def`           | Fonksiyon tanımlama       |
| `say`          | `print`         | Ekrana yazdır             |
| `ask`          | `input`         | Kullanıcıdan giriş al     |
| `use`          | `import`        | Modül içe aktar           |
| `let`          | *(yok)*         | Değişken tanımlama        |
| `const`        | *(yok)*         | Sabit tanımlama           |
| `catch`        | `except`        | Hata yakalama             |
| `throw`        | `raise`         | Hata fırlatma             |
| `null`         | `None`          | Boş değer                 |
| `true`/`false` | `True`/`False`  | Boolean                   |
| `##`           | `#`             | Yorum satırı              |
| `shell()`      | `subprocess`    | Shell komutu çalıştır     |
| `scan()`       | nmap wrapper    | Port tarama               |
| `recon()`      | socket lookup   | Domain keşif              |
| `tool()`       | subprocess      | Kali aracı çalıştır       |

---

## Kod Örnekleri

### Merhaba Dünya
```fly
fn main():
    say "Merhaba, Fly!"

main()
```

### Fonksiyonlar
```fly
fn topla(a, b):
    return a + b

let sonuc = topla(10, 20)
say f"Sonuç: {sonuc}"
```

### Sınıflar (Python ile aynı)
```fly
class Insan:
    fn init(self, isim, yas):
        self.isim = isim
        self.yas = yas

    fn tanitim(self):
        say f"Ben {self.isim}, {self.yas} yaşındayım."

let ali = Insan("Ali", 25)
ali.tanitim()
```

### Hata Yönetimi
```fly
try:
    let x = int(ask("Bir sayı gir: "))
    say f"Girdiğin sayı: {x}"
catch ValueError:
    say "Hata: Geçersiz sayı!"
```

### Shell Komutu
```fly
## Sistem bilgisi al
shell("uname -a")

## Çıktıyı yakala
let hostname = shell("hostname", capture=true)
say f"Host: {hostname}"
```

### OSINT / Tarama
```fly
use socket

## Domain çözümle
let ip = recon("example.com")

## Port tarama (nmap gerekli)
scan("192.168.1.1", ports="22,80,443")

## Kali aracı çalıştır
tool("wafw00f", "https://example.com")
```

---

## Kali Linux Araç Yöneticisi

```bash
# Araç yükle
fly install wafw00f
fly install nmap
fly install sqlmap
fly install nikto
fly install gobuster
fly install subfinder

# Araçları listele
fly list

# Araç kaldır
fly remove wafw00f

# Araç ara
fly search "web scanner"

# Araçları güncelle
fly update
```

---

## Araç Çalıştırma

```bash
# Direkt araç çalıştırma
fly nmap -sV 192.168.1.1

# Script ile çalıştırma
fly osint.fy example.com
fly scanner.fy 192.168.1.1 1 1000
fly web_check.fy https://example.com
```

---

## Transpile (Debug)

Fly kodunun Python karşılığını görüntüle:
```bash
fly transpile myscript.fy
```

---

## REPL (İnteraktif Mod)

```bash
fly repl
```

```
Fly Language REPL v1.0.0
Type 'exit()' or Ctrl+D to quit
========================================
fly> say "Merhaba!"
Merhaba!
fly> let x = 42
fly> say x * 2
84
```

---

## Python ile Uyumluluk

Fly, Python'ın **tüm özelliklerini** destekler:

- Tüm Python standart kütüphaneleri
- Pip paketleri (`use requests`, `use pandas`, vb.)
- Async/await
- List/dict comprehensions
- Decorators
- Type hints
- f-strings
- Context managers (`with`)
- Generators

---

## Dosya Uzantısı

- `.fy` — Standart Fly scripti
- `.fly` — Alternatif uzantı (ikisi de çalışır)

---

## GitHub'a Yükleme

```bash
git init
git add .
git commit -m "Initial commit - Fly Language v1.0.0"
git remote add origin https://github.com/YOUR_USERNAME/fly-lang.git
git push -u origin main
```

---

## PyPI'a Yayınlama

```bash
pip install build twine

# Paket oluştur
python -m build

# PyPI'a yükle
twine upload dist/*
```

Sonra herkes şu şekilde kurabilir:
```bash
pip install fly-lang
```

---

## Lisans

MIT License — Özgürce kullanabilir, değiştirebilir ve dağıtabilirsiniz.

---

## Katkıda Bulunma

Pull request ve issue'lar memnuniyetle karşılanır!

```
fly new myscript.fy  # Katkını başlat
```
