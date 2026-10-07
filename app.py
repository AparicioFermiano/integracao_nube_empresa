from flask import Flask, request, Response
import requests
from auth import AuthAD
import json

app = Flask(__name__)

API_BASE_URL = "https://www.nube.com.br/api/"

def repassar_get_para_nube(caminho, timeout):
    """Repassa o GET para `caminho` na Nube, assinado, e devolve a resposta."""
    # A assinatura usa a query crua, como chegou (sem o ?).
    query_string = request.query_string.decode()

    url_request = f"{API_BASE_URL}{caminho}"

    auth = AuthAD(
        url=url_request,
        query=query_string
    )

    response = requests.get(
        url_request,
        params=request.args,
        auth=auth,
        timeout=timeout
    )

    # JSON volta como application/json puro, sem charset; o resto, como veio.
    content_type = response.headers.get("Content-Type", "text/plain")
    if content_type.startswith("application/json"):
        content_type = "application/json"

    return Response(
        response.content,
        status=response.status_code,
        content_type=content_type
    )

@app.route("/api/documentos", methods=["GET"])
def listar_documentos():
    return repassar_get_para_nube("documentos/", timeout=10)

@app.route("/api/documentos/dados_gerais", methods=["GET"])
def listar_dados_gerais():
    return repassar_get_para_nube("documentos/dados_gerais", timeout=30)

@app.route("/api/documentos/download", methods=["GET"])
def donwload():
    return repassar_get_para_nube("documentos/download", timeout=30)

@app.route("/api/rescisao/gerar_rescisao", methods=["POST"])
def gerar_rescisao():
    payload = request.get_json(silent=True) or {}

    id_documento = payload.get("id_documento")
    data_rescisao = payload.get("data_rescisao", "")
    id_motivo_rescisao = payload.get("id_motivo_rescisao")
    estagiario_efetivado = payload.get("estagiario_efetivado", False)

    if not id_documento or not id_motivo_rescisao:
        return Response(
            "Parâmetros obrigatórios não informados",
            status=400
        )

    url_request = f"{API_BASE_URL}rescisao/gerar_rescisao"

    data = {
        "id_documento": id_documento,
        "data_rescisao": data_rescisao,
        "id_motivo_rescisao": id_motivo_rescisao,
        "estagiario_efetivado": estagiario_efetivado
    }

    response = requests.post(
        url=url_request, auth=AuthAD(url=url_request, query=json.dumps(data)),
        json=data
    )

    return Response(
        response.content,
        status=response.status_code,
        content_type="application/json"
    )

if __name__ == "__main__":
    app.run()
