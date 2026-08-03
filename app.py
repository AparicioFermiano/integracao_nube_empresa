from flask import Flask, request, Response
import requests
from auth import AuthAD
import json

app = Flask(__name__)

API_BASE_URL = "https://www.nube.com.br/api/"

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

@app.route("/api/documentos/aprovacao", methods=["POST"])
def aprovacao():
    # Recupera dados enviados no body (JSON)
    payload = request.get_json(silent=True) or {}

    estudante = payload.get("estudante") or {}
    contrato = payload.get("contrato") or {}

    # Validação mínima: o que a API rejeita com status 400
    obrigatorios = (
        ("estudante.nome", estudante.get("nome")),
        ("estudante.cpf", estudante.get("cpf")),
        ("contrato.cnpj_contratacao", contrato.get("cnpj_contratacao")),
        ("contrato.data_inicio", contrato.get("data_inicio")),
        ("contrato.bolsa_auxilio", contrato.get("bolsa_auxilio")),
    )

    faltando = [campo for campo, valor in obrigatorios if not valor]

    if faltando:
        return Response(
            f"Parâmetros obrigatórios não informados: {', '.join(faltando)}",
            status=400
        )

    # Endpoint correto da API externa
    url_request = f"{API_BASE_URL}documentos/aprovacao"

    # Payload que será enviado para a API externa. Os demais campos da ficha
    # (RG, endereço, escolaridade, dependentes, supervisor, representante,
    # auxílio transporte, atividades) são repassados como recebidos; o que
    # faltar volta na lista "pendencias" do retorno.
    data = {
        "estudante": estudante,
        "contrato": contrato
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
