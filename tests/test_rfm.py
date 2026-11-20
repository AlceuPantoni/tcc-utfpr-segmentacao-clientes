"""Teste do cálculo de RFM com um conjunto de transações fictício e conhecido."""

import pandas as pd
from segmentacao.rfm import calcular_rfm, limpar_transacoes

def _transacoes_exemplo() -> pd.DataFrame:
    return pd.DataFrame({
        "InvoiceNo": ["1001", "1002", "1003", "C1004", "1005"],
        "StockCode": ["A", "B", "A", "A", "B"],
        "Description": ["Produto A", "Produto B", "Produto A", "Produto A", "Produto B"],
        "Quantity": [2, 1, 3, -1, 5],
        "InvoiceDate": pd.to_datetime([
            "2011-01-01", "2011-01-10", "2011-01-15", "2011-01-16", "2011-01-20",
        ]),
        "UnitPrice": [10.0, 20.0, 10.0, 10.0, 5.0],
        "CustomerID": [1, 1, 1, 1, None],
        "Country": ["UK"] * 5,
    })

def test_limpar_remove_sem_cliente_e_devolucoes():
    df = _transacoes_exemplo()
    df_limpo = limpar_transacoes(df)

    # a linha sem CustomerID (cliente None) e a devolução (C1004) devem sumir;
    # sobram as 3 compras do cliente 1 (1001, 1002, 1003)
    assert len(df_limpo) == 3
    assert not bool(df_limpo["InvoiceNo"].astype(str).str.startswith("C").any())
    assert bool(df_limpo["CustomerID"].notna().all())


def test_calcular_rfm_valores_esperados():
    df = _transacoes_exemplo()
    df_limpo = limpar_transacoes(df)

    data_referencia = pd.Timestamp("2011-01-20")
    rfm = calcular_rfm(df_limpo, data_referencia=data_referencia)

    assert len(rfm) == 1                                        # só o cliente 1 sobrou após a limpeza
    assert rfm.loc[1, "Recencia"] == 5                          # última compra em 01-15, referência 01-20
    assert rfm.loc[1, "Frequencia"] == 3                        # três pedidos distintos (1001, 1002, 1003)
    assert rfm.loc[1, "Valor"] == 2 * 10 + 1 * 20 + 3 * 10      # 20 + 20 + 30 = 70