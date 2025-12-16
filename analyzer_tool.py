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

# ================= VERSION =================
VERSION = "3.0"

# ================= COLORES =================
C_RESET  = "\033[0m"
C_GREEN  = "\033[92m"
C_RED    = "\033[91m"
C_YELLOW = "\033[93m"
C_BLUE   = "\033[94m"
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
def clear(): os.system("clear")
def pause(): input(f"\n{TEXT[LANG]['press']}")

def header(title):
    print(C_CYAN + "=" * 70)
    print(C_BOLD + title)
    print("=" * 70 + C_RESET)

# ================= FAKE DATA =================
DOMAINS = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com"]

COUNTRIES = {
    "us": {"name": "United States", "cities": ["New York","Chicago","Philadelphia"], "states": ["NY","PA","CA"], "zip": lambda: str(random.randint(10000,99999))},
    "co": {"name": "Colombia", "cities": ["Bogotá","Medellín","Cali"], "states": ["Cundinamarca","Antioquia"], "zip": lambda: str(random.randint(110000,999999))},
    "br": {"name": "Brazil", "cities": ["São Paulo","Rio de Janeiro"], "states": ["SP","RJ"], "zip": lambda: f"{random.randint(10000,99999)}-{random.randint(100,999)}"},
    "ar": {"name": "Argentina", "cities": ["Buenos Aires","Córdoba"], "states": ["BA","CBA"], "zip": lambda: str(random.randint(1000,9999))},
    "cl": {"name": "Chile", "cities": ["Santiago","Valparaíso"], "states": ["RM","V"], "zip": lambda: str(random.randint(1000000,9999999))},
    "in": {"name": "India", "cities": ["Delhi","Mumbai","Bangalore"], "states": ["Delhi","MH","KA"], "zip": lambda: str(random.randint(100000,999999))},
    "uk": {"name": "United Kingdom", "cities": ["London","Manchester"], "states": ["England"], "zip": lambda: "SW1A " + str(random.randint(1,9)) + "AA"},
    "de": {"name": "Germany", "cities": ["Berlin","Munich"], "states": ["BE","BY"], "zip": lambda: str(random.randint(10000,99999))}
}

NAMES = ["Lucas","Mateo","Juan","Carlos","Ana","Maria","Sofia","Laura","Daniel","Pedro"]
LASTNAMES = ["Walker","Gomez","Perez","Silva","Rodriguez","Lopez","Fernandez","Muller","Schmidt"]

def generate_fake_data(code):
    c = COUNTRIES[code]
    name = f"{random.choice(NAMES)} {random.choice(LASTNAMES)}"
    email = f"{name.replace(' ','').lower()}{random.randint(10,999)}@{random.choice(DOMAINS)}"
    return {
        "name": name,
        "street": f"{random.randint(1,9999)} {random.choice(['Main','Market','Oak','Pine'])} Street",
        "city": random.choice(c["cities"]),
        "state": random.choice(c["states"]),
        "postal_code": c["zip"](),
        "country": c["name"],
        "email": email
    }

# ================= FAKE GENERATOR MENU =================
def fake_generator():
    clear()
    header("🏠 FAKE ADDRESS GENERATOR")

    while True:
        code = input("País (us, co, br, in, uk, de, ar, cl): ").lower().strip()
        if code not in COUNTRIES:
            print(C_RED + "País no soportado" + C_RESET)
            pause()
            return

        try:
            count = int(input("Cantidad a generar: "))
        except:
            count = 1

        clear()
        header(f"📍 Address For {COUNTRIES[code]['name']}")

        for i in range(count):
            d = generate_fake_data(code)
            print(f"""
━━━━━━━━━━━━━━━━━━━
Name        : {d['name']}
Street      : {d['street']}
City        : {d['city']}
State       : {d['state']}
Postal Code : {d['postal_code']}
Country     : {d['country']}
Email       : {d['email']}
━━━━━━━━━━━━━━━━━━━
""")

        again = input(TEXT[LANG]["again"]).lower()
        if again not in ("s","y"):
            break

# ================= API LOCAL =================
class LocalAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != "/fake":
            self.send_response(404); self.end_headers(); return

        params = parse_qs(parsed.query)
        country = params.get("country",[None])[0]
        count = int(params.get("count",[1])[0])

        if country not in COUNTRIES:
            self.send_response(400); self.end_headers()
            self.wfile.write(b"Invalid country")
            return

        data = [generate_fake_data(country) for _ in range(min(count,50))]

        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data,indent=2).encode())

def start_api():
    def run():
        HTTPServer(("127.0.0.1",5050),LocalAPI).serve_forever()
    threading.Thread(target=run,daemon=True).start()

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
0) ❌ Salir
""")

        op = input(f"{TEXT[LANG]['menu']}: ").strip()

        if op == "8": fake_generator()
        elif op == "0": sys.exit()
        else:
            print(TEXT[LANG]["invalid"])
            pause()

if __name__ == "__main__":
    menu()