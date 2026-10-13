"""Ham sayfada tüm market başlıklarını (oley dahil) ve KG/yarı ile ilgili geçen metinleri listeler."""
import html, re, sys, collections
t = open(sys.argv[1], encoding='utf-8').read()
bloklar = re.split(r'<li class="widget-iddaa-markets__market-item"', t)[1:]
print('Toplam market bloğu:', len(bloklar))
say = collections.Counter()
for b in bloklar:
    n = re.search(r'header-text">\s*([^<]+?)\s*<', b)
    on = re.findall(r'data-shortcode="(\d+)\.', b)
    kume = 'oley' if on and all(x == '0' for x in on) else ('iddaa' if on else 'kodsuz')
    ad = html.unescape(n.group(1)) if n else '?'
    say[kume] += 1
    print(f'  [{kume}] {ad}')
print(say)
print('--- anahtar kelime geçişleri (benzersiz) ---')
duz = html.unescape(re.sub(r'<[^>]+>', ' ', t))
for k in ['Karşılıklı', 'KG', '2. Yarı', 'İkinci Yarı', 'Evet/Evet', 'Her İki Yarı', 'İki Yarı']:
    bul = sorted(set(m.strip() for m in re.findall(r'[^\n]{0,40}' + re.escape(k) + r'[^\n]{0,40}', duz)))
    print(k, len(bul)); [print('   ', re.sub(r'\s+', ' ', x)) for x in bul[:15]]
print('nesine code:', sorted(set(re.findall(r'code=(\d+)', t))))
