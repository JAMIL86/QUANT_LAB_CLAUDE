"""Report Generator (Quant Lab)
Regras: R1 honesto, R3 sandbox, R8 seed/hash
"""
import json


def generate_report(result: dict, out_json: str = None, out_html: str = None) -> dict:
    """Gera relatório JSON + HTML.

    Args:
        result: dict com resultados do backtest/monte carlo/etc
        out_json: caminho para arquivo JSON (opcional)
        out_html: caminho para arquivo HTML (opcional)

    Returns:
        dict com paths dos arquivos gerados
    """
    output_files = {}

    # JSON sempre gerado (R8: fonte de verdade)
    if out_json:
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        output_files["json"] = out_json

    # HTML para leitura (não marketing — lab técnico)
    if out_html:
        html = _generate_html(result)
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(html)
        output_files["html"] = out_html

    return output_files


def _generate_html(result: dict) -> str:
    """Gera HTML básico para visualização."""
    status = result.get("status", "N/A")
    label = result.get("label", "N/A")
    rules = result.get("rules_applied", [])

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Quant Lab — Report</title>
    <style>
        body {{ font-family: monospace; margin: 20px; }}
        h1 {{ color: #333; }}
        .status {{ padding: 10px; background: #f0f0f0; }}
        .label {{ color: #666; }}
        pre {{ background: #fafafa; padding: 10px; }}
    </style>
</head>
<body>
    <h1>Quant Lab — Relatório</h1>
    <div class="status">Status: {status}</div>
    <div class="label">Label: {label}</div>
    <p>Regras: {', '.join(rules)}</p>
    <pre>{json.dumps(result, indent=2, ensure_ascii=False)}</pre>
</body>
</html>"""
    return html

__all__ = ["generate_report"]