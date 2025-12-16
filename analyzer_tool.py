#!/usr/bin/env python3
# ============================================
# ANALYZER TOOL
# Autor: Cracke2
# Contacto: https://t.me/Cracke2
# Plataforma: Android / Termux
# ============================================

import os, sys, socket, requests, ipaddress, random, string
from urllib.parse import urlparse

# ================= CONFIG =================
VERSION = "3.3"
VT_API_KEY = "43a2ed5e0ea79724d1c21fcec6d49059ff906c71df906d350bfa6ea08ea4cdcf"

# ================= COLORES =================
C_RESET  = "\033[0m"
C_GREEN  = "\033[92m"
C_RED    = "\033[91m"
C_YELLOW = "\033[93m"
C_CYAN   = "\033[96m"
C_BOLD   = "\033[1m"

# ================= UTILIDADES =================
def clear():
    os.system("clear")

def pause():
    input("\nPresione ENTER para continuar...")

def header(title):
    print(C_CYAN + "=" * 70)
    print(C_BOLD + title)
    print("=" * 70 + C_RESET)

# ================= OPCIÓN 1 =================
def network_status():
    clear()
    header("🌐 ESTADO DE RED ACTUAL")
    try:
        ip = requests.get("https://api.ipify.org", timeout=5).text
        data = requests.get(f"http://ip-api.com/json/{ip}", timeout=6).json()
        print(f"""
IP Pública : {ip}
País       : {data.get('country')}
Ciudad     : {data.get('city')}
ISP        : {data.get('isp')}
ASN        : {data.get('as')}
""")
    except:
        print(C_RED + "Error obteniendo información de red" + C_RESET)
    pause()

# ================= OPCIÓN 2 =================
def analyze_ip():
    clear()
    header("📌 ANÁLISIS TÉCNICO DE IP")

    ip = input("IP objetivo: ").strip()
    try:
        ipaddress.ip_address(ip)
    except:
        print(C_RED + "IP inválida" + C_RESET)
        pause()
        return

    data = requests.get(f"http://ip-api.com/json/{ip}", timeout=6).json()
    print(f"""
IP          : {ip}
País        : {data.get('country')}
Región      : {data.get('regionName')}
Ciudad      : {data.get('city')}
ZIP         : {data.get('zip')}
ISP         : {data.get('isp')}
ASN         : {data.get('as')}
Lat/Lon     : {data.get('lat')}, {data.get('lon')}
""")
    pause()

# ================= OPCIÓN 3 =================
def resolve_dns():
    clear()
    header("📡 RESOLVER DOMINIO")
    domain = input("Dominio: ").strip()
    try:
        _, _, ips = socket.gethostbyname_ex(domain)
        for i in ips:
            print("-", i)
    except:
        print("No encontrado")
    pause()

# ================= OPCIÓN 4 =================
def domain_ips():
    clear()
    header("🌐 IPv4 / IPv6")
    domain = input("Dominio: ").strip()
    try:
        infos = socket.getaddrinfo(domain, None)
        for info in infos:
            print(info[4][0])
    except:
        print("No encontrado")
    pause()

# ================= OPCIÓN 5 =================
def find_subdomains():
    clear()
    header("🧩 SUBDOMINIOS")
    domain = input("Dominio: ").strip()
    prefixes = ["www","mail","api","m","cdn"]
    found = False
    for p in prefixes:
        try:
            socket.gethostbyname(f"{p}.{domain}")
            print(f"- {p}.{domain}")
            found = True
        except:
            pass
    if not found:
        print("No encontrados")
    pause()

# ================= OPCIÓN 6 =================
def site_info():
    clear()
    header("📄 INFORMACIÓN DEL SITIO")
    url = input("URL: ").strip()
    if not url.startswith("http"):
        url = "http://" + url
    try:
        r = requests.get(url, timeout=6)
        print(f"""
URL Final : {r.url}
HTTP      : {r.status_code}
Servidor  : {r.headers.get('Server')}
Tamaño    : {len(r.content)/1024:.2f} KB
""")
    except:
        print("No responde")
    pause()

# ================= OPCIÓN 7 =================
def password_generator():
    clear()
    header("🔐 GENERADOR DE CONTRASEÑAS")
    length = input("Longitud (default 20): ").strip()
    length = int(length) if length.isdigit() else 20

    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+?"
    password = "".join(random.SystemRandom().choice(chars) for _ in range(length))

    print(f"\nContraseña generada:\n{C_GREEN}{password}{C_RESET}")
    pause()

# ================= OPCIÓN 8 =================
def clean_url():
    clear()
    header("🔗 LIMPIAR / REVELAR URL")
    url = input("URL: ").strip()
    if not url.startswith("http"):
        url = "http://" + url
    try:
        r = requests.head(url, allow_redirects=True, timeout=8)
        final = r.url
        if final == url:
            print("La URL NO está acortada")
        else:
            print("URL final:", final)
    except:
        print("Error procesando URL")
    pause()

# ================= OPCIÓN 9 =================
def virustotal_ip():
    clear()
    header("🛡️ VIRUSTOTAL IP CHECK")
    ip = input("IP a analizar: ").strip()

    headers = {"x-apikey": VT_API_KEY}
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"

    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        stats = data["data"]["attributes"]["last_analysis_stats"]
        print(f"""
Malicioso : {stats['malicious']}
Sospechoso: {stats['suspicious']}
Inofensivo: {stats['harmless']}
""")
    except:
        print("Error con VirusTotal (API o conexión)")
    pause()

# ================= MENÚ =================
def menu():
    while True:
        clear()
        header("ANALYZER TOOL")
        print(C_GREEN + f"Versión {VERSION}" + C_RESET)
        print("""
1) 🌐 Estado de red actual
2) 📌 Análisis técnico de IP
3) 📡 Resolver dominio
4) 🌐 IPv4 / IPv6
5) 🧩 Buscar subdominios
6) 📄 Información del sitio
7) 🔐 Generador de contraseñas
8) 🔗 Limpiar / revelar URL
9) 🛡️ VirusTotal IP check
0) ❌ Salir
""")
        op = input("Seleccione una opción: ").strip()

        if   op == "1": network_status()
        elif op == "2": analyze_ip()
        elif op == "3": resolve_dns()
        elif op == "4": domain_ips()
        elif op == "5": find_subdomains()
        elif op == "6": site_info()
        elif op == "7": password_generator()
        elif op == "8": clean_url()
        elif op == "9": virustotal_ip()
        elif op == "0": sys.exit()
        else:
            print("Opción inválida")
            pause()

if __name__ == "__main__":
    menu()