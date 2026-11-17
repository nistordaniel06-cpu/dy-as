"""Generate the public catalog using the same CSV files as WooCommerce."""
import csv
import shutil
from pathlib import Path
from html import escape

def read_catalog(path):
    with open(path, newline='', encoding='utf-8-sig') as source:
        return list(csv.DictReader(source))

out = Path('public')
out.mkdir(exist_ok=True)
shutil.copy('dy-as/hero.webp', out / 'hero.webp')
products = read_catalog('catalog.csv')
tools = read_catalog('catalog-scule.csv')
cards = []
for item in products:
    if item['Type'] == 'variation':
        continue
    prices = [float(v['Regular price']) for v in products if v.get('Parent') == item['SKU']]
    price = ('de la ' if prices else '') + ('%.2f' % (min(prices) if prices else float(item['Regular price']))).replace('.', ',') + ' €'
    image = escape(item['Images'].split(',')[0].strip(), quote=True)
    cards.append(f'<article><img loading="lazy" src="{image}" alt=""><small>{escape(item["Categories"])}</small><h3>{escape(item["Name"])}</h3><p>{price}</p></article>')
coming = ''.join(f'<article><small>În pregătire</small><h3>{escape(i["Name"])}</h3><p>{escape(i["Short description"])}</p></article>' for i in tools)
page = """<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DY-AS | Catalog</title><style>
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:#241f1c;background:#faf9f6;font:16px/1.55 system-ui}header,main{max-width:1250px;margin:auto;padding:1rem 5%}header{display:flex;align-items:center;justify-content:space-between}b{font-size:1.35rem;letter-spacing:.12em}a{color:inherit}nav a{margin-left:1em}section{padding:2rem 0}.hero{background:linear-gradient(90deg,#15100cbd,transparent),url(hero.webp) center/cover;color:white;padding:clamp(4rem,10vw,8rem) 7%}h1,h2{font-family:Georgia,serif;font-weight:400;line-height:1.08}h1{font-size:clamp(3rem,7vw,6rem);max-width:9em;margin:.1em 0 .45em}h2{font-size:2.4rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,225px),1fr));gap:1rem}article{padding:1.1em;background:white;border:1px solid #e5e0d7}article img{width:100%;aspect-ratio:1;object-fit:contain}small{color:#685f53}h3{line-height:1.25;margin:.4em 0}footer{text-align:center;padding:2rem}</style><header><b>DY-AS</b><nav><a href="#scule">Scule</a><a href="#produse">Produse</a></nav></header><main><section class="hero"><h1>Ordinea, făcută frumos.</h1><a href="#produse">Descoperă catalogul ↓</a></section><section id="scule"><h2>Scule și unelte</h2><div class="grid">TOOLS</div></section><section id="produse"><h2>Colecția DY-AS</h2><p>Catalog de prezentare. Comenzile online se deschid la lansare.</p><div class="grid">CARDS</div></section></main><footer>DY-AS</footer></html>"""
(out / 'index.html').write_text(page.replace('TOOLS', coming).replace('CARDS', ''.join(cards)), encoding='utf-8')
