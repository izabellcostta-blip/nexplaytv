from flask import Flask, render_template
from urllib.parse import quote

app = Flask(__name__)

WHATSAPP = "5513988817584"

PLANS_STANDARD = {
    "15 dias": ("R$ 10,00", "15 DIAS S/ ADULTO", "Sem conteúdo adulto"),
    "Mensal": ("R$ 24,99", "MENSAL S/ ADULTOS", "Sem conteúdo adulto"),
    "Trimestral": ("R$ 39,99", "3 MESES S/ ADULTO", "Sem conteúdo adulto"),
    "Semestral": ("R$ 59,99", "6 MESES SEM ADULTO", "Sem conteúdo adulto"),
    "Anual": ("R$ 129,99", "12 MESES SEM ADULTO", "Sem conteúdo adulto"),
}

PLANS_MULTI = {
    "Mensal": ("R$ 30,00", "MENSAL C/ ADULTOS", "Com conteúdo adulto"),
    "Trimestral": ("R$ 64,99", "TRIMESTRAL C/ ADULTOS", "Com conteúdo adulto"),
    "Semestral": ("R$ 89,99", "SEMESTRAL C/ ADULTOS", "Com conteúdo adulto"),
    "Anual": ("R$ 169,99", "ANUAL C/ ADULTOS", "Com conteúdo adulto"),
}

ADULT_STANDARD = {
    "15 dias": ("R$ 15,00", "15 DIAS C/ ADULTO", "Com conteúdo adulto"),
    "Mensal": ("R$ 29,99", "1 MÊS COM ADULTO", "Com conteúdo adulto"),
    "Trimestral": ("R$ 54,99", "3 MESES C/ ADULTO", "Com conteúdo adulto"),
    "Semestral": ("R$ 79,99", "6 MESES COM ADULTO", "Com conteúdo adulto"),
    "Anual": ("R$ 159,99", "12 MESES COM ADULTO", "Com conteúdo adulto"),
}

ADULT_MULTI = {
    "Mensal": ("R$ 30,00", "MENSAL C/ ADULTOS", "Com conteúdo adulto"),
    "Trimestral": ("R$ 64,99", "TRIMESTRAL C/ ADULTOS", "Com conteúdo adulto"),
    "Semestral": ("R$ 89,99", "SEMESTRAL C/ ADULTOS", "Com conteúdo adulto"),
    "Anual": ("R$ 169,99", "ANUAL C/ ADULTOS", "Com conteúdo adulto"),
}

def wa(message):
    return "https://wa.me/" + WHATSAPP + "?text=" + quote(message)

def rows(data):
    return [
        {
            "period": period,
            "price": value[0],
            "name": value[1],
            "description": value[2],
            "url": wa(f"Olá! Tenho interesse no plano {value[1]} — {value[0]}.")
        }
        for period, value in data.items()
    ]

@app.route("/")
def home():
    return render_template(
        "index.html",
        standard=rows(PLANS_STANDARD),
        multi=rows(PLANS_MULTI),
        adult_standard=rows(ADULT_STANDARD),
        adult_multi=rows(ADULT_MULTI),
        trial_url=wa("Olá! Quero solicitar o teste da NexPlay TV Brasil."),
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
