"""Nomeação dos segmentos e sugestão de ação de marketing, a partir do
perfil médio de RFM de cada grupo (classificação relativa entre os grupos)."""

import pandas as pd

ACOES = {
    "Campeões": "Programa de fidelidade e acesso antecipado a lançamentos",
    "Fiéis": "Cross-sell e incentivo para virar campeão",
    "Em risco": "Cupom de reativação e contato personalizado",
    "Novos": "E-mail de boas-vindas e incentivo à compra",
    "Hibernando": "Campanha de reengajamento de baixo custo",
}


def classificar_segmentos(perfil: pd.DataFrame) -> pd.DataFrame:
    """`perfil`: índice = Segmento, colunas Recencia/Frequencia/Valor (médias).

    Retorna o mesmo DataFrame com as colunas Nome e Acao adicionadas.
    """
    p = perfil.copy()
    p["rank_recencia"] = p["Recencia"].rank()                      # 1 = mais recente
    p["rank_frequencia"] = p["Frequencia"].rank(ascending=False)   # 1 = mais frequente
    p["rank_valor"] = p["Valor"].rank(ascending=False)             # 1 = maior valor
    p["pontuacao"] = p["rank_recencia"] + p["rank_frequencia"] + p["rank_valor"]

    mediana_recencia = p["Recencia"].median()
    mediana_frequencia = p["Frequencia"].median()
    mediana_valor = p["Valor"].median()

    def classificar(linha: pd.Series) -> str:
        if linha["pontuacao"] == p["pontuacao"].min():
            return "Campeões"
        if linha["pontuacao"] == p["pontuacao"].max():
            return "Hibernando"
        if linha["Recencia"] > mediana_recencia:
            return "Em risco"
        if linha["Frequencia"] < mediana_frequencia and linha["Valor"] < mediana_valor:
            return "Novos"
        return "Fiéis"

    p["Nome"] = p.apply(classificar, axis=1)
    p["Acao"] = p["Nome"].map(ACOES)
    return p.drop(columns=["rank_recencia", "rank_frequencia", "rank_valor", "pontuacao"])