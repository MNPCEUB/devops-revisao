from app import app, mensagem


def test_mensagem_padrao():
    assert mensagem() == "Ola, DevOps!"


def test_rota_raiz_responde_200():
    cliente = app.test_client()
    resposta = cliente.get("/")
    assert resposta.status_code == 200
    assert resposta.get_data(as_text=True) == mensagem()
