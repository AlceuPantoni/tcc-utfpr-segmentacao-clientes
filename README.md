# Segmentação de Clientes com RFM e K-Means

Trabalho de Conclusão de Curso — Especialização em Ciência de Dados, UTFPR.

Segmentação de clientes de um e-commerce a partir do histórico de transações, utilizando a análise RFM (Recência, Frequência, Valor monetário) combinada ao algoritmo K-Means. O objetivo é agrupar os clientes por comportamento de compra e associar uma ação de marketing a cada segmento identificado.

## Dataset

[Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail) (UCI Machine Learning Repository) — transações de um e-commerce do Reino Unido entre dezembro de 2010 e dezembro de 2011 (~541 mil registros).

O dataset é baixado automaticamente na primeira execução e **não** é versionado neste repositório.

## Estrutura do projeto

```
├── src/segmentacao/        # lógica reutilizável (dados, RFM, clustering, nomeação)
├── notebooks/              # notebook principal: exploração, gráficos e narrativa
├── tests/                  # testes automatizados
├── outputs/                # resultados gerados (CSV e figuras)
└── data/raw/               # dataset baixado (não versionado)
```

## Como executar

Pré-requisitos: Python 3.12 (gerenciado via [pyenv](https://github.com/pyenv/pyenv)).

```bash
# clonar o repositório
git clone https://github.com/AlceuPantoni/tcc-utfpr-segmentacao-clientes.git
cd tcc-utfpr-segmentacao-clientes

# ambiente virtual
pyenv local 3.12.12
python -m venv .venv
source .venv/bin/activate

# dependências
pip install -r requirements.txt
pip install -e .
```

Abra `notebooks/01_segmentacao_rfm_kmeans.ipynb` no Jupyter ou no VSCode e execute as células em ordem (o dataset é baixado automaticamente na primeira execução).

## Testes

```bash
pytest tests/
```

## Resultados

A segmentação (k=5, definido por cotovelo e silhueta) identificou cinco perfis de cliente:

| Segmento | Perfil | Ação sugerida |
|---|---|---|
| Campeões | Compra recente, frequente, alto valor | Programa de fidelidade e acesso antecipado a lançamentos |
| Fiéis | Compra recente, frequente, valor alto | Cross-sell e incentivo para virar campeão |
| Em risco | Não compra há algum tempo, valor médio | Cupom de reativação e contato personalizado |
| Novos | Compra recente, pouca frequência/valor | E-mail de boas-vindas e incentivo à compra |
| Hibernando | Não compra há muito tempo, baixo valor | Campanha de reengajamento de baixo custo |

A lista completa de clientes por segmento é exportada em `outputs/segmentos_clientes.csv`.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## Autor

Alceu Pantoni Neto