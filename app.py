from flask import Flask, render_template
from urllib.parse import quote

app = Flask(__name__)

WHATSAPP = "5513988817584"

def whatsapp_url(message):
    return "https://wa.me/" + WHATSAPP + "?text=" + quote(message)

PLANS_WITHOUT_ADULT = [
    ("15 DIAS S/ ADULTO", "R$ 10,00", "15 dias", ""),
    ("MENSAL S/ ADULTOS", "R$ 24,99", "1 mês", ""),
    ("TRIMESTRAL S/ ADULTOS", "R$ 49,99", "3 meses", "MULTI-SERVER"),
    ("3 MESES S/ ADULTO", "R$ 39,99", "3 meses", ""),
    ("SEMESTRAL S/ ADULTOS", "R$ 69,99", "6 meses", "MULTI-SERVER"),
    ("6 MESES SEM ADULTO", "R$ 59,99", "6 meses", ""),
    ("ANUAL S/ ADULTOS", "R$ 139,99", "12 meses", "MULTI-SERVER"),
    ("12 MESES SEM ADULTO", "R$ 129,99", "12 meses", ""),
]

PLANS_WITH_ADULT = [
    ("15 DIAS C/ ADULTO", "R$ 15,00", "15 dias", ""),
    ("MENSAL C/ ADULTOS", "R$ 30,00", "1 mês", "MULTI-SERVER"),
    ("1 MÊS COM ADULTO", "R$ 29,99", "1 mês", ""),
    ("TRIMESTRAL C/ ADULTOS", "R$ 64,99", "3 meses", "MULTI-SERVER"),
    ("3 MESES C/ ADULTO", "R$ 54,99", "3 meses", ""),
    ("SEMESTRAL C/ ADULTOS", "R$ 89,99", "6 meses", "MULTI-SERVER"),
    ("6 MESES COM ADULTO", "R$ 79,99", "6 meses", ""),
    ("ANUAL C/ ADULTOS", "R$ 169,99", "12 meses", "MULTI-SERVER"),
    ("12 MESES COM ADULTO", "R$ 159,99", "12 meses", ""),
]

def prepare(plans):
    return [
        {
            "name": name,
            "price": price,
            "duration": duration,
            "tag": tag,
            "url": whatsapp_url(f"Olá! Tenho interesse no plano {name} — {price}."),
        }
        for name, price, duration, tag in plans
    ]

@app.route("/")
def home():
    return render_template(
        "index.html",
        plans_without=prepare(PLANS_WITHOUT_ADULT),
        plans_adult=prepare(PLANS_WITH_ADULT),
        trial_url=whatsapp_url("Olá! Quero saber como funciona o teste da NexPlay TV Brasil."),
        whatsapp_url=whatsapp_url,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
