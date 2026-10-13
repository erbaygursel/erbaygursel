"""Fikstür HTML'lerinde iki takım adını içeren /mac/ linklerini bulur. Kullanım: mac_bul.py <takım1> <takım2> <html>..."""
import html, re, sys, urllib.parse
a, b = sys.argv[1].lower(), sys.argv[2].lower()
bulunan = {}
for yol in sys.argv[3:]:
    t = open(yol, encoding='utf-8', errors='replace').read()
    for href in re.findall(r'href="([^"]*/mac/[^"]+)"', t):
        h = html.unescape(href)
        cozuk = urllib.parse.unquote(h).lower()
        if a in cozuk and b in cozuk and '/karsilastirma' not in cozuk:
            m = re.search(r'/mac/([^/]+)/(?:iddaa/)?([a-z0-9]{20,})', h)
            if m:
                bulunan[m.group(2)] = m.group(1)
for mid, slug in bulunan.items():
    print(f'{slug} {mid}')
