"""Gera ``src/api_brasil/generated/catalog.py`` a partir do catálogo público
do gateway APIBrasil (``GET /api/v2/documentations``).

Uso::

    python scripts/codegen.py                          # produção
    APIBRASIL_BASE_URL=... python scripts/codegen.py   # outra base (ex: homolog)
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Tuple

DEFAULT_BASE_URL = "https://gateway.apibrasil.io/api/v2"
OUTPUT = (
    Path(__file__).resolve().parent.parent
    / "src"
    / "api_brasil"
    / "generated"
    / "catalog.py"
)

_API_V2 = re.compile(r"/api/v2/(.+)$")
_CONSULTA = re.compile(r"^consulta/([^/]+)/credits$")


def fetch_catalog(base_url: str) -> Any:
    url = base_url.rstrip("/") + "/documentations"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "APIBRASIL/SDK-PYTHON codegen",
        },
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        raw = response.read()

    try:
        return json.loads(raw.decode("utf-8"))
    except ValueError:
        sys.exit("Falha ao decodificar o catálogo (JSON inválido).")


def collect(documentations: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], int]:
    service_actions: Dict[str, set] = {}
    consulta_tipos: Dict[str, Dict[str, Any]] = {}
    consulta_servicos: set = set()
    endpoint_count = 0

    for doc in documentations:
        for endpoint in doc.get("endpoints") or []:
            url = endpoint.get("url")
            if not isinstance(url, str):
                continue

            match = _API_V2.search(url)
            if not match:
                continue

            endpoint_count += 1
            full_path = match.group(1).strip("/")
            segments = full_path.split("/")
            service = segments[0]
            action = "/".join(segments[1:])

            if not service:
                continue

            service_actions.setdefault(service, set())
            if action:
                service_actions[service].add(action)

            consulta = _CONSULTA.match(full_path)
            if consulta:
                consulta_servicos.add(consulta.group(1))
                body = endpoint.get("body")

                if (
                    isinstance(body, dict)
                    and isinstance(body.get("tipo"), str)
                    and body["tipo"]
                ):
                    fields = sorted(
                        key for key in body if key not in ("tipo", "homolog")
                    )
                    consulta_tipos[body["tipo"]] = {
                        "service": consulta.group(1),
                        "fields": [str(field) for field in fields],
                    }

    collected = {
        "whatsapp": sorted(service_actions.get("whatsapp", set())),
        "evolution": sorted(service_actions.get("evolution", set())),
        "whatsmeow": sorted(service_actions.get("whatsmeow", set())),
        "consulta_servicos": sorted(consulta_servicos),
        "consulta_tipos": dict(sorted(consulta_tipos.items())),
        "service_actions": {
            service: sorted(actions)
            for service, actions in sorted(service_actions.items())
        },
    }

    return collected, endpoint_count


def _list_literal(values: List[str], indent: int) -> str:
    if not values:
        return "[]"

    pad = " " * indent
    body = "\n".join('{}    "{}",'.format(pad, value) for value in values)

    return "[\n" + body + "\n" + pad + "]"


def render(collected: Dict[str, Any], docs: int, endpoints: int) -> str:
    lines: List[str] = []
    tipos = collected["consulta_tipos"]

    lines.append('"""')
    lines.append("ARQUIVO GERADO AUTOMATICAMENTE — não edite manualmente.")
    lines.append("")
    lines.append("Fonte: https://gateway.apibrasil.io/api/v2/documentations")
    lines.append("Regenerar: python scripts/codegen.py")
    lines.append("")
    lines.append(
        "{} documentações, {} endpoints, {} tipos de consulta conhecidos.".format(
            docs, endpoints, len(tipos)
        )
    )
    lines.append('"""')
    lines.append("")
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from typing import Dict, List, Optional")
    lines.append("")
    lines.append("__all__ = [")
    for name in (
        "WHATSAPP_ACTIONS",
        "EVOLUTION_PATHS",
        "WHATSMEOW_ACTIONS",
        "CONSULTA_SERVICOS",
        "CONSULTA_TIPOS",
        "SERVICE_ACTIONS",
        "consulta_tipo",
        "service_actions",
    ):
        lines.append('    "{}",'.format(name))
    lines.append("]")
    lines.append("")
    lines.append(
        "#: Actions conhecidas da API de WhatsApp (``POST /whatsapp/{action}``)."
    )
    lines.append(
        "WHATSAPP_ACTIONS: List[str] = " + _list_literal(collected["whatsapp"], 0)
    )
    lines.append("")
    lines.append(
        "#: Caminhos conhecidos da Evolution API (``POST /evolution/{controller}/{action}``)."
    )
    lines.append(
        "EVOLUTION_PATHS: List[str] = " + _list_literal(collected["evolution"], 0)
    )
    lines.append("")
    lines.append("#: Actions conhecidas do WhatsMeow (``POST /whatsmeow/{action}``).")
    lines.append(
        "WHATSMEOW_ACTIONS: List[str] = " + _list_literal(collected["whatsmeow"], 0)
    )
    lines.append("")
    lines.append(
        "#: Serviços de consulta por crédito (``POST /consulta/{service}/credits``)."
    )
    lines.append(
        "CONSULTA_SERVICOS: List[str] = "
        + _list_literal(collected["consulta_servicos"], 0)
    )
    lines.append("")
    lines.append(
        "#: Metadados por tipo de consulta: serviço da rota e campos do body de exemplo."
    )
    lines.append("CONSULTA_TIPOS: Dict[str, Dict[str, object]] = {")
    for tipo, meta in tipos.items():
        fields = "[" + ", ".join('"{}"'.format(field) for field in meta["fields"]) + "]"
        entry = '    "{}": {{"service": "{}", "fields": {}}},'.format(
            tipo, meta["service"], fields
        )
        if len(entry) <= 100:
            lines.append(entry)
        else:
            lines.append('    "{}": {{'.format(tipo))
            lines.append('        "service": "{}",'.format(meta["service"]))
            lines.append('        "fields": [')
            for field in meta["fields"]:
                lines.append('            "{}",'.format(field))
            lines.append("        ],")
            lines.append("    },")
    lines.append("}")
    lines.append("")
    lines.append("#: Actions documentadas por serviço do gateway.")
    lines.append("SERVICE_ACTIONS: Dict[str, List[str]] = {")
    for service, actions in collected["service_actions"].items():
        entry = (
            '    "{}": ['.format(service)
            + ", ".join('"{}"'.format(action) for action in actions)
            + "],"
        )
        if len(entry) <= 100:
            lines.append(entry)
        else:
            lines.append('    "{}": ['.format(service))
            for action in actions:
                lines.append('        "{}",'.format(action))
            lines.append("    ],")
    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append("def consulta_tipo(tipo: str) -> Optional[Dict[str, object]]:")
    lines.append(
        '    """Metadados de um tipo de consulta (``None`` quando desconhecido)."""'
    )
    lines.append("    return CONSULTA_TIPOS.get(tipo)")
    lines.append("")
    lines.append("")
    lines.append("def service_actions(service: str) -> List[str]:")
    lines.append('    """Actions documentadas de um serviço."""')
    lines.append("    return SERVICE_ACTIONS.get(service, [])")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    base_url = os.environ.get("APIBRASIL_BASE_URL") or DEFAULT_BASE_URL

    print("Baixando catálogo de {}/documentations ...".format(base_url))
    payload = fetch_catalog(base_url)
    documentations = (
        payload.get("documentations", payload) if isinstance(payload, dict) else payload
    )

    if not isinstance(documentations, list):
        sys.exit('Resposta inesperada: "documentations" não é uma lista.')

    collected, endpoints = collect(documentations)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        render(collected, len(documentations), endpoints),
        encoding="utf-8",
        newline="\n",
    )
    _format(OUTPUT)

    print(
        "OK: {} ({} docs, {} endpoints, {} tipos)".format(
            OUTPUT, len(documentations), endpoints, len(collected["consulta_tipos"])
        )
    )


def _format(path: Path) -> None:
    """Aplica ``black`` no arquivo gerado, se disponível (mantém o estilo do repo)."""
    try:
        import subprocess

        subprocess.run(
            [sys.executable, "-m", "black", "--quiet", str(path)],
            check=False,
        )
    except Exception:  # noqa: BLE001 - black é opcional
        pass


if __name__ == "__main__":
    main()
