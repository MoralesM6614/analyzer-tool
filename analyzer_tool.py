#!/usr/bin/env python3
# ============================================
# ANALYZER TOOL
# Autor: Cracke2
# Contacto: https://t.me/Cracke2
# Plataforma: Android / Termux
# ============================================

import os, sys, socket, requests, ipaddress, random, string, subprocess, json, time
from urllib.parse import urlparse

# ================= AUTO-INSTALACIÓN =================
def install(pkg):
    subprocess.call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])

try:
    from faker import Faker
    import pycountry
except:
    install("faker")
    install("pycountry")
    from faker import Faker
    import pycountry

# ================= CONFIG =================
VERSION = "3.3"
LANG = "ES"

# ================= COLORES =================
C_RESET="\033[0m"; C_GREEN="\033[92m"; C_RED="\033[91m"
C_YELLOW="\033[93m"; C_CYAN="\033[96m"; C_BOLD="\033[1m"

# ================= TEXTOS =================
TEXT = {
    "ES": {
        "menu":"Seleccione una opción",
        "invalid":"Opción inválida",
        "press":"Presione ENTER para continuar...",
        "again":"¿Generar nuevos datos? (S/N): ",
        "copy":"¿Copiar al portapapeles? (S/N): "
    },
    "EN": {
        "menu":"Select an option",
        "invalid":"Invalid option",
        "press":"Press ENTER to continue...",
        "again":"Generate again? (Y/N): ",
        "copy":"Copy to clipboard? (Y/N): "
    }
}

# ================= UTIL =================
def clear(): os.system("clear")
def pause(): input("\n" + TEXT[LANG]["press"])

def header(t):
    print(C_CYAN + "="*70)
    print(C_BOLD + t)
    print("="*70 + C_RESET)

# ================= OPCIÓN 1 =================
def network_status():
    clear(); header("🌐 ESTADO DE RED ACTUAL")
    try:
        ip = requests.get("https://api.ipify.org",timeout=5).text
        data = requests.get(f"http://ip-api.com/json/{ip}",timeout=5).json()
        print(f"""
IP pública : {ip}
País       : {data.get('country')}
Ciudad     : {data.get('city')}
ISP        : {data.get('isp')}
ASN        : {data.get('as')}
""")
    except:
        print(C_RED+"Error de red"+C_RESET)
    pause()

# ================= OPCIÓN 2 =================
def analyze_ip():
    clear(); header("📌 ANÁLISIS TÉCNICO DE IP")
    ip = input("IP: ").strip()
    try: ipaddress.ip_address(ip)
    except:
        print(C_RED+"IP inválida"+C_RESET); pause(); return

    d = requests.get(f"http://ip-api.com/json/{ip}",timeout=5).json()
    print(f"""
IP        : {ip}
País      : {d.get('country')}
Región    : {d.get('regionName')}
Ciudad    : {d.get('city')}
ZIP       : {d.get('zip')}
Lat/Lon   : {d.get('lat')}, {d.get('lon')}
ISP       : {d.get('isp')}
ASN       : {d.get('as')}
""")
    pause()

# ================= OPCIÓN 3 =================
def resolve_dns():
    clear(); header("📡 RESOLVER DNS")
    d = input("Dominio: ").strip()
    try:
        for ip in socket.gethostbyname_ex(d)[2]:
            print("•", ip)
    except:
        print("No encontrado")
    pause()

# ================= OPCIÓN 4 =================
def domain_ips():
    clear(); header("🌐 IPv4 / IPv6")
    d = input("Dominio: ").strip()
    v4,v6=set(),set()
    try:
        for i in socket.getaddrinfo(d,None):
            (v4 if i[0]==socket.AF_INET else v6).add(i[4][0])
    except: pass
    print("IPv4:", ", ".join(v4) or "N/A")
    print("IPv6:", ", ".join(v6) or "N/A")
    pause()

# ================= OPCIÓN 5 =================
def find_subdomains():
    clear(); header("🧩 SUBDOMINIOS")
    d=input("Dominio: ").strip()
    found=[]
    for p in ["www","api","mail","m","cdn","static"]:
        try:
            socket.gethostbyname(f"{p}.{d}")
            found.append(f"{p}.{d}")
        except: pass
    print("\n".join(found) if found else "No encontrados")
    pause()

# ================= OPCIÓN 6 =================
def site_info():
    clear(); header("📄 INFORMACIÓN DEL SITIO")
    url=input("URL: ").strip()
    if not url.startswith("http"): url="http://"+url
    try:
        r=requests.get(url,timeout=5)
        print(f"""
URL       : {r.url}
Estado    : {r.status_code}
Servidor  : {r.headers.get('Server')}
Tipo      : {r.headers.get('Content-Type')}
Tamaño    : {len(r.content)/1024:.2f} KB
""")
    except:
        print("No responde")
    pause()

# ================= OPCIÓN 7 =================
def curl_headers():
    clear(); header("🧰 CURL / HEADERS")
    url=input("URL: ").strip()
    os.system(f"curl -I {url}")
    pause()

# ================= OPCIÓN 8 =================
def password_generator():
    clear(); header("🔐 PASSWORD GENERATOR")
    length=int(input("Longitud (ej 16): ") or 16)
    chars=string.ascii_letters+string.digits+"@#$%&*-_+?"
    pwd="".join(random.choice(chars) for _ in range(length))
    print("\nPassword:", C_GREEN+pwd+C_RESET)
    c=input(TEXT[LANG]["copy"]).lower()
    if c in ("s","y"):
        os.system(f'echo "{pwd}" | termux-clipboard-set')
    pause()

# ================= OPCIÓN 9 =================
def temp_email():
    clear(); header("📧 EMAIL TEMPORAL")
    login="".join(random.choice(string.ascii_lowercase+string.digits) for _ in range(8))
    domain="1secmail.com"
    email=f"{login}@{domain}"
    print("Email:", C_GREEN+email+C_RESET)

    input("\nPresione ENTER para ver bandeja...")
    try:
        inbox=requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}").json()
        if not inbox:
            print("Bandeja vacía")
        for m in inbox:
            msg=requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={m['id']}").json()
            print(f"\nFrom: {msg['from']}\nSubject: {msg['subject']}\n{msg['textBody']}")
    except:
        print("Error al consultar")
    pause()

# ================= MENÚ =================
def menu():
    while True:
        clear(); header("ANALYZER TOOL")
        print(C_GREEN+f"Versión {VERSION}"+C_RESET)
        print("""
1) 🌐 Estado de red
2) 📌 Analizar IP
3) 📡 Resolver DNS
4) 🌐 IPv4 / IPv6
5) 🧩 Subdominios
6) 📄 Info sitio
7) 🧰 Curl / Headers
8) 🔐 Password Generator
9) 📧 Email temporal
0) ❌ Salir
""")
        op=input(TEXT[LANG]["menu"]+": ").strip()
        if   op=="1":network_status()
        elif op=="2":analyze_ip()
        elif op=="3":resolve_dns()
        elif op=="4":domain_ips()
        elif op=="5":find_subdomains()
        elif op=="6":site_info()
        elif op=="7":curl_headers()
        elif op=="8":password_generator()
        elif op=="9":temp_email()
        elif op=="0":sys.exit()
        else:
            print(TEXT[LANG]["invalid"]); pause()

if __name__=="__main__":
    menu()