#!/usr/bin/env python3
# ============================================
# ANALYZER TOOL
# Autor: Cracke2
# Contacto: https://t.me/Cracke2
# Plataforma: Android / Termux
# ============================================

import os, sys, socket, requests, ipaddress, subprocess, random, json, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# ================= INSTALACIÓN AUTOMÁTICA =================
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])

try:
    from faker import Faker
    import pycountry
except ImportError:
    print("🔄 Instalando dependencias...")
    install_package("Faker")
    install_package("pycountry")
    from faker import Faker
    import pycountry
    print("✅ Dependencias instaladas")

# ================= VERSION =================
VERSION = "3.1"

# ================= COLORES =================
C_RESET  = "\033[0m"
C_GREEN  = "\033[92m"
C_RED    = "\033[91m"
C_YELLOW = "\033[93m"
C_CYAN   = "\033[96m"
C_BOLD   = "\033[1m"

# ================= IDIOMA =================
LANG = "ES"

TEXT = {
    "ES": {
        "menu": "Seleccione una opción",
        "press": "Presione ENTER para continuar...",
        "invalid": "Opción inválida",
        "again": "¿Generar nuevos datos? (S/N): "
    },
    "EN": {
        "menu": "Select an option",
        "press": "Press ENTER to continue...",
        "invalid": "Invalid option",
        "again": "Generate new data? (Y/N): "
    }
}

# ================= UTILIDADES =================
def clear():
    os.system("clear")

def pause():
    input(f"\n{TEXT[LANG]['press']}")

def header(title):
    print(C_CYAN + "=" * 70)
    print(C_BOLD + title)
    print("=" * 70 + C_RESET)

# ================= FUNCIONES DE RED =================
def network_status():
    clear()
    header("🌐 ESTADO DE RED ACTUAL")
    try:
        ip_public = requests.get("https://api.ipify.org", timeout=5).text
        data = requests.get("http://ip-api.com/json", timeout=8).json()
        print(f"""
IP Pública : {ip_public}
País       : {data.get('country')}
Ciudad     : {data.get('city')}
ISP        : {data.get('isp')}
ASN        : {data.get('as')}
""")
    except:
        print(C_RED + "Error obteniendo datos de red" + C_RESET)
    pause()

def analyze_ip():
    clear()
    header("📌 ANÁLISIS TÉCNICO DE IP")
    ip = input("IP objetivo: ").strip()
    try:
        ipaddress.ip_address(ip)
        data = requests.get(f"http://ip-api.com/json/{ip}", timeout=8).json()
        print(json.dumps(data, indent=2))
    except:
        print(C_RED + "IP inválida" + C_RESET)
    pause()

def resolve_dns():
    clear()
    header("📡 RESOLVER DOMINIO DNS")
    domain = input("Dominio: ").strip()
    try:
        _, _, ips = socket.gethostbyname_ex(domain)
        for ip in ips:
            print(" -", ip)
    except:
        print("No encontrado")
    pause()

def domain_ips():
    clear()
    header("🌐 IPv4 / IPv6")
    domain = input("Dominio: ").strip()
    try:
        for info in socket.getaddrinfo(domain, None):
            print(info[4][0])
    except:
        print("No encontrado")
    pause()

def find_subdomains():
    clear()
    header("🧩 BUSCAR SUBDOMINIOS")
    domain = input("Dominio: ").strip()
    prefixes = ["www", "api", "mail", "cdn", "static"]
    found = []
    for p in prefixes:
        try:
            socket.gethostbyname(f"{p}.{domain}")
            found.append(f"{p}.{domain}")
        except:
            pass
    if found:
        for f in found:
            print(" -", f)
    else:
        print("No encontrados")
    pause()

def site_info():
    clear()
    header("📄 INFORMACIÓN DEL SITIO")
    url = input("URL: ").strip()
    if not url.startswith("http"):
        url = "http://" + url
    try:
        r = requests.get(url, timeout=8)
        print(f"""
URL        : {r.url}
Servidor   : {r.headers.get('Server')}
Tipo       : {r.headers.get('Content-Type')}
Tamaño     : {len(r.content)/1024:.2f} KB
""")
    except:
        print("No responde")
    pause()

