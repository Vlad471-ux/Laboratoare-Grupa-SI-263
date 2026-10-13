import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    # scot / de la inceput ca sa nu apara de doua ori
    if path.startswith("/"):
        path = path[1:]
    return "https://" + host + "/" + path


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    if url.startswith("https://"):
        return True
    else:
        return False


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    r = requests.get(url, timeout=5)
    print("Status:", r.status_code)
    print("Content-Type:", r.headers.get("Content-Type"))


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        r = requests.get(url, timeout=5)
    except:
        return {"status": None, "error": "site-ul nu raspunde"}

    rezultat = {}
    rezultat["status"] = r.status_code
    rezultat["content_type"] = r.headers.get("Content-Type")
    rezultat["length"] = len(r.content)
    rezultat["server"] = r.headers.get("Server", "unknown")
    return rezultat


def get_length(site):
    # folosita la sortare in scan_sites
    return site["length"]


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    rezultate = []
    for url in SITES:
        rez = check_site(url)
        rez["url"] = url
        rezultate.append(rez)

    bune = []
    for rez in rezultate:
        if rez["status"] == 200:
            bune.append(rez)

    bune.sort(key=get_length, reverse=True)

    for rez in bune:
        print(rez["url"], "->", rez["status"], ",", rez["length"], "octeti")

    print("Reusite:", len(bune), "| Esuate:", len(rezultate) - len(bune))


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        r = requests.get(url, timeout=5)
    except:
        return {"status": None, "error": "site-ul nu raspunde"}

    present = []
    missing = []
    for header in SECURITY_HEADERS:
        if header in r.headers:
            present.append(header)
        else:
            missing.append(header)

    score = len(present) * 25
    return {"present": present, "missing": missing, "score": score}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    status = None
    eroare = None
    incercari = 0

    for i in range(attempts):
        incercari = incercari + 1
        try:
            r = requests.get(url, timeout=5)
            status = r.status_code
            if status < 500:
                break
        except:
            eroare = "site-ul nu raspunde"

    if status == None:
        return {"status": None, "error": eroare, "attempts": incercari}
    return {"status": status, "attempts": incercari}
