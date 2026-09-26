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
        "NEXPLAY TV BRASIL": "NEXPLAY TV BRASIL",
        "NexPlay TV Brasil": "NexPlay TV Brasil",
        "NEXPLAY TV BRASIL": "NEXPLAY TV BRASIL",
        "NexPlay TV Brasil": "NexPlay TV Brasil",
        "SEU ENTRETENIMENTO": "ENTRETENIMENTO DO SEU JEITO",
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

    # Botão flutuante de atendimento BR.
    # Faz a troca sem editar index.html ou styles.css.
    floating_script = r"""
    <style>
      .nexplay-br-wa-float {
        position: fixed !important;
        right: 22px !important;
        bottom: 22px !important;
        width: 58px !important;
        height: 58px !important;
        border-radius: 50% !important;
        background: #25D366 !important;
        color: #fff !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        z-index: 99999 !important;
        box-shadow: 0 10px 28px rgba(0,0,0,.35) !important;
        text-decoration: none !important;
        border: 0 !important;
        transition: transform .2s ease, box-shadow .2s ease !important;
      }
      .nexplay-br-wa-float:hover {
        transform: translateY(-3px) scale(1.04) !important;
        box-shadow: 0 14px 34px rgba(0,0,0,.42) !important;
      }
      .nexplay-br-wa-float svg {
        width: 31px !important;
        height: 31px !important;
        display: block !important;
      }
      @media (max-width: 600px) {
        .nexplay-br-wa-float {
          right: 16px !important;
          bottom: 16px !important;
          width: 56px !important;
          height: 56px !important;
        }
      }
    </style>
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        // Remove apenas antigos botões flutuantes do WhatsApp que possam
        // ter vindo do layout USA. Os botões normais dos planos permanecem.
        document.querySelectorAll('a[href*="wa.me"]').forEach(function (el) {
          var s = window.getComputedStyle(el);
          if (s.position === "fixed" || el.classList.contains("whatsapp-float") ||
              el.classList.contains("wa-float") || el.classList.contains("floating-whatsapp")) {
            el.remove();
          }
        });

        var old = document.getElementById("nexplay-br-wa-float");
        if (old) old.remove();

        var a = document.createElement("a");
        a.id = "nexplay-br-wa-float";
        a.className = "nexplay-br-wa-float";
        a.href = "https://wa.me/5513988817584";
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        a.setAttribute("aria-label", "Atendimento pelo WhatsApp");
        a.title = "Atendimento pelo WhatsApp";

        // Ícone no padrão oficial do WhatsApp, em branco sobre o verde da marca.
        a.innerHTML = '<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false">' +
          '<path fill="#fff" d="M19.11 17.41c-.27-.14-1.58-.78-1.83-.87-.25-.09-.43-.14-.61.14-.18.27-.7.87-.86 1.05-.16.18-.32.2-.59.07-.27-.14-1.13-.42-2.15-1.34-.79-.7-1.33-1.56-1.49-1.83-.16-.27-.02-.42.12-.56.12-.12.27-.32.41-.48.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.48-.07-.14-.61-1.47-.84-2.02-.22-.53-.45-.46-.61-.47-.16-.01-.34-.01-.52-.01-.18 0-.48.07-.73.34-.25.27-.95.93-.95 2.27s.98 2.64 1.11 2.82c.14.18 1.93 2.95 4.68 4.14.65.28 1.16.45 1.56.58.65.21 1.24.18 1.71.11.52-.08 1.58-.65 1.81-1.27.22-.62.22-1.15.16-1.27-.07-.11-.25-.18-.52-.32z"/>' +
          '<path fill="#fff" fill-rule="evenodd" d="M16.03 4.2c-6.52 0-11.82 5.3-11.82 11.82 0 2.08.55 4.11 1.58 5.89L4.2 27.8l6.07-1.59a11.77 11.77 0 0 0 5.76 1.5h.01c6.52 0 11.82-5.3 11.82-11.82S22.56 4.2 16.03 4.2zm0 21.57h-.01a9.75 9.75 0 0 1-4.97-1.37l-.36-.21-3.6.94.96-3.51-.23-.36a9.76 9.76 0 1 1 8.21 4.51z"/>' +
        '</svg>';

        document.body.appendChild(a);
      });
    </script>
    """

    # Evita que referências residuais ao USA apareçam no botão/área de contato.
    for old, new in {
        "NexPlay TV Brasil": "NexPlay TV Brasil",
        "NEXPLAY TV BRASIL": "NEXPLAY TV BRASIL",
        "NexPlay TV Brasil": "NexPlay TV Brasil",
        "NEXPLAY TV BRASIL": "NEXPLAY TV BRASIL",
        "Atendimento nos EUA": "Atendimento no Brasil",
        "nos EUA": "no Brasil",
    }.items():
        html = html.replace(old, new)

    html = html.replace("</body>", floating_script + "\n</body>")


    # FAQ exclusivo da versão Brasil.
    # Não há pergunta sobre idioma/atendimento no Brasil.
    faq_replacements = {
        "É compatível com quais dispositivos?":
            "Quais são os dispositivos compatíveis?",
        "Em quais dispositivos posso usar?":
            "Quais são os dispositivos compatíveis?",
        "A NexPlay é compatível com diversos dispositivos, como Smart TVs, celulares, tablets, computadores e outros aparelhos compatíveis. Fale conosco para confirmar a compatibilidade do seu aparelho.":
            "A NexPlay é compatível com diversos dispositivos, como Smart TVs, celulares, tablets, computadores e outros aparelhos compatíveis.",
        "É compatível com diversos dispositivos, como Smart TVs, celulares, tablets, computadores e outros aparelhos compatíveis. Consulte nossa equipe para confirmar o seu dispositivo.":
            "A NexPlay é compatível com diversos dispositivos, como Smart TVs, celulares, tablets, computadores e outros aparelhos compatíveis.",
        "O atendimento é em português?":
            "Quantos conteúdos vocês têm?",
        "Sim. Nosso suporte é realizado em português pelo WhatsApp.":
            "Temos mais de 20 mil conteúdos, incluindo canais ao vivo, conteúdos em 4K e HD, séries, filmes e conteúdos infantis.",
        "O atendimento é realizado em português?":
            "Quantos conteúdos vocês têm?",
        "Nosso suporte é realizado em português pelo WhatsApp.":
            "Temos mais de 20 mil conteúdos, incluindo canais ao vivo, conteúdos em 4K e HD, séries, filmes e conteúdos infantis.",
        "Quais formas de pagamento são aceitas?":
            "Preciso de cartão de crédito para ativar?",
        "Aceitamos Pix e cartão. Fale com nossa equipe pelo WhatsApp para receber as instruções de pagamento.":
            "Não. Você não precisa de cartão de crédito para ativar. As opções de pagamento disponíveis são informadas no momento da contratação.",
    }

    for old, new in faq_replacements.items():
        html = html.replace(old, new)

    # Se o template original ainda tiver a pergunta de português com atributos
    # data-pt/data-en, substitui a linha inteira por uma pergunta BR.
    html = re.sub(
        r'<summary[^>]*>O atendimento é em português\?</summary>\s*<p[^>]*>.*?</p>',
        '<summary data-pt="Quantos conteúdos vocês têm?" data-en="How many contents are available?">Quantos conteúdos vocês têm?</summary><p data-pt="Temos mais de 20 mil conteúdos, incluindo canais ao vivo, conteúdos em 4K e HD, séries, filmes e conteúdos infantis." data-en="We have more than 20,000 contents, including live channels, 4K and HD content, series, movies and children’s content.">Temos mais de 20 mil conteúdos, incluindo canais ao vivo, conteúdos em 4K e HD, séries, filmes e conteúdos infantis.</p>',
        html,
        flags=re.S,
    )

    # Substitui também variações da pergunta antiga, se existirem.
    html = re.sub(
        r'<summary[^>]*>É compatível com quais dispositivos\?</summary>\s*<p[^>]*>.*?</p>',
        '<summary data-pt="Quais são os dispositivos compatíveis?" data-en="Which devices are compatible?">Quais são os dispositivos compatíveis?</summary><p data-pt="A NexPlay é compatível com diversos dispositivos, como Smart TVs, celulares, tablets, computadores e outros aparelhos compatíveis." data-en="NexPlay is compatible with various devices, such as Smart TVs, smartphones, tablets, computers and other compatible devices.">A NexPlay é compatível com diversos dispositivos, como Smart TVs, celulares, tablets, computadores e outros aparelhos compatíveis.</p>',
        html,
        flags=re.S,
    )

    html = re.sub(
        r'<summary[^>]*>Quais formas de pagamento são aceitas\?</summary>\s*<p[^>]*>.*?</p>',
        '<summary data-pt="Preciso de cartão de crédito para ativar?" data-en="Do I need a credit card to activate?">Preciso de cartão de crédito para ativar?</summary><p data-pt="Não. Você não precisa de cartão de crédito para ativar. As opções de pagamento disponíveis são informadas no momento da contratação." data-en="No. You do not need a credit card to activate. Available payment options are provided at the time of purchase.">Não. Você não precisa de cartão de crédito para ativar. As opções de pagamento disponíveis são informadas no momento da contratação.</p>',
        html,
        flags=re.S,
    )



    # FAQ BR — conteúdo, dispositivos e teste grátis.
    faq_questions = [
        (
            "Quais conteúdos estão disponíveis?",
            "Você encontra canais ao vivo, filmes, séries, conteúdos em 4K e HD, opções infantis e muito mais, com uma programação pensada para diferentes momentos e perfis."
        ),
        (
            "Quantos conteúdos estão disponíveis?",
            "São mais de 20 mil conteúdos, incluindo canais ao vivo, 4K, HD, séries, filmes e conteúdos infantis."
        ),
        (
            "Quais dispositivos são compatíveis?",
            "A NexPlay é compatível com diversos dispositivos, como Smart TVs, celulares, tablets e computadores. A compatibilidade pode variar conforme o aparelho e o aplicativo utilizado."
        ),
        (
            "Preciso de cartão de crédito para ativar o teste grátis?",
            "Não. Não é necessário cartão de crédito para ativar o seu teste grátis. Você pode solicitar o teste pelo WhatsApp e receber as orientações para começar."
        ),
        (
            "Como funciona o teste grátis?",
            "Você pode solicitar um teste grátis de 6 ou 12 horas, conforme disponibilidade. Assim, você conhece a experiência NexPlay antes de escolher um plano."
        ),
        (
            "O que está incluso nos planos?",
            "Os planos incluem acesso aos conteúdos disponíveis na opção escolhida, com canais ao vivo, filmes, séries, conteúdos infantis e opções em diferentes qualidades, como 4K e HD, conforme a disponibilidade de cada conteúdo."
        ),
    ]

    faq_html = '<div class="faq-list" id="faq-br">'
    for question, answer in faq_questions:
        faq_html += (
            '<details class="faq-item">'
            '<summary>' + question + '</summary>'
            '<p>' + answer + '</p>'
            '</details>'
        )
    faq_html += '</div>'

    html = re.sub(
        r'<div class="faq-list".*?</div>',
        faq_html,
        html,
        count=1,
        flags=re.S,
    )


    # Hero BR: substitui a arte genérica da tela por uma foto de família assistindo TV.
    # A imagem é carregada diretamente no navegador, portanto não exige outro arquivo.
    family_photo = "https://images.pexels.com/photos/5813746/pexels-photo-5813746.jpeg?auto=compress&cs=tinysrgb&w=1400"

    hero_visual_script = """
    <style>
      .nexplay-family-hero {
        position: absolute;
        inset: 7% 4% 7% 4%;
        overflow: hidden;
        border-radius: 24px;
        border: 1px solid rgba(55,153,255,.55);
        box-shadow: 0 0 45px rgba(32,137,255,.20), 0 22px 55px rgba(0,0,0,.35);
        background: #07101e;
        transform: rotate(1.5deg);
      }
      .nexplay-family-hero img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
        display: block;
      }
      .nexplay-family-hero::after {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(2,12,28,.05), rgba(0,25,65,.18));
        pointer-events: none;
      }
      @media (max-width: 700px) {
        .nexplay-family-hero {
          inset: 5% 3%;
          border-radius: 18px;
        }
      }
    </style>
    <script>
      document.addEventListener("DOMContentLoaded", function () {
        var photoUrl = "__FAMILY_PHOTO_URL__";

        // Localiza a tela/arte atual do hero sem alterar o restante da página.
        var candidates = document.querySelectorAll(
          ".hero-visual, .hero-art, .hero-screen, .screen, .device, .visual-card, .hero-media"
        );

        var target = null;
        for (var i = 0; i < candidates.length; i++) {
          var el = candidates[i];
          var rect = el.getBoundingClientRect();
          if (rect.width > 250 && rect.height > 140) {
            target = el;
            break;
          }
        }

        // Fallback: procura o bloco que contém o texto da arte antiga.
        if (!target) {
          var all = document.querySelectorAll("div, section, article");
          for (var j = 0; j < all.length; j++) {
            var t = (all[j].textContent || "").trim();
            if (t.indexOf("ENTERTAINMENT") !== -1 || t.indexOf("YOUR WAY") !== -1) {
              var r = all[j].getBoundingClientRect();
              if (r.width > 250 && r.height > 140) {
                target = all[j];
                break;
              }
            }
          }
        }

        if (!target) return;

        target.style.position = "relative";
        target.style.overflow = "hidden";

        var oldContent = target.querySelectorAll("*");
        for (var k = 0; k < oldContent.length; k++) {
          oldContent[k].style.visibility = "hidden";
        }

        var photo = document.createElement("div");
        photo.className = "nexplay-family-hero";
        photo.innerHTML = '<img src="' + photoUrl + '" alt="Família assistindo televisão em casa">';
        target.appendChild(photo);
      });
    </script>
    """  # URL is inserted below without "%" formatting.

    hero_visual_script = hero_visual_script.replace("__FAMILY_PHOTO_URL__", family_photo)
    html = html.replace("</body>", hero_visual_script + "\n</body>")

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
