"""Preparação de features e segmentação de clientes com K-Means."""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42  # fixo por reprodutibilidade (RNF04)


def preparar_features(rfm: pd.DataFrame) -> np.ndarray:
    """Aplica log(1+x) (corrige a assimetria) e normaliza (StandardScaler).

    O K-Means usa distância euclidiana, então sem essas duas transformações
    os poucos clientes com Frequência/Valor muito altos dominariam os clusters.
    """
    log_rfm = np.log1p(rfm[["Recencia", "Frequencia", "Valor"]])
    return StandardScaler().fit_transform(log_rfm)


def avaliar_k(X: np.ndarray, k_min: int = 2, k_max: int = 10) -> pd.DataFrame:
    """Calcula inércia (cotovelo) e silhouette para cada k no intervalo.

    Retorna um DataFrame com uma linha por k — o notebook decide, olhando os
    gráficos, qual k usar; esta função não decide por você.
    """
    resultados = []
    for k in range(k_min, k_max + 1):
        modelo = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        rotulos = modelo.fit_predict(X)
        resultados.append({
            "k": k,
            "inertia": modelo.inertia_,
            "silhouette": silhouette_score(X, rotulos),
        })
    return pd.DataFrame(resultados)


def segmentar(X: np.ndarray, k: int) -> tuple[np.ndarray, KMeans]:
    """Roda o K-Means final com o k escolhido. Retorna os rótulos e o modelo."""
    modelo = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
    rotulos = modelo.fit_predict(X)
    return rotulos, modelo