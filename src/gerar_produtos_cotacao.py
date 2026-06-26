import pandas as pd


def gerar_produtos_cotacao(
    estoque: pd.DataFrame,
    vendas: pd.DataFrame,
    industria: pd.DataFrame
) -> pd.DataFrame:
    produtos_industria = set(industria["CodProduto"])

    produtos = estoque[
        estoque["CodProduto"].isin(produtos_industria)
    ].copy()

    produtos = (
        produtos
        .sort_values("CodProduto")
        .drop_duplicates(subset=["CodProduto"])
    )

    produtos = produtos.merge(
        industria[
            [
                "CodProduto",
                "DescricaoIndustria",
                "Preco_Fabrica",
                "Default_Preco",
                "Default_Desc"
            ]
        ],
        on="CodProduto",
        how="left"
    )

    return produtos