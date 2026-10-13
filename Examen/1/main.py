from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check
from checker import SITES

# Partea 1: apeluri pentru build_url și is_https
print("Partea 1, build_url:", build_url("example.com", "login"))
print("Partea 1, build_url cu /:", build_url("example.com", "/login"))
print("Partea 1, is_https:", is_https("https://example.com"))
print("Partea 1, is_https cu http:", is_https("http://example.com"))

# Partea 2: apeluri pentru show_response
print()
print("Partea 2, show_response:")
show_response("https://example.com")
# nu merge pe un site care nu exista, programul se opreste cu eroare,
# de aceea am lasat apelul comentat
# show_response("http://this-site-does-not-exist.invalid")

# Partea 3: apeluri pentru check_site
print()
print("Partea 3, check_site:")
for url in SITES:
    print(url, check_site(url))

# Partea 4: apelul scan_sites()
print()
print("Partea 4, scan_sites:")
scan_sites()

# Partea 5: apeluri pentru check_headers
print()
print("Partea 5, check_headers:", check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print("Partea 5, check_headers litere mici:", check_headers("https://httpbin.org/response-headers?x-frame-options=DENY"))
print("Partea 5, check_headers fara antete:", check_headers("https://httpbin.org/html"))
print("Partea 5, check_headers site inexistent:", check_headers("http://this-site-does-not-exist.invalid"))

# Partea 6: apeluri pentru retry_check
print()
print("Partea 6, retry_check 200:", retry_check("https://httpbin.org/status/200"))
print("Partea 6, retry_check 404:", retry_check("https://httpbin.org/status/404"))
print("Partea 6, retry_check 500:", retry_check("https://httpbin.org/status/500"))
print("Partea 6, retry_check 500 cu 2 incercari:", retry_check("https://httpbin.org/status/500", attempts=2))
print("Partea 6, retry_check site inexistent:", retry_check("http://this-site-does-not-exist.invalid"))
