from flask import Flask, render_template, jsonify
import re
import os
import time
from datetime import datetime, timedelta, timezone

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

@app.route("/")
def home():
    html = render_template(
        "index.html",
        plans=BR_PLANS,
        multi=BR_MULTI,
        whatsapp="https://wa.me/" + BR_WHATSAPP,
    )

    # Alterações feitas somente pelo app.py.
    # index.html, CSS, JavaScript e logo permanecem intactos.
    replacements = {
        "NEXPLAY TV USA": "NEXPLAY TV BRASIL",
        "NexPlay TV USA": "NexPlay TV Brasil",
        "NEXPLAY USA": "NEXPLAY TV BRASIL",
        "NexPlay USA": "NexPlay TV Brasil",
        "ENTERTAINMENT YOUR WAY": "ENTRETENIMENTO DO SEU JEITO",
        "Valores em dólares.": "Valores em reais.",
        "Values in dollars.": "Valores em reais.",
        "Séries em exibição nos EUA": "Séries e filmes",
        "séries em exibição nos EUA": "séries e filmes",
    }
    for old, new in replacements.items():
        html = html.replace(old, new)

    content_section = """
    <section class="section catalog" id="catalogo">
      <div class="section-head">
        <span class="eyebrow">NEXPLAY TV BRASIL</span>
        <h2>Mais de 20 mil conteúdos para você aproveitar</h2>
        <p>Uma programação completa com canais ao vivo, conteúdos em 4K e HD, séries, filmes e opções infantis.</p>
      </div>

      <div class="feature-grid" style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:28px;">
        <article class="feature-card" style="background:linear-gradient(145deg,rgba(15,20,35,.96),rgba(7,10,20,.98));border:1px solid rgba(45,140,255,.22);border-radius:18px;padding:22px;box-shadow:0 14px 35px rgba(0,0,0,.22);">

          <span class="feature-number">01</span>
          <h3>Canais ao vivo</h3>
          <p>Uma ampla variedade de canais para acompanhar sua programação favorita.</p>
        </article>

        <article class="feature-card" style="background:linear-gradient(145deg,rgba(15,20,35,.96),rgba(7,10,20,.98));border:1px solid rgba(45,140,255,.22);border-radius:18px;padding:22px;box-shadow:0 14px 35px rgba(0,0,0,.22);">
          <span class="feature-number">02</span>
          <h3>Filmes e séries</h3>
          <p>Opções de entretenimento para diferentes estilos e momentos.</p>
        </article>

        <article class="feature-card" style="background:linear-gradient(145deg,rgba(15,20,35,.96),rgba(7,10,20,.98));border:1px solid rgba(45,140,255,.22);border-radius:18px;padding:22px;box-shadow:0 14px 35px rgba(0,0,0,.22);">
          <span class="feature-number">03</span>
          <h3>4K e HD</h3>
          <p>Conteúdos disponíveis em diferentes qualidades, conforme a disponibilidade.</p>
        </article>

        <article class="feature-card" style="background:linear-gradient(145deg,rgba(15,20,35,.96),rgba(7,10,20,.98));border:1px solid rgba(45,140,255,.22);border-radius:18px;padding:22px;box-shadow:0 14px 35px rgba(0,0,0,.22);">
          <span class="feature-number">04</span>
          <h3>Conteúdo infantil</h3>
          <p>Opções de entretenimento para os pequenos também fazem parte da experiência NexPlay.</p>
        </article>
      </div>
    </section>
    """

    html = re.sub(
        r'\s*<section class="section catalog" id="catalogo">.*?</section>\s*',
        "\n" + content_section + "\n",
        html,
        count=1,
        flags=re.S,
    )

    faq_replacements = {
        "Clique em qualquer botão de teste e fale conosco pelo WhatsApp. A disponibilidade e duração do teste serão confirmadas no atendimento.":
            "Clique em qualquer botão de teste e fale conosco pelo WhatsApp. Nossa equipe informa a disponibilidade e orienta você durante o atendimento.",
        "Aceitamos Pix e cartão. Fale com o suporte para receber as instruções de pagamento.":
            "Aceitamos Pix e cartão. Fale com nossa equipe pelo WhatsApp para receber as instruções de pagamento.",
        "É compatível com quais dispositivos?":
            "Em quais dispositivos posso usar?",
        "É compatível com diversos dispositivos, como Smart TVs, celulares, tablets, computadores e outros aparelhos compatíveis. Consulte nossa equipe para confirmar o seu dispositivo.":
            "A NexPlay é compatível com diversos dispositivos, como Smart TVs, celulares, tablets, computadores e outros aparelhos compatíveis. Fale conosco para confirmar a compatibilidade do seu aparelho.",
    }
    for old, new in faq_replacements.items():
        html = html.replace(old, new)

    html = html.replace("</head>", """<style>
@media (max-width: 900px) {
  .feature-grid { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
}
@media (max-width: 560px) {
  .feature-grid { grid-template-columns: 1fr !important; }
}
</style></head>""")
    return html


@app.route("/api/catalog")
def catalog():
    return jsonify({
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "movies": [],
        "series": [],
        "attribution": {},
    })


@app.route("/health")
def health():
    return {"status": "ok", "service": "NexPlay TV Brasil"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
