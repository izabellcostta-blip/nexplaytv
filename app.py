from flask import Flask, render_template
from urllib.parse import quote
import os

app = Flask(__name__)

WHATSAPP = "5513988817584"

PLANS_NO_ADULT = [
    {"period":"15 DIAS","price":"R$ 10,00","name":"15 DIAS S/ ADULTO","multi":"—"},
    {"period":"MENSAL","price":"R$ 24,99","name":"MENSAL S/ ADULTOS","multi":"R$ 30,00"},
    {"period":"TRIMESTRAL","price":"R$ 39,99","name":"3 MESES S/ ADULTO","multi":"R$ 49,99"},
    {"period":"SEMESTRAL","price":"R$ 59,99","name":"6 MESES SEM ADULTO","multi":"R$ 69,99"},
    {"period":"ANUAL","price":"R$ 129,99","name":"12 MESES SEM ADULTO","multi":"R$ 139,99"},
]

PLANS_ADULT = [
    {"period":"15 DIAS","price":"R$ 15,00","name":"15 DIAS C/ ADULTO","multi":"—"},
    {"period":"MENSAL","price":"R$ 29,99","name":"1 MÊS COM ADULTO","multi":"R$ 30,00"},
    {"period":"TRIMESTRAL","price":"R$ 54,99","name":"3 MESES C/ ADULTO","multi":"R$ 64,99"},
    {"period":"SEMESTRAL","price":"R$ 79,99","name":"6 MESES COM ADULTO","multi":"R$ 89,99"},
    {"period":"ANUAL","price":"R$ 159,99","name":"12 MESES COM ADULTO","multi":"R$ 169,99"},
]

def whatsapp(text):
    return "https://wa.me/" + WHATSAPP + "?text=" + quote(text)

@app.route("/")
def home():
    for p in PLANS_NO_ADULT + PLANS_ADULT:
        p["url"] = whatsapp("Olá! Tenho interesse no plano " + p["name"] + " — " + p["price"] + ".")
    return render_template(
        "index.html",
        no_adult=PLANS_NO_ADULT,
        adult=PLANS_ADULT,
        trial_url=whatsapp("Olá! Quero solicitar o teste da NexPlay TV Brasil."),
        whatsapp_display="(13) 98881-7584"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
