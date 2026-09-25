from flask import Flask, render_template, jsonify
import re
import os
import time
from datetime import datetime, timedelta, timezone
import requests

app = Flask(__name__)

BR_WHATSAPP = "5513988817584"
BR_PLANS = [
    ("15 dias", "R$ 10,00", "R$ 15,00"),
    ("Mensal", "R$ 24,99", "R$ 29,99"),
    ("Trimestral", "R$ 39,99", "R$ 54,99"),
    ("Semestral", "R$ 59,99", "R$ 79,99"),
    ("Anual", "R$ 129,99", "R$ 159,99"),
]
BR_MULTI = {
    "Mensal": ("R$ 30,00", "R$ 30,00"),
    "Trimestral": ("R$ 49,99", "R$ 64,99"),
    "Semestral": ("R$ 69,99", "R$ 89,99"),
    "Anual": ("R$ 139,99", "R$ 169,99"),
}

CATALOG_CACHE = {"timestamp": 0, "data": None}
CATALOG_TTL = 30 * 60  # refresh every 30 minutes


def _wikidata_movies():
    """Recent/upcoming films with poster artwork from Wikidata/Wikimedia Commons."""
    today = datetime.now(timezone.utc).date()
    start = today - timedelta(days=120)
    end = today + timedelta(days=60)
    query = f"""
    SELECT ?item ?itemLabel ?date ?image WHERE {{
      ?item wdt:P31/wdt:P279* wd:Q11424;
            wdt:P577 ?date;
            wdt:P18 ?image.
      FILTER(?date >= "{start}T00:00:00Z"^^xsd:dateTime)
      FILTER(?date <= "{end}T23:59:59Z"^^xsd:dateTime)
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    ORDER BY DESC(?date)
    LIMIT 24
    """
    r = requests.get(
        "https://query.wikidata.org/sparql",
        params={"query": query, "format": "json"},
        headers={"User-Agent": "NexPlay-TV-BR/1.0 (catalog metadata)", "Accept": "application/sparql-results+json"},
        timeout=18,
    )
    r.raise_for_status()
    rows = r.json().get("results", {}).get("bindings", [])
    out = []
    seen = set()
    for row in rows:
        title = row.get("itemLabel", {}).get("value", "").strip()
        image = row.get("image", {}).get("value", "").strip()
        date = row.get("date", {}).get("value", "")[:10]
        item = row.get("item", {}).get("value", "")
        if not title or not image or title in seen:
            continue
        seen.add(title)
        if image.startswith("http://"):
            image = "https://" + image[7:]
        out.append({
            "title": title,
            "year": date[:4] if date else "",
            "date": date,
            "image": image,
            "type": "movie",
            "source": "Wikidata / Wikimedia Commons",
            "source_url": item,
        })
    return out[:12]


def _tvmaze_series():
    """Series airing in the US over the next few days, with TVmaze artwork."""
    today = datetime.now(timezone.utc).date()
    shows = {}
    for offset in range(3):
        date = today + timedelta(days=offset)
        try:
            r = requests.get(
                "https://api.tvmaze.com/schedule",
                params={"country": "US", "date": date.isoformat()},
                headers={"User-Agent": "NexPlay-TV-BR/1.0"},
                timeout=10,
            )
            r.raise_for_status()
            for ep in r.json():
                show = ep.get("show") or {}
                sid = show.get("id")
                if not sid or sid in shows:
                    continue
                image = show.get("image") or {}
                poster = image.get("medium") or image.get("original")
                if not poster:
                    continue
                shows[sid] = {
                    "title": show.get("name", ""),
                    "year": (show.get("premiered") or "")[:4],
                    "date": ep.get("airdate", ""),
                    "image": poster,
                    "type": "series",
                    "source": "TVmaze",
                    "source_url": show.get("url", "https://www.tvmaze.com/"),
                }
        except requests.RequestException:
            continue
    return list(shows.values())[:12]


def get_catalog():
    now = time.time()
    if CATALOG_CACHE["data"] is not None and now - CATALOG_CACHE["timestamp"] < CATALOG_TTL:
        return CATALOG_CACHE["data"]

    movies = []
    series = []
    try:
        movies = _wikidata_movies()
    except Exception:
        movies = []
    try:
        series = _tvmaze_series()
    except Exception:
        series = []

    data = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "movies": movies,
        "series": series,
        "attribution": {
            "wikidata": "https://www.wikidata.org/",
            "commons": "https://commons.wikimedia.org/",
            "tvmaze": "https://www.tvmaze.com/",
        },
    }
    CATALOG_CACHE.update({"timestamp": now, "data": data})
    return data


@app.route("/")
def home():
    html = render_template("index.html", plans=BR_PLANS, multi=BR_MULTI,
                           whatsapp="https://wa.me/" + BR_WHATSAPP)

    # Mantém o mesmo index.html/visual do projeto, mas remove o catálogo
    # dinâmico de filmes e séries e coloca apenas a informação institucional.
    content_section = """
    <section class="section catalog" id="catalogo">
      <div class="section-head">
        <span class="eyebrow">NEXPLAY</span>
        <h2>Mais de 20 mil conteúdos</h2>
        <p>Mais de 20 mil conteúdos entre canais ao vivo, 4K, HD, séries, filmes e conteúdos infantis.</p>
      </div>
    </section>
    """
    html = re.sub(r'\s*<section class="section catalog" id="catalogo">.*?</section>\s*',
                  "\n" + content_section + "\n", html, count=1, flags=re.S)

    # Melhora somente o FAQ sobre compatibilidade.
    html = html.replace(
        '<summary data-pt="O atendimento é em português?" data-en="Is support available in Portuguese?">O atendimento é em português?</summary><p data-pt="Sim. Nosso suporte é realizado em português pelo WhatsApp." data-en="Yes. Support is available in Portuguese through WhatsApp.">Sim. Nosso suporte é realizado em português pelo WhatsApp.</p>',
        '<summary data-pt="É compatível com quais dispositivos?" data-en="Which devices is it compatible with?">É compatível com quais dispositivos?</summary><p data-pt="É compatível com diversos dispositivos, como Smart TVs, celulares, tablets, computadores e outros aparelhos compatíveis. Consulte nossa equipe para confirmar o seu dispositivo." data-en="It is compatible with various devices, such as Smart TVs, smartphones, tablets, computers and other compatible devices. Contact our team to confirm your device.">É compatível com diversos dispositivos, como Smart TVs, celulares, tablets, computadores e outros aparelhos compatíveis. Consulte nossa equipe para confirmar o seu dispositivo.</p>'
    )
    return html


@app.route("/api/catalog")
def catalog():
    return jsonify(get_catalog())


@app.route("/health")
def health():
    return {"status": "ok", "service": "NexPlay TV Brasil"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
