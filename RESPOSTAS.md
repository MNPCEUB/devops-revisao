# Revisao DevOps — exercicios 23 a 28

Repositorio: `devops-revisao` (conta GitHub **MNPCEUB**)
Aplicacao: API Flask minima (`app.py`) com testes em `pytest` (`test_app.py`).

---

## 23. Repositorio Git local com dois commits

```bash
mkdir -p ~/repos/devops-revisao && cd ~/repos/devops-revisao
git init -b main
git config user.name "Matheus"
git config user.email "matheuswark@sempreceub.com"

# 1o commit: aplicacao + dependencias
git add app.py requirements.txt .gitignore
git commit -m "Cria aplicacao Flask basica com a funcao mensagem"

# 2o commit: testes + documentacao
git add test_app.py README.md
git commit -m "Adiciona testes com pytest e README do projeto"

git log --oneline
```

Saida de `git log --oneline`:

```
e0d4133 Adiciona testes com pytest e README do projeto
2676c47 Cria aplicacao Flask basica com a funcao mensagem
```

---

## 24. Branch `feature-mensagem` e integracao ao branch principal

```bash
# cria e entra na branch
git switch -c feature-mensagem          # equivalente a: git checkout -b feature-mensagem

# alteracao da saida do programa:
#   "Ola, DevOps!"  ->  "Ola, DevOps! Pipeline rodando com GitHub Actions."
git add app.py test_app.py
git commit -m "Altera a mensagem exibida pela aplicacao"

# volta ao branch principal e integra
git switch main                         # equivalente a: git checkout main
git merge --no-ff feature-mensagem -m "Integra a branch feature-mensagem ao main"

git log --oneline --graph --all
```

`--no-ff` forca um commit de merge, deixando o historico da branch visivel:

```
*   69d2a3b Integra a branch feature-mensagem ao main
|\
| * 39710fa Altera a mensagem exibida pela aplicacao
|/
* e0d4133 Adiciona testes com pytest e README do projeto
* 2676c47 Cria aplicacao Flask basica com a funcao mensagem
```

Opcional, depois do merge:

```bash
git branch -d feature-mensagem   # remove a branch ja integrada
git push origin main
```

---

## 25. Workflow minimo do GitHub Actions

Arquivo `.github/workflows/ci.yml`:

```yaml
name: CI

on: [push]

jobs:
  testes:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout do codigo
        uses: actions/checkout@v4

      - name: Configura o Python 3
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Instala dependencias
        run: |
          python -m pip install --upgrade pip
          pip install pytest
          pip install -r requirements.txt

      - name: Executa os testes
        run: pytest -q
```

Os quatro passos pedidos: **checkout** (`actions/checkout`), **Python 3**
(`actions/setup-python`), **instalacao do pytest** e **execucao dos testes**.

Execucao local equivalente (2 testes passando):

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/pytest -q
# ..                                        [100%]
# 2 passed in 0.30s
```

---

## 26. Servidor local, PID da porta e encerramento

Terminal 1:

```bash
python3 -m http.server 8080
```

Terminal 2 — identificar a porta e o PID:

```bash
lsof -i :8080 -sTCP:LISTEN     # lista o processo que escuta na porta
lsof -t -i :8080 -sTCP:LISTEN  # imprime apenas o PID
# alternativas: netstat -anv | grep 8080   |   ss -ltnp | grep 8080 (Linux)
```

Encerrar e confirmar que a porta foi liberada:

```bash
kill <PID>                     # kill -9 <PID> apenas se nao encerrar
lsof -i :8080 -sTCP:LISTEN     # sem saida = porta liberada
curl http://localhost:8080/    # "Connection refused" = porta liberada
```

Execucao real nesta maquina (a porta 8080 ja estava ocupada pelo OrbStack, entao a
demonstracao usou a 8081 — os comandos sao identicos, so muda o numero da porta):

```
### identificar porta e PID
COMMAND   PID   USER   FD   TYPE  ...  NAME
Python  30834 matier    5u  IPv6  ...  TCP *:sunproxyadmin (LISTEN)
PID = 30834

### servidor respondendo
HTTP 200

### apos kill 30834
nenhum processo escutando na porta 8081 (porta liberada)
curl: conexao recusada (porta liberada)
```

Observacao util: quando a porta ja esta em uso, `python -m http.server 8080` falha com
`OSError: [Errno 48] Address already in use` — e o proprio `lsof -i :8080` que mostra
qual processo a esta segurando.

---

## 27. Dockerfile

```dockerfile
# Imagem base com Python
FROM python:3.12-slim

# Diretorio de trabalho dentro do container
WORKDIR /app

# Instalacao das dependencias (copiadas antes para aproveitar o cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia dos arquivos da aplicacao
COPY . .

EXPOSE 5000

# Comando de inicializacao
CMD ["python", "app.py"]
```

Os cinco itens pedidos: imagem base (`FROM`), diretorio de trabalho (`WORKDIR`),
copia dos arquivos (`COPY`), instalacao de dependencias (`RUN pip install`) e
comando de inicializacao (`CMD`).

---

## 28. Build, execucao e inspecao do container

```bash
# constroi a imagem com o nome pedido
docker build -t devops-revisao .

# executa em background expondo a aplicacao para o host (host 8000 -> container 5000)
docker run -d --name app-revisao -p 8000:5000 devops-revisao

# lista os containers em execucao
docker ps

# le os logs da aplicacao
docker logs app-revisao

# teste a partir do host
curl http://localhost:8000/
```

Saidas obtidas:

`docker ps`

```
CONTAINER ID   IMAGE            COMMAND           STATUS         PORTS                        NAMES
97765d9db52f   devops-revisao   "python app.py"   Up 3 seconds   0.0.0.0:8000->5000/tcp       app-revisao
```

`curl http://localhost:8000/`

```
Ola, DevOps! Pipeline rodando com GitHub Actions.
```

`docker logs app-revisao`

```
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
192.168.215.1 - - [01/Oct/2026 23:37:10] "GET / HTTP/1.1" 200 -
```

Limpeza:

```bash
docker stop app-revisao
docker rm app-revisao
```
