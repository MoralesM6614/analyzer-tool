#!/usr/bin/env python3
# ============================================
# ANALYZER TOOL
# Autor: Cracke2
# Contacto: https://t.me/Cracke2
# Plataforma: Android / Termux
# ============================================

import os, sys, socket, requests, ipaddress, subprocess, random

# ================= VERSION =================
VERSION = "1.0"

# ================= COLORES =================
C_RESET="\033[0m"; C_GREEN="\033[92m"; C_RED="\033[91m"
C_YELLOW="\033[93m"; C_CYAN="\033[96m"; C_BOLD="\033[1m"

# ================= UTIL =================
def clear(): os.system("clear")
def pause(): input("\nPresione ENTER para continuar...")

def header(t):
    print(C_CYAN + "="*70)
    print(C_BOLD + t)
    print("="*70 + C_RESET)

# ================= NETWORK =================
def network_status():
    clear(); header("🌐 ESTADO DE RED ACTUAL")
    try:
        ip_pub = requests.get("https://api.ipify.org",timeout=5).text
        d = requests.get("http://ip-api.com/json/?fields=country,countryCode,city,zip,isp,as,proxy,hosting",timeout=8).json()
        net = "VPN / Proxy" if d.get("proxy") or d.get("hosting") else "Red residencial"
        print(f"""
IP pública : {ip_pub}
País       : {d.get('country')} [{d.get('countryCode')}]
Ciudad     : {d.get('city')}
ZIP        : {d.get('zip')}
ISP        : {d.get('isp')}
ASN        : {d.get('as')}
Tipo       : {net}
""")
    except:
        print(C_RED+"Error de red"+C_RESET)
    pause()

# ================= IP ANALYSIS =================
def analyze_ip():
    clear(); header("📌 ANÁLISIS TÉCNICO DE IP")
    ip=input("IP objetivo: ").strip()
    try: ipaddress.ip_address(ip)
    except: print("IP inválida"); pause(); return
    d=requests.get(f"http://ip-api.com/json/{ip}",timeout=8).json()
    print(f"""
IP        : {ip}
País      : {d.get('country')} [{d.get('countryCode')}]
Región    : {d.get('regionName')}
Ciudad    : {d.get('city')}
ZIP       : {d.get('zip')}
Lat/Lon   : {d.get('lat')}, {d.get('lon')}
ISP       : {d.get('isp')}
ASN       : {d.get('as')}
""")
    pause()

# ================= DNS =================
def resolve_dns():
    clear(); header("📡 RESOLVER DNS")
    d=input("Dominio: ").strip()
    try:
        for i in socket.gethostbyname_ex(d)[2]: print("-",i)
    except: print("No encontrados")
    pause()

# ================= IPs =================
def domain_ips():
    clear(); header("🌐 IPv4 / IPv6")
    d=input("Dominio: ").strip()
    v4,v6=set(),set()
    try:
        for i in socket.getaddrinfo(d,None):
            (v4 if i[0]==socket.AF_INET else v6).add(i[4][0])
        print("IPv4:"); [print(" ",x) for x in v4]
        print("\nIPv6:"); [print(" ",x) for x in v6]
    except: print("No encontrados")
    pause()

# ================= SUBDOMAINS =================
def find_subdomains():
    clear(); header("🧩 SUBDOMINIOS")
    d=input("Dominio: ").strip()
    pref=["www","api","mail","m","cdn","static"]
    f=[]
    for p in pref:
        try: socket.gethostbyname(f"{p}.{d}"); f.append(f"{p}.{d}")
        except: pass
    if f:
        for s in f: print("-",s)
    else: print("No encontrados")
    pause()

