"""NexPlay TV Brasil - aplicação WSGI independente.

Este arquivo não depende de Flask, templates externos ou arquivos estáticos.
Pode ser executado pelo Gunicorn com: gunicorn app:app
"""
from html import escape
from urllib.parse import quote

WHATSAPP = "5513988817584"
PLANS = [
    {"duration": "15 Dias", "days": 15, "standard": 20.00, "adult": 25.00},
    {"duration": "1 Mês", "days": 30, "standard": 30.00, "adult": 35.00},
    {"duration": "3 Meses", "days": 90, "standard": 65.00, "adult": 70.00},
    {"duration": "6 Meses", "days": 180, "standard": 105.00, "adult": 110.00},
    {"duration": "12 Meses", "days": 365, "standard": 165.00, "adult": 170.00},
]


def money(value):
    return (f"R$ {value:,.2f}").replace(",", "X").replace(".", ",").replace("X", ".")


def build_page():
    cards = []
    for index, plan in enumerate(PLANS):
        cards.append(f'''<article class="plan-card" data-index="{index}">
          <div class="plan-main"><div><span class="plan-duration">{escape(plan['duration'])}</span>
          <span class="per-month">{money(plan['standard'] / max(1, round(plan['days']/30)))}/mês aprox.</span></div>
          <div class="price" data-standard="{money(plan['standard'])}" data-adult="{money(plan['adult'])}">{money(plan['standard'])}</div></div>
          <div class="plan-bottom"><span class="saving">{('MELHOR CUSTO-BENEFÍCIO' if index == 4 else ('Economize mais no plano' if index in (2,3) else ''))}</span>
          <a class="choose-plan" data-plan="{escape(plan['duration'])}" href="https://wa.me/{WHATSAPP}?text={quote('Olá! Tenho interesse no plano ' + plan['duration'] + ' sem conteúdo adulto por ' + money(plan['standard']) + '.')}">Escolher plano</a></div>
        </article>''')
    plans_html = "\n".join(cards)
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#080d1c">
<meta name="description" content="Conheça os planos NexPlay TV Brasil e fale com nosso atendimento pelo WhatsApp.">
<title>NexPlay TV Brasil | Planos</title>
<style>
:root{{--bg:#080d1c;--panel:#111a30;--panel2:#17223c;--text:#f6f8ff;--muted:#aab6d0;--blue:#347cff;--green:#24c66a;--line:rgba(255,255,255,.11)}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:radial-gradient(ellipse at top,#172747 0,#080d1c 48%,#060914 100%);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--text);line-height:1.5}}a{{color:inherit;text-decoration:none}}.wrap{{width:min(1120px,calc(100% - 32px));margin:0 auto}}header{{padding:22px 0;border-bottom:1px solid var(--line);background:rgba(5,9,20,.55)}}.nav{{display:flex;align-items:center;justify-content:space-between;gap:18px}}.brand{{display:flex;align-items:center;gap:12px;font-weight:850;letter-spacing:.4px}}.logo{{display:grid;place-items:center;width:43px;height:43px;border-radius:14px;background:linear-gradient(145deg,#4489ff,#1e4cc0);box-shadow:0 8px 24px #347cff44;font-size:18px}}.brand small{{display:block;color:var(--muted);font-size:11px;letter-spacing:2px;font-weight:700}}.nav-cta{{background:var(--green);color:#04160b;font-weight:800;padding:11px 17px;border-radius:999px}}.hero{{padding:68px 0 36px;text-align:center}}.eyebrow{{display:inline-flex;padding:7px 12px;border:1px solid #347cff55;background:#347cff17;border-radius:999px;color:#8bb5ff;font-size:12px;font-weight:800;letter-spacing:1.8px}}h1{{font-size:clamp(34px,6vw,58px);line-height:1.08;margin:19px auto 16px;max-width:850px;letter-spacing:-1.7px}}.gradient{{background:linear-gradient(90deg,#fff,#8bb7ff);-webkit-background-clip:text;background-clip:text;color:transparent}}.hero p{{max-width:670px;margin:0 auto;color:var(--muted);font-size:17px}}.benefits{{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:26px auto 0}}.benefits span{{border:1px solid var(--line);background:#ffffff08;border-radius:999px;padding:8px 12px;font-size:13px;color:#d9e3f8}}.pricing{{padding:20px 0 70px}}.section-title{{text-align:center;margin-bottom:24px}}.section-title h2{{font-size:clamp(26px,4vw,38px);margin:0 0 8px;letter-spacing:-.8px}}.section-title p{{margin:0;color:var(--muted)}}.toggle-label{{font-size:13px;color:var(--muted);text-align:center;margin-bottom:10px;font-weight:750;letter-spacing:.7px}}.toggle{{width:min(490px,100%);margin:0 auto 28px;padding:6px;display:grid;grid-template-columns:1fr 1fr;gap:6px;background:#ffffff0d;border:1px solid var(--line);border-radius:17px}}.toggle button{{border:0;border-radius:12px;padding:13px 10px;background:transparent;color:var(--muted);font:inherit;font-weight:800;cursor:pointer}}.toggle button.active{{background:#f8faff;color:#101a32;box-shadow:0 3px 12px #0003}}.toggle button span{{display:block;font-size:11px;font-weight:550;margin-top:2px}}.plans{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}.plan-card{{background:linear-gradient(145deg,#131d34,#0f172a);border:1px solid var(--line);border-radius:22px;padding:22px;box-shadow:0 14px 40px #0002;display:flex;flex-direction:column;gap:16px;min-width:0}}.plan-card:last-child{{grid-column:1/-1;border-color:#347cff77;background:linear-gradient(145deg,#172b50,#10182c)}}.plan-main{{display:flex;align-items:center;justify-content:space-between;gap:12px}}.plan-duration{{font-size:20px;font-weight:850;display:block}}.per-month{{font-size:12px;color:var(--muted);display:block;margin-top:3px}}.price{{font-size:clamp(24px,3vw,32px);font-weight:900;letter-spacing:-.7px;white-space:nowrap}}.plan-bottom{{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}}.saving{{font-size:11px;letter-spacing:.6px;color:#82b1ff;font-weight:850}}.choose-plan{{display:inline-flex;align-items:center;justify-content:center;padding:11px 16px;border-radius:12px;background:var(--blue);color:white;font-weight:850;font-size:14px;white-space:nowrap}}.info{{padding:0 0 62px}}.info-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}}.info-card{{padding:20px;border:1px solid var(--line);border-radius:18px;background:#ffffff07}}.info-card strong{{display:block;margin-bottom:6px}}.info-card p{{margin:0;color:var(--muted);font-size:14px}}.contact{{text-align:center;padding:34px 20px;border:1px solid #347cff55;border-radius:24px;background:linear-gradient(120deg,#14274a,#10172a);margin-bottom:64px}}.contact h2{{margin:0 0 8px;font-size:28px}}.contact p{{color:var(--muted);margin:0 auto 18px}}.contact a{{display:inline-flex;padding:13px 22px;background:var(--green);color:#04160b;border-radius:999px;font-weight:900}}footer{{border-top:1px solid var(--line);padding:22px 0;color:var(--muted);font-size:12px;text-align:center}}.float-wa{{position:fixed;right:20px;bottom:20px;z-index:9;width:60px;height:60px;border-radius:50%;display:grid;place-items:center;background:var(--green);color:#04200f;box-shadow:0 8px 28px #0006;font-size:29px;font-weight:900;border:3px solid #fff3}}@media(max-width:700px){{.hero{{padding:48px 0 25px}}.plans{{grid-template-columns:1fr}}.plan-card:last-child{{grid-column:auto}}.info-grid{{grid-template-columns:1fr}}.plan-card{{padding:19px}}.nav-cta{{padding:10px 12px;font-size:13px}}.brand{{font-size:13px}}.brand small{{font-size:9px}}.plan-main{{gap:6px}}.price{{font-size:27px}}}}
</style>
</head><body>
<header><div class="wrap nav"><a class="brand" href="/"><span class="logo">N</span><span>NEXPLAY TV<small>BRASIL</small></span></a><a class="nav-cta" href="https://wa.me/{WHATSAPP}?text={quote('Olá! Quero conhecer os planos NexPlay TV Brasil.')}">Falar no WhatsApp</a></div></header>
<main><section class="hero wrap"><span class="eyebrow">NEXPLAY TV BRASIL</span><h1>Seu entretenimento,<br><span class="gradient">do seu jeito.</span></h1><p>Escolha o plano que combina com você e fale com nossa equipe para receber orientações de ativação.</p><div class="benefits"><span>✓ Planos de 15 dias a 12 meses</span><span>✓ Opção com ou sem conteúdo adulto</span><span>✓ Atendimento pelo WhatsApp</span></div></section>
<section class="pricing wrap" id="planos"><div class="section-title"><h2>Escolha seu plano</h2><p>Selecione o tipo de conteúdo para ver os valores atualizados.</p></div><div class="toggle-label">TIPO DE CONTEÚDO</div><div class="toggle" role="group" aria-label="Tipo de conteúdo"><button class="active" id="standardBtn" type="button" aria-pressed="true">Padrão<span>Sem conteúdo adulto</span></button><button id="adultBtn" type="button" aria-pressed="false">Adulto incluso<span>Com conteúdo adulto</span></button></div><div class="plans">{plans_html}</div></section>
<section class="info wrap"><div class="section-title"><h2>Como funciona?</h2><p>Veja as informações principais antes de escolher.</p></div><div class="info-grid"><article class="info-card"><strong>1. Escolha o plano</strong><p>Selecione a duração e o tipo de conteúdo desejado.</p></article><article class="info-card"><strong>2. Fale com a equipe</strong><p>Use o WhatsApp para tirar dúvidas e receber as instruções.</p></article><article class="info-card"><strong>3. Receba orientações</strong><p>Nossa equipe informa os próximos passos para ativação.</p></article></div></section>
<section class="contact wrap"><h2>Precisa de ajuda para escolher?</h2><p>Entre em contato com a equipe NexPlay TV Brasil.</p><a href="https://wa.me/{WHATSAPP}?text={quote('Olá! Preciso de ajuda para escolher um plano NexPlay TV Brasil.')}">Conversar pelo WhatsApp</a></section></main>
<footer><div class="wrap">NexPlay TV Brasil · Atendimento pelo WhatsApp · Os valores são apresentados em reais.</div></footer>
<a class="float-wa" aria-label="Falar com a NexPlay no WhatsApp" href="https://wa.me/{WHATSAPP}?text={quote('Olá! Vim pelo site NexPlay TV Brasil e gostaria de informações.')}">✆</a>
<script>
(function(){{
 const adultBtn=document.getElementById('adultBtn'); const standardBtn=document.getElementById('standardBtn');
 function setMode(adult){{
  standardBtn.classList.toggle('active',!adult); adultBtn.classList.toggle('active',adult);
  standardBtn.setAttribute('aria-pressed',String(!adult)); adultBtn.setAttribute('aria-pressed',String(adult));
  document.querySelectorAll('.plan-card').forEach(function(card){{
   const price=card.querySelector('.price'); const amount=adult?price.dataset.adult:price.dataset.standard;
   price.textContent=amount;
   const plan=card.querySelector('.plan-duration').textContent;
   const link=card.querySelector('.choose-plan');
   const type=adult?'com conteúdo adulto':'sem conteúdo adulto';
   link.href='https://wa.me/{WHATSAPP}?text='+encodeURIComponent('Olá! Tenho interesse no plano '+plan+' '+type+' por '+amount+'.');
  }});
 }}
 standardBtn.addEventListener('click',function(){{setMode(false)}}); adultBtn.addEventListener('click',function(){{setMode(true)}});
 setMode(false);
}})();
</script></body></html>'''

PAGE = build_page().encode("utf-8")
HEALTH = b'{"status":"ok","service":"NexPlay TV Brasil"}'


def app(environ, start_response):
    """Minimal WSGI entry point, compatible with Gunicorn's app:app target."""
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET").upper()
    if path == "/health":
        body = HEALTH
        content_type = "application/json; charset=utf-8"
        status = "200 OK"
    elif path == "/" or path == "/index.html":
        body = PAGE
        content_type = "text/html; charset=utf-8"
        status = "200 OK"
    elif path == "/api/catalog":
        body = b'{"movies":[],"series":[],"attribution":{}}'
        content_type = "application/json; charset=utf-8"
        status = "200 OK"
    else:
        body = b'{"error":"not found"}'
        content_type = "application/json; charset=utf-8"
        status = "404 Not Found"
    headers = [("Content-Type", content_type), ("Content-Length", str(len(body))), ("Cache-Control", "no-store")]
    start_response(status, headers)
    return [b"" if method == "HEAD" else body]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    import os
    port = int(os.environ.get("PORT", "8080"))
    with make_server("0.0.0.0", port, app) as server:
        print(f"NexPlay TV Brasil ouvindo na porta {port}")
        server.serve_forever()
