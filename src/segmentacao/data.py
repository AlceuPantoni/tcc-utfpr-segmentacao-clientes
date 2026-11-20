"""Download e carga do dataset Online Retail (UCI)."""

import io
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd

URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
XLSX_PATH = RAW_DIR / "online_retail.xlsx"


def _garantir_dataset(url: str = URL, destino: Path = XLSX_PATH) -> Path:
    """Garante que o Online Retail.xlsx exista em data/raw/, baixando se necessário.

    Retorna o caminho do arquivo .xlsx local.
    """
    if destino.exists():
        print(f"Dataset já existe no projeto, pulando download.")
        return destino

    destino.parent.mkdir(parents=True, exist_ok=True)
    zip_path = destino.parent / "online_retail.zip"

    print(f"Baixando dataset de {url} ...")
    try:
        urlretrieve(url, zip_path)
    except Exception as exc:
        raise RuntimeError(
            "Não foi possível baixar o dataset automaticamente. "
            f"Baixe manualmente em {url} e coloque o arquivo .xlsx extraído "
            f"em {destino}."
        ) from exc

    print("Extraindo o .xlsx do zip...")
    with zipfile.ZipFile(zip_path) as z:
        nomes_xlsx = [n for n in z.namelist() if n.lower().endswith(".xlsx")]
        if not nomes_xlsx:
            raise RuntimeError("O arquivo .zip baixado não contém um .xlsx.")
        with z.open(nomes_xlsx[0]) as origem, open(destino, "wb") as saida:
            saida.write(io.BytesIO(origem.read()).getbuffer())

    zip_path.unlink()
    print(f"Dataset pronto em {destino}.")
    return destino


def carregar_transacoes(caminho: Path = XLSX_PATH) -> pd.DataFrame:
    """Carrega o Online Retail em um DataFrame, com os tipos já ajustados."""
    caminho = _garantir_dataset(destino=caminho)
    df = pd.read_excel(caminho)

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["CustomerID"] = df["CustomerID"].astype("Int64")

    return df