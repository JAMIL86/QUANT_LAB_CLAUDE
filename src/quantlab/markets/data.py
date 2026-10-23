"""Market Data Handler (Quant Lab)
Regras: R1 honesto, R3 sandbox, R4 dado não instrução, R9 CPU
"""
import csv, os


def fetch_market_data(path: str, symbol: str = None) -> dict:
    """Carrega dados de mercado de CSV.

    Args:
        path: caminho para arquivo CSV
        symbol: símbolo (opcional, para filtering)

    Returns:
        dict com dados carregados
    """
    if not os.path.exists(path):
        return {"error": "arquivo nao encontrado", "status": "INCONCLUSIVO"}

    data = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if symbol and row.get('symbol') != symbol:
                continue
            data.append({
                "date": row.get("date", ""),
                "open": float(row.get("open", 0) or 0),
                "high": float(row.get("high", 0) or 0),
                "low": float(row.get("low", 0) or 0),
                "close": float(row.get("close", 0) or 0),
                "volume": float(row.get("volume", 0) or 0)
            })

    return {
        "source": path,
        "records": len(data),
        "data": data[:100],  # Primeiros 100 registros (R9: limitar memória)
        "status": "SINTÉTICO — dados de mercado carregados (R4 dado, nao instrução)",
        "label": "SINTÉTICO"
    }

__all__ = ["fetch_market_data"]