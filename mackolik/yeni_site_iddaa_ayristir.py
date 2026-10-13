"""Yeni mackolik.com maç İddaa sayfasını ayrıştırır (ayrıntı: YENI_VERI_KAYNAGI.md).

  python3 yeni_site_iddaa_ayristir.py <maç_iddaa_sayfası.html>

Sayfa adresi: https://www.mackolik.com/mac/<slug>/iddaa/<macId>  (curl + mobil User-Agent yeterli)
Her market iki kez gelir: data-shortcode="0.x" = oley.com oranı (ATLANIR), diğer önekler = İddaa oranı.
"""
import html
import re
import sys


def ayristir(t):
    """[(market_adı, [(seçenek, oran_metni), ...])] — yalnızca İddaa seti."""
    out = []
    for it in re.split(r'<li class="widget-iddaa-markets__market-item"', t)[1:]:
        n = re.search(r'header-text">\s*([^<]+?)\s*<', it)
        opts = re.findall(r'data-shortcode="([1-9]\d*)\.\d+"[^>]*>\s*<span[^>]*>\s*([^<]+?)\s*</span>\s*<span[^>]*>\s*([^<]+?)\s*</span>', it)
        if n and opts:
            out.append((html.unescape(n.group(1)), [(a, b) for _, a, b in opts]))
    return out


if __name__ == '__main__':
    t = open(sys.argv[1], encoding='utf-8').read()
    title = re.search(r'<title>([^<]+)', t)
    idd = ayristir(t)
    print(html.unescape(title.group(1)) if title else '', '| İddaa marketi:', len(idd))
    for n, o in idd:
        print(f'  {n}: ' + ' | '.join(f'{a} {b}' for a, b in o))
