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
shutil.copytree('storefront/media', out / 'media', dirs_exist_ok=True)
products = read_catalog('catalog.csv')
tools = read_catalog('catalog-scule.csv')

categories = {'Home & Organization':'Casă', 'Desk & Tech':'Birou', 'Travel & Car':'Călătorii', 'Beauty & Rituals':'Îngrijire', 'Gifts':'Cadouri'}
names = {'Jasmine & Sweet Orange Soap':'Săpun cu iasomie și portocală', 'Rechargeable Bike Light Set, Front & Rear':'Set de lumini pentru bicicletă', 'Rich Night Cream, Green Tea & Rosehip':'Cremă de noapte cu ceai verde și măceșe', 'Bladeless Mini Fan, Rechargeable':'Mini ventilator fără pale', 'Coffee Steel Ring Set, Amethyst Crystal':'Set de inele cu ametist', 'Magnetic Case for iPhone 17 Pro Max':'Husă magnetică pentru iPhone 17 Pro Max', 'Mini Aroma Diffuser & Humidifier':'Mini difuzor de aromă', 'Handwriting Bracelet, Personalised':'Brățară personalizată', 'Salt Lake Flatware Set, 10 Pieces':'Set de tacâmuri Salt Lake', 'Wireless CarPlay Adapter, 2-in-1':'Adaptor CarPlay wireless 2 în 1'}

def make_card(category, name, note, image=''):
    category, name, note = map(escape, (category, name, note))
    if image:
        media = f'<div class="photo"><img src="{escape(image, quote=True)}" loading="lazy" alt=""></div>'
    else:
        media = ''
    return f'<article class="card" data-category="{category}">{media}<small>{category}</small><h3>{name}</h3><p>{note}</p></article>'

catalog = []
for item in products:
    if item['Type'] == 'variation':
        continue
    variants = [float(row['Regular price']) for row in products if row.get('Parent') == item['SKU']]
    price = min(variants) if variants else float(item['Regular price'])
    price_label = ('de la ' if variants else '') + f'{price:.2f}'.replace('.', ',') + ' €'
    category = categories.get(item['Categories'], item['Categories'])
    name = names.get(item['Name'], item['Name'])
    card = make_card(category, name, price_label, (f"media/{item['SKU']}.webp" if (out / 'media' / f"{item['SKU']}.webp").is_file() else item['Images'].split(',')[0].strip()))
    catalog.append((list(categories.values()).index(category) if category in categories.values() else 99, card))

cards = ''.join(card for _, card in sorted(catalog, key=lambda pair: pair[0]))
tools_html = ''.join(make_card('Scule și unelte', item['Name'], item['Short description'], f"media/{item['SKU']}.webp" if (out / 'media' / f"{item['SKU']}.webp").is_file() else '') for item in tools)
page = (Path('storefront') / 'index.html').read_text(encoding='utf-8')
page = page.replace('<!-- PRODUCT_CARDS -->', cards).replace('<!-- TOOL_CARDS -->', tools_html)
(out / 'index.html').write_text(page, encoding='utf-8')
