"""Limpeza das transações e cálculo dos indicadores RFM por cliente."""

from datetime import timedelta
import pandas as pd


def limpar_transacoes(df: pd.DataFrame) -> pd.DataFrame:
    """Remove registros sem cliente identificado, devoluções e valores inválidos."""
    df_limpo = df.copy()

    # Sem CustomerID não dá para segmentar o cliente
    df_limpo = df_limpo.dropna(subset=["CustomerID"])

    # InvoiceNo começa com "C" (cancelamento)
    df_limpo = df_limpo[~df_limpo["InvoiceNo"].astype(str).str.startswith("C")]

    # Linhas com quantidade ou preço não positivos não fazem sentido para o cálculo de valor
    df_limpo = df_limpo[(df_limpo["Quantity"] > 0) & (df_limpo["UnitPrice"] > 0)]

    return df_limpo


def calcular_rfm(df: pd.DataFrame, data_referencia: pd.Timestamp | None = None) -> pd.DataFrame:
    """Calcula Recência, Frequência e Valor monetário por CustomerID.

    `df` deve já estar limpo (ver `limpar_transacoes`).
    `data_referencia` é o "hoje" usado para calcular a recência; por padrão,
    usa um dia depois da última transação do próprio dataset (já que os
    dados são históricos, não há um "hoje" real).
    """
    df = df.copy()
    df["Valor"] = df["Quantity"] * df["UnitPrice"]

    if data_referencia is None:
        data_referencia = df["InvoiceDate"].max() + timedelta(days=1)

    rfm = df.groupby("CustomerID").agg(
        Recencia=("InvoiceDate", lambda x: (data_referencia - x.max()).days),
        Frequencia=("InvoiceNo", "nunique"),
        Valor=("Valor", "sum"),
    )

    return rfm