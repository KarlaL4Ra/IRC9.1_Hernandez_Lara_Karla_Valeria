from flask import Flask, render_template, request, make_response, render_template_string
import subprocess
from weasyprint import HTML

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = ""
    if request.method == "POST":
        playbook = request.form["playbook"]
        try:
            result = subprocess.run(
                ["ansible-playbook", f"playbooks/{playbook}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            resultado = result.stdout + result.stderr
        except Exception as e:
            resultado = str(e)
    return render_template("index.html", resultado=resultado)

@app.route("/descargar-pdf", methods=["POST"])
def descargar_pdf():
    resultado = request.form.get("resultado", "")
    html_code = render_template_string("""
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body { font-family: sans-serif; padding: 20px; }
            h2 { color: #b73cbd; }
            pre { background: #eee; padding: 10px; border-radius: 5px; }
          </style>
        </head>
        <body>
          <h2>🫧 Resultado LIMPOWER 🫧</h2>
          <pre>{{ resultado }}</pre>
        </body>
        </html>
    """, resultado=resultado)

    pdf = HTML(string=html_code).write_pdf()
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=limpieza_resultado.pdf"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