# ================= SITE INFO =================
def site_info():
    clear(); header("📄 INFO DEL SITIO")
    u=input("URL: ").strip()
    if not u.startswith("http"): u="http://"+u
    try:
        r=requests.get(u,timeout=8)
        t="N/A"
        if "<title>" in r.text.lower():
            t=r.text.lower().split("<title>")[1].split("</title>")[0]
        print(f"""
URL      : {r.url}
Título   : {t}
Servidor : {r.headers.get('Server')}
Tipo     : {r.headers.get('Content-Type')}
""")
    except: print("No responde")
    pause()

# ================= CURL =================
def curl_tool():
    clear(); header("🧰 CURL")
    u=input("URL: ").strip()
    os.system(f"curl -I {u}")
    pause()

# ================= CPF / CEP =================
def gerar_cpf():
    n=[random.randint(0,9) for _ in range(9)]
    def d(x): r=(sum(v*(len(x)+1-i) for i,v in enumerate(x))*10)%11; return 0 if r==10 else r
    n.append(d(n)); n.append(d(n))
    return f"{n[0]}{n[1]}{n[2]}.{n[3]}{n[4]}{n[5]}.{n[6]}{n[7]}{n[8]}-{n[9]}{n[10]}"

def gerar_cep(): return f"{random.randint(10000,99999)}-{random.randint(100,999)}"

# ================= FAKE ADDRESS =================
def fake_address():
    clear(); header("🏠 FAKE ADDRESS GENERATOR")
    c=input("Código país (br,co,ar,cl,mx,us,uk,de,in): ").lower()

    data={
        "br":{"name":["João","Lucas","Marcos"],"ln":["Silva","Pereira"],"city":"São Paulo"},
        "co":{"name":["Juan","Carlos"],"ln":["Gómez","Pérez"],"city":"Bogotá"},
        "ar":{"name":["Mateo","Lucas"],"ln":["Gómez","Fernández"],"city":"Buenos Aires"},
        "cl":{"name":["Diego","Sebastián"],"ln":["Rojas","Muñoz"],"city":"Santiago"},
        "mx":{"name":["Luis","Jorge"],"ln":["Hernández","López"],"city":"CDMX"},
        "us":{"name":["John","Michael"],"ln":["Smith","Brown"],"city":"New York"},
        "uk":{"name":["Oliver","Harry"],"ln":["Wilson","Taylor"],"city":"London"},
        "de":{"name":["Lukas","Leon"],"ln":["Müller","Schmidt"],"city":"Berlin"},
        "in":{"name":["Rahul","Amit"],"ln":["Sharma","Patel"],"city":"Mumbai"},
    }

    if c not in data:
        print("País no soportado"); pause(); return

    d=data[c]
    fn=random.choice(d["name"]); ln=random.choice(d["ln"])
    street=f"{random.randint(10,999)} Main Street"

    print(f"""
Nombre     : {fn} {ln}
Dirección  : {street}
Ciudad     : {d['city']}
País       : {c.upper()}
""")

    if c=="br":
        print(f"CPF        : {gerar_cpf()}")
        print(f"CEP        : {gerar_cep()}")

    pause()

# ================= MENU =================
def menu():
    while True:
        clear()
        header("ANALYZER TOOL")
        print(f"Versión {VERSION} • Cracke2 • https://t.me/Cracke2\n")
        print("""
1) 🌐 Estado de red
2) 📌 Análisis IP
3) 📡 DNS
4) 🌐 IPv4 / IPv6
5) 🧩 Subdominios
6) 📄 Info sitio
7) 🧰 Curl
8) 🏠 Fake Address Generator
0) ❌ Salir
""")
        o=input("Seleccione una opción: ").strip()
        if o=="1": network_status()
        elif o=="2": analyze_ip()
        elif o=="3": resolve_dns()
        elif o=="4": domain_ips()
        elif o=="5": find_subdomains()
        elif o=="6": site_info()
        elif o=="7": curl_tool()
        elif o=="8": fake_address()
        elif o=="0": sys.exit()
        else: print("Opción inválida"); pause()

if __name__=="__main__":
    menu()