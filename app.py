from flask import Flask, render_template
from urllib.parse import quote

app=Flask(__name__)
WHATSAPP="5513988817584"

standard=[
("15 dias","R$ 10,00","15 DIAS S/ ADULTO",None),
("Mensal","R$ 24,99","MENSAL S/ ADULTOS","R$ 30,00"),
("Trimestral","R$ 39,99","3 MESES S/ ADULTO","R$ 49,99"),
("Semestral","R$ 59,99","6 MESES SEM ADULTO","R$ 69,99"),
("Anual","R$ 129,99","12 MESES SEM ADULTO","R$ 139,99"),
]
adult=[
("15 dias","R$ 15,00","15 DIAS C/ ADULTO",None),
("Mensal","R$ 29,99","1 MÊS COM ADULTO","R$ 30,00"),
("Trimestral","R$ 54,99","3 MESES C/ ADULTO","R$ 64,99"),
("Semestral","R$ 79,99","6 MESES COM ADULTO","R$ 89,99"),
("Anual","R$ 159,99","12 MESES COM ADULTO","R$ 169,99"),
]
def wa(msg):
    return "https://wa.me/"+WHATSAPP+"?text="+quote(msg)
def pack(items):
    return [{"period":a,"price":b,"name":c,"multi":d,
             "url":wa(f"Olá! Tenho interesse no plano {c} — {b}.")}
            for a,b,c,d in items]

@app.route("/")
def home():
    return render_template("index.html", standard=pack(standard), adult=pack(adult),
                           trial_url=wa("Olá! Quero fazer o teste da NexPlay TV Brasil."),
                           whatsapp=WHATSAPP)
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
