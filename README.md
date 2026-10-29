# Integração Nube (empresa)

API em Flask que repassa chamadas para a [API da Nube](https://www.nube.com.br/api/), assinando cada requisição com o cabeçalho `security-hash` (SHA-256 de URL + segredo + query, em Base64 com o token).

## Requisitos

Python 3.10+.

## Rodar

```bash
python -m venv .venv
.venv/bin/pip install flask requests        # Windows: .venv\Scripts\pip install flask requests
```

As credenciais da Nube entram pelas variáveis de ambiente `NUBE_SECRET` e `NUBE_TOKEN`; sem elas, `auth.py` assina com os marcadores `<SECRET>` e `<TOKEN>`. **Não commite as credenciais reais.**

```bash
export NUBE_SECRET='...' NUBE_TOKEN='...'   # Windows (PowerShell): $env:NUBE_SECRET='...'; $env:NUBE_TOKEN='...'
.venv/bin/python app.py                     # Windows: .venv\Scripts\python app.py
```

A API sobe em <http://localhost:5000>. Para depurar, defina `FLASK_DEBUG=1` antes de subir: isso liga o debugger do Werkzeug, que executa código pelo navegador e mostra as variáveis (credenciais inclusive). Só na sua máquina.

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
