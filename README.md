# Integração Nube (empresa)

API em Flask que repassa chamadas para a [API da Nube](https://www.nube.com.br/api/), assinando cada requisição com o cabeçalho `security-hash` (SHA-256 de URL + segredo + query, em Base64 com o token).

## Requisitos

Python 3.10+.

## Rodar

```bash
python -m venv .venv
.venv/bin/pip install flask requests        # Windows: .venv\Scripts\pip install flask requests
```

Preencha `SECRET` e `TOKEN` em `auth.py` com as credenciais da Nube. **Não commite as credenciais reais.**

```bash
.venv/bin/python app.py                     # Windows: .venv\Scripts\python app.py
```

A API sobe em <http://localhost:5000> (modo debug).

## Endpoints

| Método | Rota | Repassa para |
|---|---|---|
| GET | `/api/documentos` | `documentos/` |
| GET | `/api/documentos/dados_gerais` | `documentos/dados_gerais` |
| GET | `/api/documentos/download` | `documentos/download` |
| POST | `/api/rescisao/gerar_rescisao` | `rescisao/gerar_rescisao` (corpo JSON) |

Os parâmetros de query são repassados como vieram, e a resposta da Nube volta sem alteração.

## Estrutura

```
app.py     as rotas
auth.py    a assinatura das requisições (AuthAD)
```

## Homologação

Não há ambiente de homologação.
