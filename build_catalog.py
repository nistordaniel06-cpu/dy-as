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

categories = {'Home & Organization':'Casă', 'Desk & Tech':'Birou', 'Travel & Car':'Călătorii', 'Beauty & Rituals':'Îngrijire', 'Gifts':'Cadouri'}
names = {'Jasmine & Sweet Orange Soap':'Săpun cu iasomie și portocală', 'Rechargeable Bike Light Set, Front & Rear':'Set de lumini pentru bicicletă', 'Rich Night Cream, Green Tea & Rosehip':'Cremă de noapte cu ceai verde și măceșe', 'Bladeless Mini Fan, Rechargeable':'Mini ventilator fără pale', 'Coffee Steel Ring Set, Amethyst Crystal':'Set de inele cu ametist', 'Magnetic Case for iPhone 17 Pro Max':'Husă magnetică pentru iPhone 17 Pro Max', 'Mini Aroma Diffuser & Humidifier':'Mini difuzor de aromă', 'Handwriting Bracelet, Personalised':'Brățară personalizată', 'Salt Lake Flatware Set, 10 Pieces':'Set de tacâmuri Salt Lake', 'Wireless CarPlay Adapter, 2-in-1':'Adaptor CarPlay wireless 2 în 1'}
cards = []
for item in products:
    if item['Type'] == 'variation':
        continue
    prices = [float(v['Regular price']) for v in products if v.get('Parent') == item['SKU']]
    price = ('de la ' if prices else '') + ('%.2f' % (min(prices) if prices else float(item['Regular price']))).replace('.', ',') + ' €'
    photo = escape(item['Images'].split(',')[0].strip(), quote=True)
    category = escape(categories.get(item['Categories'],item['Categories']))
    name = escape(names.get(item['Name'],item['Name']))
    cards.append(f'<article data-cat="{category}"><div class="photo"><img loading="lazy" src="{photo}" alt="{name}"></div><small>{category}</small><h3>{name}</h3><p>{price}</p></article>')
buttons = ''.join(f'<button aria-pressed="false">{c}</button>' for c in categories.values())
coming = ''.join(f'<article class="tool"><small>În pregătire</small><h3>{escape(i["Name"])}</h3><p>{escape(i["Short description"])}</p></article>' for i in tools)
page = """<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#111110"><title>DY-AS · Obiecte pentru cotidian</title><style>
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:1rem}body{margin:0;background:#111110;color:#f4f0e9;font:16px/1.45 system-ui,sans-serif}.wrap{max-width:1400px;margin:auto;padding:0 clamp(18px,5vw,80px)}header,footer,.line{display:flex;align-items:center;justify-content:space-between}header{height:76px;border-bottom:1px solid #33332f}a{color:inherit;text-decoration:none}header nav{display:flex;gap:1.3rem;font-size:.88rem}.brand{font:600 30px/1 Georgia,serif;letter-spacing:-2px}.hero{position:relative;isolation:isolate;overflow:hidden;min-height:400px;display:flex;align-items:center;margin-top:20px;border-radius:18px;background:#181510}.hero:before{content:"";position:absolute;inset:0 0 0 24%;background:url(hero.webp) right center/cover no-repeat;z-index:-2}.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#171410 25%,#171410fc 39%,transparent 70%);z-index:-1}.intro{padding:clamp(24px,5vw,70px)}h1,h2{font:normal clamp(38px,5vw,76px)/1.01 Georgia,serif;letter-spacing:-.052em;margin:0}h1 em{font-weight:normal;color:#e5cbb0}.cta{display:inline-flex;background:#f3eee7;color:#211e1a;border-radius:99px;padding:13px 22px;margin-top:26px;font-weight:600;font-size:14px;gap:18px}section{margin:55px 0}h2{font-size:clamp(34px,4vw,55px)}.filters{display:flex;overflow-x:auto;gap:7px;margin:20px 0 25px;scrollbar-width:thin}.filters button{white-space:nowrap;background:transparent;color:#dfdcd6;border:1px solid #4a4845;border-radius:30px;padding:10px 17px;cursor:pointer;font:inherit;font-size:14px}.filters button[aria-pressed=true]{background:#f1ece3;color:#27241f;border-color:transparent}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:32px 16px}.photo{background:#e9e7e3;border-radius:12px;overflow:hidden;aspect-ratio:1.12}.photo img{width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply}.grid small,.tool small{display:block;color:#c7ae90;font-size:11px;text-transform:uppercase;letter-spacing:.12em;margin-top:12px}h3{font-size:clamp(15px,1.5vw,21px);font-weight:550;line-height:1.25;margin:5px 0}p{margin:6px 0;color:#d4cfc6;font-size:14px}.tools{border-top:1px solid #393733;padding-top:32px}.tool-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:20px}.tool{background:#23211e;border-radius:14px;padding:20px}.tool small{margin:0 0 14px}footer{border-top:1px solid #383632;padding:24px 0;gap:20px}footer p{max-width:30em}button:focus-visible,a:focus-visible{outline:3px solid #edbb79;outline-offset:2px}
@media(max-width:700px){header{height:60px}.hero{min-height:370px;align-items:end;margin-top:12px}.hero:before{inset:0;background-size:auto 85%;background-position:88% top}.hero:after{background:linear-gradient(0deg,#181510 6%,#181510e8 25%,transparent 68%),linear-gradient(90deg,#18151070,transparent 50%)}.intro{padding:24px}h1{font-size:44px}.cta{margin-top:15px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:24px 12px}.tool-grid{grid-template-columns:1fr}section{margin:35px 0}.filters{margin:15px 0}.brand{font-size:26px}footer{align-items:flex-start}footer p{font-size:12px;max-width:19em}}
</style></head><body><div class="wrap"><header><a class="brand" href="./">DY-AS</a><nav><a href="#colectie">Colecție</a><a href="#scule">Scule și unelte</a></nav></header><main><div class="hero"><div class="intro"><h1>Ordinea,<br><em>făcută frumos.</em></h1><a class="cta" href="#colectie">Explorează colecția <span aria-hidden="true">↘</span></a></div></div><section id="colectie"><h2>Colecția DY-AS</h2><div class="filters" role="group" aria-label="Categorii"><button aria-pressed="true">Toate</button>FILTERS</div><div class="grid">CARDS</div></section><section id="scule" class="tools"><h2>Scule și unelte</h2><div class="tool-grid">TOOLS</div></section></main><footer><b class="brand">DY-AS</b><p>Catalog de prezentare. Comenzile online se deschid la lansare.</p></footer></div><script>document.querySelector('.filters').addEventListener('click',e=>{if(!e.target.matches('button'))return;const category=e.target.textContent;document.querySelectorAll('.filters button').forEach(b=>b.setAttribute('aria-pressed',String(b===e.target)));document.querySelectorAll('[data-cat]').forEach(card=>card.hidden=category!=='Toate'&&card.dataset.cat!==category)})</script></body></html>"""
(out / 'index.html').write_text(page.replace('FILTERS',buttons).replace('TOOLS',coming).replace('CARDS',''.join(cards)),encoding='utf-8')
