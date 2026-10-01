"""Aplicacao simples usada na revisao de DevOps."""
from flask import Flask

app = Flask(__name__)


def mensagem() -> str:
    """Retorna a mensagem exibida pela aplicacao."""
    return "Ola, DevOps!"


@app.route("/")
def index():
    return mensagem()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
