from flask import Flask, request, Response
import requests
from auth import AuthAD
import json

app = Flask(__name__)

API_BASE_URL = "http://localhost:8082/api/"

@app.route("/api/documentos", methods=["GET"])
def listar_documentos():
    # Query exatamente como recebida (sem ?)
    query_string = request.query_string.decode()

    # Endpoint correto
    url_request = f"{API_BASE_URL}documentos/"

    # Auth customizada
    auth = AuthAD(
        url=url_request,
        query=query_string
    )

    response = requests.get(
        url_request,
        params=request.args,
        auth=auth,
        timeout=10
    )

    # Se a API externa retornar JSON → repassa direto
    if response.headers.get("Content-Type", "").startswith("application/json"):
        return Response(
            response.content,
            status=response.status_code,
            content_type="application/json"
        )

    # Caso não seja JSON, repassa o erro cru
    return Response(
        response.content,
        status=response.status_code,
        content_type=response.headers.get("Content-Type", "text/plain")
    )

@app.route("/api/documentos/dados_gerais", methods=["GET"])
def listar_dados_gerais():
    # Query exatamente como recebida (sem ?)
    query_string = request.query_string.decode()

    # Endpoint correto
    url_request = f"{API_BASE_URL}documentos/dados_gerais"

    # Auth customizada
    auth = AuthAD(
        url=url_request,
        query=query_string
    )

    response = requests.get(
        url_request,
        params=request.args,
        auth=auth,
        timeout=30
    )

    # Se a API externa retornar JSON → repassa direto
    if response.headers.get("Content-Type", "").startswith("application/json"):
        return Response(
            response.content,
            status=response.status_code,
            content_type="application/json"
        )

    # Caso não seja JSON, repassa o erro cru
    return Response(
        response.content,
        status=response.status_code,
        content_type=response.headers.get("Content-Type", "text/plain")
    )

@app.route("/api/documentos/download", methods=["GET"])
def donwload():
    query_string = request.query_string.decode()

    # Endpoint correto
    url_request = f"{API_BASE_URL}documentos/download"

    # Auth customizada
    auth = AuthAD(
        url=url_request,
        query=query_string
    )

    response = requests.get(
        url_request,
        params=request.args,
        auth=auth,
        timeout=30
    )

    # Se a API externa retornar JSON → repassa direto
    if response.headers.get("Content-Type", "").startswith("application/json"):
        return Response(
            response.content,
            status=response.status_code,
            content_type="application/json"
        )

    # Caso não seja JSON, repassa o erro cru
    return Response(
        response.content,
        status=response.status_code,
        content_type=response.headers.get("Content-Type", "text/plain")
    )

@app.route("/api/rescisao/gerar_rescisao", methods=["POST"])
def gerar_rescisao():
    # Recupera dados enviados no body (JSON)
    payload = request.get_json(silent=True) or {}

    id_documento = payload.get("id_documento")
    data_rescisao = payload.get("data_rescisao", "")
    id_motivo_rescisao = payload.get("id_motivo_rescisao")
    estagiario_efetivado = payload.get("estagiario_efetivado", False)

    # Validação mínima (opcional, mas recomendado)
    if not id_documento or not id_motivo_rescisao:
        return Response(
            "Parâmetros obrigatórios não informados",
            status=400
        )

    # Endpoint correto da API externa
    url_request = f"{API_BASE_URL}rescisao/gerar_rescisao"

    # Payload que será enviado para a API externa
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
    app.run(debug=True)