def curl_tool():
    clear()
    header("🧰 CURL / HEADERS")
    url = input("URL: ").strip()
    os.system(f"curl -I {url}")
    pause()

# ================= UPDATE TOOL =================
def update_tool():
    clear()
    header("🔄 ACTUALIZAR HERRAMIENTA")
    try:
        subprocess.run(["git", "pull"], check=True)
        print(C_GREEN + "\n✔ Herramienta actualizada correctamente" + C_RESET)
    except:
        print(C_RED + "\n✖ Error al actualizar (¿es un repo git?)" + C_RESET)
    pause()

# ================= FAKE DATA =================
EMAIL_DOMAINS = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com"]

def generate_fake_data(country_name):
    try:
        country = pycountry.countries.search_fuzzy(country_name)[0]
        locale = country.alpha_2
    except:
        locale = "DEFAULT"

    fake = Faker()
    name = fake.name()
    email = f"{name.replace(' ','').lower()}{random.randint(10,999)}@{random.choice(EMAIL_DOMAINS)}"

    return {
        "name": name,
        "street": fake.street_address(),
        "city": fake.city(),
        "state": fake.state(),
        "postal": fake.postcode(),
        "country": country_name.title(),
        "email": email
    }

def fake_generator():
    clear()
    header("🏠 FAKE ADDRESS GENERATOR")
    while True:
        country = input("Nombre del país: ").strip()
        if not country:
            print(C_RED + "País inválido" + C_RESET)
            pause()
            return
        count = int(input("Cantidad a generar: ") or "1")
        clear()
        header(f"📍 Address For {country.title()}")
        for _ in range(count):
            d = generate_fake_data(country)
            print(f"""
━━━━━━━━━━━━━━━━━━━
Name        : {d['name']}
Street      : {d['street']}
City        : {d['city']}
State       : {d['state']}
Postal Code : {d['postal']}
Country     : {d['country']}
Email       : {d['email']}
━━━━━━━━━━━━━━━━━━━
""")
        again = input(TEXT[LANG]["again"]).lower()
        if again not in ("s", "y"):
            break

# ================= API LOCAL =================
class LocalAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != "/fake":
            self.send_response(404); self.end_headers(); return
        params = parse_qs(parsed.query)
        country = params.get("country", [None])[0]
        count = int(params.get("count", [1])[0])
        data = [generate_fake_data(country) for _ in range(min(count, 50))]
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

def start_api():
    threading.Thread(
        target=lambda: HTTPServer(("127.0.0.1", 5050), LocalAPI).serve_forever(),
        daemon=True
    ).start()

# ================= MENÚ =================
def menu():
    start_api()
    while True:
        clear()
        header("ANALYZER TOOL")
        print(C_GREEN + f"Versión {VERSION} • ✔ Activo • API Local 127.0.0.1:5050" + C_RESET)
        print("""
1) 🌐 Estado de red actual
2) 📌 Análisis técnico de IP
3) 📡 Resolver dominio DNS
4) 🌐 IPv4 / IPv6
5) 🧩 Buscar subdominios
6) 📄 Información del sitio
7) 🧰 Curl / Headers
8) 🏠 Fake Address Generator
9) 🔄 Actualizar herramienta
0) ❌ Salir
""")
        op = input(f"{TEXT[LANG]['menu']}: ").strip()
        if   op == "1": network_status()
        elif op == "2": analyze_ip()
        elif op == "3": resolve_dns()
        elif op == "4": domain_ips()
        elif op == "5": find_subdomains()
        elif op == "6": site_info()
        elif op == "7": curl_tool()
        elif op == "8": fake_generator()
        elif op == "9": update_tool()
        elif op == "0": sys.exit()
        else:
            print(TEXT[LANG]["invalid"])
            pause()

if __name__ == "__main__":
    menu()