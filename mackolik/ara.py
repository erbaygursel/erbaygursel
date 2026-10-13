"""Ham dosyada (etiket/JSON/script dahil) '1. Yarı / 2. Yarı Karşılıklı Gol' benzeri ifadeleri arar."""
import html, re, sys, codecs
for yol in sys.argv[1:]:
    ham = open(yol, encoding='utf-8', errors='replace').read()
    # \uXXXX kaçışlarını da çöz
    try:
        cozuk = codecs.decode(ham.replace('\\/', '/'), 'unicode_escape').encode('latin-1', 'replace').decode('utf-8', 'replace')
    except Exception:
        cozuk = ham
    for ad, t in [('ham', ham), ('kacis-cozulmus', cozuk), ('entity-cozulmus', html.unescape(ham))]:
        print(f'=== {yol} [{ad}] ===')
        kaliplar = [
            r'1\.?\s*Yar[ıi]\s*/\s*2\.?\s*Yar[ıi]',
            r'Yar[ıi]\s*/\s*2',
            r'2\.?\s*Yar[ıi]\s*Kar[şs][ıi]l[ıi]kl[ıi]',
            r'Kar[şs][ıi]l[ıi]kl[ıi]\s*Gol',
            r'(?i)iy\s*/\s*2y|iy-2y|1y\s*/\s*2y',
            r'(?i)evet\s*/\s*evet',
            r'(?i)halves|both.?halves',
        ]
        for k in kaliplar:
            m = list(re.finditer(k, t))
            print(f'  {k!r}: {len(m)}')
            for x in {re.sub(r"\s+", " ", t[max(0, x.start()-80):x.end()+80]) for x in m[:200]} if len(m) < 60 else []:
                if 'Karşılıklı Gol' in k or 'Kar' in k:
                    continue
                print('     ...', x)
        # Karşılıklı Gol geçen tüm farklı başlık/etiket metinleri
        adlar = sorted(set(re.sub(r'\s+', ' ', a) for a in re.findall(r'[>"\'][^<>"\']{0,60}Kar[şs][ıi]l[ıi]kl[ıi][^<>"\']{0,40}[<"\']', t)))
        print('  Karşılıklı geçen farklı metinler:', len(adlar))
        for a in adlar[:40]:
            print('     ', a)
