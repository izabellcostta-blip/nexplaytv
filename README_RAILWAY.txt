NEXPLAY TV USA — Railway / Flask

1. Suba estes arquivos para o projeto no Railway:
   app.py
   requirements.txt
   Procfile
   runtime.txt
   templates/index.html
   static/styles.css
   static/script.js
   static/assets/logo.png

2. O Railway pode iniciar pelo Procfile:
   web: gunicorn app:app

3. O app usa a variável PORT do Railway automaticamente.

4. A rota /health serve para verificar se o serviço está online.
