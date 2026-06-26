import pandas as pd


MESES_3M = [
    "junho/2026",
    "maio/2026",
    "abril/2026",
]

MESES_6M = [
    "junho/2026",
    "maio/2026",
    "abril/2026",
    "março/2026",
    "fevereiro/2026",
    "janeiro/2026",
]

MESES_12M = [
    "junho/2026",
    "maio/2026",
    "abril/2026",
    "março/2026",
    "fevereiro/2026",
    "janeiro/2026",
    "dezembro/2025",
    "novembro/2025",
    "outubro/2025",
    "setembro/2025",
    "agosto/2025",
    "julho/2025",
]


def gerar_base_decisao_produto(
    estoque: pd.DataFrame,
    vendas: pd.DataFrame,
    industria: pd.DataFrame
) -> pd.DataFrame:

    produtos_industria = set(industria["CodProduto"])

    estoque_filtrado = estoque[
        estoque["CodProduto"].isin(produtos_industria)
    ].copy()

    estoque_filtrado["Eh_CD"] = estoque_filtrado["CodFilial"] == "900"

    estoque_agrupado = (
        estoque_filtrado
        .groupby("CodProduto", as_index=False)
        .agg(
            Descricao=("Descricao", "first"),
            Fabricante=("Fabricante", "first"),
            Linha=("Linha", "first"),
            Estoque_Lojas=("QtEstoqueComercial", lambda x: x[~estoque_filtrado.loc[x.index, "Eh_CD"]].sum()),
            Estoque_CD=("QtEstoqueComercial", lambda x: x[estoque_filtrado.loc[x.index, "Eh_CD"]].sum()),
            Media_Utilizada=("Media_Utilizada", "sum"),
            StatusProduto=("StatusProduto", "first"),
        )
    )

    vendas_filtradas = vendas[
        vendas["CodProduto"].isin(produtos_industria)
    ].copy()

    vendas_filtradas["Venda_3M"] = vendas_filtradas[MESES_3M].sum(axis=1)
    vendas_filtradas["Venda_6M"] = vendas_filtradas[MESES_6M].sum(axis=1)
    vendas_filtradas["Venda_12M"] = vendas_filtradas[MESES_12M].sum(axis=1)

    vendas_agrupadas = (
        vendas_filtradas
        .groupby("CodProduto", as_index=False)
        .agg(
            Venda_3M=("Venda_3M", "sum"),
            Venda_6M=("Venda_6M", "sum"),
            Venda_12M=("Venda_12M", "sum"),
        )
    )

    base = estoque_agrupado.merge(
        vendas_agrupadas,
        on="CodProduto",
        how="left"
    )

    base[["Venda_3M", "Venda_6M", "Venda_12M"]] = base[
        ["Venda_3M", "Venda_6M", "Venda_12M"]
    ].fillna(0)

    base["Media_3M"] = base["Venda_3M"] / 3
    base["Media_6M"] = base["Venda_6M"] / 6
    base["Media_12M"] = base["Venda_12M"] / 12

    base["Estoque_Total"] = base["Estoque_Lojas"] + base["Estoque_CD"]
    
    # Dias de estoque usando as médias

# Dias de estoque usando as médias

    base["Dias_Estoque_3M"] = (
        base["Estoque_Total"] / base["Media_3M"]
    ).replace([float("inf")], 9999)

    base["Dias_Estoque_6M"] = (
        base["Estoque_Total"] / base["Media_6M"]
    ).replace([float("inf")], 9999)

    base["Dias_Estoque_12M"] = (
        base["Estoque_Total"] / base["Media_12M"]
    ).replace([float("inf")], 9999)

    # Converte para dias

    base["Dias_Estoque_3M"] = base["Dias_Estoque_3M"] * 30
    base["Dias_Estoque_6M"] = base["Dias_Estoque_6M"] * 30
    base["Dias_Estoque_12M"] = base["Dias_Estoque_12M"] * 30

    # Trata divisões por zero

    base["Dias_Estoque_3M"] = base["Dias_Estoque_3M"].fillna(9999)
    base["Dias_Estoque_6M"] = base["Dias_Estoque_6M"].fillna(9999)
    base["Dias_Estoque_12M"] = base["Dias_Estoque_12M"].fillna(9999)

    # Elegibilidade para compra

    base["Elegivel_Compra"] = "NÃO"

    base.loc[
        base["StatusProduto"] == "ATIVO",
        "Elegivel_Compra"
    ] = "SIM"

    base["Motivo_Nao_Compra"] = ""

    base.loc[
        base["Elegivel_Compra"] == "NÃO",
        "Motivo_Nao_Compra"
    ] = "Status: " + base["StatusProduto"].astype(str)

    return base